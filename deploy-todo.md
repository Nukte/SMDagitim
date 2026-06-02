# Deploy TODO

Bu dosya projeyi Vercel (frontend) ve harici bir host (backend) üzerinde üretime taşımak için gereken adımları listeler.

## Özet Adımlar

1. Frontend: Vercel'e deploy
2. Backend: üretim host seçimi (Render/Fly/Railway/Heroku vs.)
3. Veritabanı: SQLite -> Postgres (kalıcı)
4. Object storage: MinIO (yerel) -> S3 / managed MinIO
5. Güvenlik: secrets yönetimi, JWT rotasyonu, güçlü parolalar
6. CI/CD ve smoke testler

---

## 1) Frontend — Vercel
- Vercel projesi oluştur, repo'yu bağla.
- Ayarlar:
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `dist`
- Environment Variables (Vercel > Settings > Environment Variables):
  - Eğer frontend `import.meta.env` ile kullanıyorsa `VITE_BACKEND_URL` veya benzeri ayarla.
- Deploy adımları:

```bash
# yerel test
cd frontend
npm install
npm run build
# preview
npm run preview
```

- Doğrulama:
  - Tarayıcıda deploy edilmiş siteyi açarak API çağrılarının doğru BACKEND_URL'e gittiğinden emin ol.

## 2) Backend — Hosting Seçimi ve Hazırlık
- Önerilen sağlayıcılar: Render, Fly, Railway, Heroku, AWS ECS/Fargate (container ile) veya DigitalOcean App Platform.
- Basit ve hızlı: Render veya Railway — Postgres ve S3 entegrasyonu kolay.

Gerekli hazırlıklar:
- `Dockerfile` ekle (container deploy planlanıyorsa).
- Alternatif: doğrudan `uvicorn`/ASGI process ile deploy edilecekse sağlayıcının başlangıç komutunu belirle.

Örnek Dockerfile (basit):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Sağlayıcıya bağlı olarak: `PORT` ortam değişkenini kullanmak için `uvicorn` komutunu ayarla.

## 3) Veritabanı — Kalıcı Depolama
- SQLite, sunucunun ephemeral dosya sistemi için uygun değil.
- Hedef: Postgres (managed DB) — sağlayıcınız üzerinden bir örnek oluşturun.
- SQLAlchemy bağlantı dizesini `.env` veya Secrets üzerinden ayarlayın (`DATABASE_URL` veya `SQLALCHEMY_DATABASE_URI`).
- Migration: `alembic` veya `sqlmodel`/`sqlalchemy` temelli migration çözümü ekleyin.

## 4) Object Storage — MinIO yerine S3 veya managed MinIO
- Üretimde MinIO'yu self-host etmek yerine AWS S3 veya sağlayıcının S3-compatible storage kullanılmasını öneririm.
- `config.py` içindeki `MINIO_*` env değişkenlerini sağlayıcı tarafından verilen değerlere göre ayarlayın.
- Eğer MinIO kullanacaksanız, erişilebilir bir URL ve credentials sağlayın; CORS ayarlarını MinIO üzerinde kontrol edin.

## 5) Güvenlik & Secrets
- Tüm hassas bilgiler: `JWT_SECRET`, `MINIO_SECRET_KEY`, OAuth client secrets, DB password → sağlayıcının Secret Manager'ına ekle.
- `backend/config.py` içindeki default `JWT_SECRET` ve `ADMIN_PASSWORD` çok zayıf; üretimde kullanmayın.
- TLS/HTTPS her yerde aktif olmalı (Vercel otomatik sağlıyor; backend için sağlayıcı üzerinden sertifika ayarlayın).
- Rotasyon politikası belirleyin (ör. 90 gün) ve deploy öncesi `JWT_SECRET` değişimini planlayın.

## 6) CORS, DEBUG ve Prod Ayarları
- `backend/config.py`:
  - `DEBUG=False` yapın.
  - `FRONTEND_URL` ve `BACKEND_URL` değerlerini prod URL'lerle güncelleyin.
  - CORS `allow_origins` production frontend URL'lerini içermeli.

## 7) CI/CD & Otomasyon
- Öneri: GitHub Actions ile iki pipeline:
  - Frontend: `build` ve `deploy` (Vercel otomatik deploy kullanıyorsanız Actions gerekli değil).
  - Backend: `build` Docker image → push to registry (Docker Hub / GHCR) → deploy trigger (Render/Fly webhook veya platform entegrasyonu).

## 8) Smoke tests ve Monitoring
- Basit smoke testler deploy sonrası çalıştırılmalı:
  - `GET /` health endpoint (beklenen JSON)
  - Auth login flow (test admin creds)
  - File upload presigned URL üretimi
- Monitoring/alerts: Sentry veya provider-integrated monitoring ekleyin.

## 9) Post-Deploy Checklist
- Secrets doğrulandı ve commit edilmedi.
- CORS ve HTTPS kontrolü tamamlandı.
- Veritabanı migration'ları uygulandı.
- Smoke testler geçti.
- Loglama + alert kuruldu (errors, high latency).

---

## Ek Notlar ve Komutlar
- Backend lokal olarak Docker ile test etmek için:

```bash
# build
docker build -t smd-backend -f backend/Dockerfile .
# run
docker run -e DATABASE_URL=postgres://user:pass@host/db -e MINIO_ENDPOINT=... -p 8000:8000 smd-backend
```

- Migration eklemek için (örnek Alembic):

```bash
pip install alembic
alembic init alembic
# sonra migration script oluştur ve apply
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---

İhtiyacınız olursa bu dosyayı otomatikleştirecek `Dockerfile`, `vercel.json` veya GitHub Actions workflow dosyalarını da hazırlayabilirim.
