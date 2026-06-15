"""
Sosyal Medya Dağıtım Platformu — FastAPI Ana Uygulama
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import get_settings
from database import engine
from models import db_models
from routers import auth, upload, publish, oauth, ai
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


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "debug": settings.DEBUG}

@app.get("/api/health", tags=["Health"])
async def api_health():
    """Docker/Coolify health check endpoint'i."""
    return {"status": "ok"}
