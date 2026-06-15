# 🚀 SMD — Social Media Distribution Platform

> Tek panelden tüm sosyal medya platformlarına içerik dağıtımı.  
> LinkedIn · Instagram · Facebook · X (Twitter)

![Stack](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat-square&logo=vue.js)
![Stack](https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square&logo=fastapi)
![Stack](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite)
![Stack](https://img.shields.io/badge/MinIO-Object_Storage-C72E49?style=flat-square&logo=minio)

---

## ✨ Özellikler

- 🔗 **Multi-platform OAuth 2.0** — LinkedIn, Instagram, Facebook hesap bağlama (CSRF korumalı)
- 📝 **Tek editörden çoklu paylaşım** — İçeriği bir kez yaz, hepsine gönder
- 🖼️ **Medya desteği** — Görsel yükleme ve platform önizleme (presigned URL akışı)
- 👁️ **Gerçek zamanlı önizleme** — Her platform için ayrı post görünümü
- ⚡ **Asenkron yayın** — Platformlar paralel çalışır, biri hata alsa diğerleri etkilenmez
- 🎨 **"Void & Jade" design system** — Space Grotesk font, neon jade aksanlar ve modern mikro-etkileşimler
- 👑 **Gelişmiş Yönetici (Admin) Paneli** — Kayıtları açma/kapama, kullanıcıları aktif/pasif etme ve sistem ayarlarını yönetme
- 🔒 **Yüksek Güvenlik Standartları** — Token bazlı doğrulama, API key maskeleme, OAuth CSRF koruması ve dosya boyutu sınırlandırmaları

## 🛠️ Tech Stack

| Katman | Teknoloji |
|--------|-----------|
| Frontend | Vue 3 (Composition API) + Vite + Pinia |
| Backend | FastAPI (Python) + SQLAlchemy + SQLite |
| Depolama | MinIO (S3-compatible object storage) |
| Auth | JWT + OAuth 2.0 (LinkedIn, Meta) + State CSRF |
| Stil | Vanilla CSS — custom design system ("Void & Jade") |

## 📐 Mimari

```
┌─────────────────────────────────────────────────────┐
│                    Vue 3 Frontend                   │
│  Login → Dashboard → Post Editör → Publish Modal   │
│             └─► Admin Settings & Users              │
└────────────────────┬────────────────────────────────┘
                     │ REST API (axios)
┌────────────────────▼────────────────────────────────┐
│                  FastAPI Backend                     │
│  /api/auth   /api/oauth  /api/upload  /api/publish  │
│  /api/admin  /api/ai                                │
└──────┬──────────────┬──────────────────┬────────────┘
       │              │                  │
   SQLite DB    LinkedIn API       MinIO Storage
   (tokens)   Instagram API      (media files)
              Facebook API
```

## 🔒 Güvenlik Özellikleri
- **OAuth CSRF Koruması**: OAuth callback isteklerinde tek kullanımlık (one-time token) `state` parametresi doğrulaması yapılarak CSRF saldırıları önlenir.
- **Kullanıcı Durum Doğrulaması (`is_active`)**: Pasif durumdaki kullanıcılar login olamaz; ayrıca aktif oturumu varken pasife alınan kullanıcılar sonraki ilk isteklerinde otomatik olarak çıkışa yönlendirilir.
- **Güvenli Yönetim**: Yöneticilerin (Admin) kendi hesaplarını yanlışlıkla pasife almaları engellenmiştir.
- **Yapay Zeka (AI) Güvenliği**: AI servisleri JWT doğrulaması altına alınmış, API anahtarları maskelenmiş ve marka profil dosya yükleme sınırları (max 10MB) eklenmiştir.

## 💎 Gelişmiş UX / UI Sistemleri
- **Custom Reactive Toast**: Harici kütüphaneye bağımlı olmadan yazılmış, reactive yapıda toast bildirim sistemi (`toast.js`).
- **Global Confirm Modal**: Uygulama içi kritik işlemlerde (kullanıcıyı pasife alma, ayar değiştirme vb.) tarayıcı varsayılanları yerine tasarımla uyumlu custom modal kullanılır.
- **Skeleton Loaders**: Admin paneli veri yükleme süreçlerinde kullanıcı deneyimini artırmak için özel skeleton kartları kullanılmıştır.

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

# AI (Optional)
GEMINI_API_KEY=...
```

## 📄 Lisans

MIT
