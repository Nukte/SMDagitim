"""
Sosyal Medya Dağıtım Platformu — FastAPI Ana Uygulama
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import traceback
import sys

from config import get_settings
from database import engine, SessionLocal
from models import db_models
from routers import auth, upload, publish, oauth, ai, admin
from routers.auth import get_password_hash
from services.storage import initialize_bucket

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama yaşam döngüsü — başlangıç ve kapanış."""
    # Startup
    logger.info("🚀 Uygulama başlatılıyor...")
    db_models.Base.metadata.create_all(bind=engine)
    logger.info("📦 Veritabanı tabloları oluşturuldu.")

    # Veritabanı başlatma ve ilk admin oluşturma
    db = SessionLocal()
    try:
        settings_db = db.query(db_models.AppSettings).first()
        if not settings_db:
            db.add(db_models.AppSettings())
            db.commit()
            logger.info("⚙️  Varsayılan uygulama ayarları oluşturuldu.")
            
        app_settings = get_settings()
        admin_user = db.query(db_models.User).filter(db_models.User.email == app_settings.ADMIN_USERNAME).first()
        if not admin_user:
            hashed_pwd = get_password_hash(app_settings.ADMIN_PASSWORD)
            new_admin = db_models.User(
                email=app_settings.ADMIN_USERNAME,
                hashed_password=hashed_pwd,
                is_superuser=True,
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            logger.info("👑 İlk süper yönetici (admin) hesabı oluşturuldu.")
    except Exception as e:
        logger.error(f"Veritabanı başlatma hatası: {e}")
    finally:
        db.close()

    try:
        initialize_bucket()
        logger.info("🪣 MinIO bucket hazır.")
    except Exception as e:
        logger.warning(f"⚠️ MinIO bağlantısı kurulamadı: {e}")
        logger.warning("MinIO olmadan devam ediliyor. Dosya yükleme çalışmayacak.")

    yield

    # Shutdown
    logger.info("👋 Uygulama kapatılıyor...")


settings = get_settings()

app = FastAPI(
    title="Sosyal Medya Dağıtım Platformu",
    description="Tek noktadan tüm sosyal medya platformlarına içerik dağıtımı",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
cors_origins = [settings.FRONTEND_URL]
if settings.DEBUG:
    cors_origins.extend([
        "http://localhost:5173",
        "http://localhost:3000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(publish.router)
app.include_router(oauth.router)
app.include_router(ai.router)
app.include_router(admin.router)


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "debug": settings.DEBUG}

@app.get("/api/health", tags=["Health"])
async def api_health():
    """Docker/Coolify health check endpoint'i."""
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Uygulama genelindeki yakalanmayan tüm hataları (exception) yakalar.
    Hatanın tam olarak hangi dosyada ve satırda meydana geldiğini tespit edip loglar.
    """
    # Hatanın traceback (iz sürme) detaylarını al
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.extract_tb(exc_traceback)
    
    # Hataya neden olan en son konumu bul
    if tb:
        last_trace = tb[-1]
        filename = last_trace.filename
        line_no = last_trace.lineno
        func_name = last_trace.name
        error_location = f"{filename} satır {line_no} ({func_name} içinde)"
    else:
        error_location = "Bilinmeyen Konum"

    # Loglara detaylı şekilde yaz
    logger.error("="*50)
    logger.error(f"🚨 YAKALANMAYAN HATA: {request.method} {request.url}")
    logger.error(f"📍 KONUM: {error_location}")
    logger.error(f"❌ HATA: {str(exc)}")
    logger.error("Detaylı Traceback:")
    for line in traceback.format_exc().splitlines():
        logger.error(f"  {line}")
    logger.error("="*50)

    # İstemciye (frontend vb.) hatanın nerede olduğunu gösteren bir yanıt dön
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Sunucu içinde beklenmeyen bir hata oluştu.",
            "error_message": str(exc),
            "error_location": error_location,
            "error_type": type(exc).__name__
        }
    )
