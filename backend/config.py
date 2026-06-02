"""
Merkezi konfigürasyon yönetimi.
Tüm ortam değişkenleri burada Pydantic Settings ile yönetilir.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # ── Uygulama ──
    APP_NAME: str = "Social Media Distribution"
    DEBUG: bool = Field(False, env="DEBUG")

    # ── Admin Giriş Bilgileri ──
    ADMIN_USERNAME: str = Field("admin", env="ADMIN_USERNAME")
    ADMIN_PASSWORD: str = Field("secret123", env="ADMIN_PASSWORD")

    # ── JWT ──
    JWT_SECRET: str = Field("dev-secret-key-change-in-production", env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24

    # ── MinIO ──
    MINIO_ENDPOINT: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = Field("admin", env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field("password", env="MINIO_SECRET_KEY")
    MINIO_BUCKET_NAME: str = "social-media-uploads"
    MINIO_PUBLIC_URL: str = ""  # Cloudflare Tunnel URL, boşsa MINIO_ENDPOINT kullanılır

    # ── Meta (Instagram / Facebook) ──
    META_CLIENT_ID: str = ""
    META_CLIENT_SECRET: str = ""
    META_ACCESS_TOKEN: str = ""

    # ── X / Twitter ──
    TWITTER_CLIENT_ID: str = ""
    TWITTER_CLIENT_SECRET: str = ""

    # ── LinkedIn ──
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""

    # ── URL'ler ──
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    # ── Veritabanı ──
    DATABASE_URL: str = "sqlite:///./app.db"

    @property
    def minio_public_url(self) -> str:
        return self.MINIO_PUBLIC_URL or self.MINIO_ENDPOINT

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
