"""
SQLAlchemy ORM modelleri.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class OAuthToken(Base):
    """Sosyal medya platformlarının OAuth token'larını saklar."""
    __tablename__ = "oauth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), index=True)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(Integer, nullable=True)
    account_id = Column(String(255), nullable=True)
    account_name = Column(String(255), nullable=True)
    target_language = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PostHistory(Base):
    """Paylaşım geçmişini saklar."""
    __tablename__ = "post_history"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(36), unique=True, index=True)
    content = Column(Text)
    hashtags = Column(Text, nullable=True)  # JSON string
    media_keys = Column(Text, nullable=True)  # JSON string
    account_ids = Column(Text)  # JSON string
    status = Column(String(20), default="pending")  # pending, completed, partial, failed
    created_at = Column(DateTime, server_default=func.now())


class AISettings(Base):
    """AI Modülü ayarlarını saklar."""
    __tablename__ = "ai_settings"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), default="gemini")  # gemini, openai, anthropic vb.
    model_name = Column(String(100), default="gemini-2.5-flash") # gemini-1.5-pro, gpt-4o vb.
    api_key = Column(Text, nullable=True) # Şifreli veya düz metin
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class BrandProfile(Base):
    """AI İçerik Üretimi için Marka Kimliği."""
    __tablename__ = "brand_profile"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(255), nullable=True)
    tone = Column(String(100), nullable=True)  # Profesyonel, Eğlenceli, Samimi vb.
    target_audience = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)  # JSON list string
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
