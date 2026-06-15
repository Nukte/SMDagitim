# 🚀 SMD — Social Media Distribution Platform

> Tek panelden tüm sosyal medya platformlarına içerik dağıtımı.  
> LinkedIn · Instagram · Facebook · X (Twitter)

![Stack](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat-square&logo=vue.js)
![Stack](https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square&logo=fastapi)
![Stack](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite)
![Stack](https://img.shields.io/badge/MinIO-Object_Storage-C72E49?style=flat-square&logo=minio)

---

## ✨ Özellikler

- 🔗 **Multi-platform OAuth 2.0** — LinkedIn, Instagram, Facebook hesap bağlama
- 📝 **Tek editörden çoklu paylaşım** — İçeriği bir kez yaz, hepsine gönder
- 🖼️ **Medya desteği** — Görsel yükleme ve platform önizleme (presigned URL akışı)
- 👁️ **Gerçek zamanlı önizleme** — Her platform için ayrı post görünümü
- ⚡ **Asenkron yayın** — Platformlar paralel çalışır, biri hata alsa diğerleri etkilenmez

## 🛠️ Tech Stack

| Katman | Teknoloji |
|--------|-----------|
| Frontend | Vue 3 (Composition API) + Vite + Pinia |
| Backend | FastAPI (Python) + SQLAlchemy + SQLite |
| Depolama | MinIO (S3-compatible object storage) |
| Auth | JWT + OAuth 2.0 (LinkedIn, Meta) |
| Stil | Vanilla CSS — custom design system |

## 📐 Mimari

```
┌─────────────────────────────────────────────────────┐
│                    Vue 3 Frontend                   │
│  Login → Dashboard → Post Editör → Publish Modal   │
└────────────────────┬────────────────────────────────┘
                     │ REST API (axios)
┌────────────────────▼────────────────────────────────┐
│                  FastAPI Backend                     │
│  /api/auth  /api/oauth  /api/upload  /api/publish  │
└──────┬──────────────┬──────────────────┬────────────┘
       │              │                  │
   SQLite DB    LinkedIn API       MinIO Storage
   (tokens)   Instagram API      (media files)
              Facebook API
```

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.10+
- Node.js 18+
- MinIO (Docker ile)

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # API key'lerini doldur
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### MinIO (Docker)
```bash
docker run -p 9000:9000 -p 9001:9001 \
  minio/minio server /data --console-address ":9001"
```

## 🔑 Ortam Değişkenleri

```env
# LinkedIn
LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...

# Meta (Instagram / Facebook)
META_CLIENT_ID=...
META_CLIENT_SECRET=...

# MinIO
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

## 📸 Ekran Görüntüleri

> Dashboard, Post Editör ve Paylaşım Modal görüntüleri eklenecek.

## 📄 Lisans

MIT
