"""
Pydantic şemaları — API request/response modelleri.
"""
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List, Optional, Literal
from enum import Enum


# ── Enums ──

class PlatformName(str, Enum):
    instagram = "instagram"
    facebook = "facebook"
    twitter = "twitter"
    linkedin = "linkedin"


# ── Auth ──

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ── Upload ──

class PresignedUrlRequest(BaseModel):
    filename: str = Field(..., description="Yüklenecek dosyanın adı")
    content_type: str = Field(..., description="Dosyanın MIME tipi (image/jpeg, video/mp4 vb.)")


class PresignedUrlResponse(BaseModel):
    upload_url: str
    upload_fields: dict
    object_key: str
    public_url: str


class UploadConfirmRequest(BaseModel):
    object_key: str = Field(..., description="MinIO'daki dosya yolu")
    content_type: str


class UploadConfirmResponse(BaseModel):
    object_key: str
    public_url: str
    media_type: str  # image veya video


# ── Media ──

class MediaItem(BaseModel):
    url: str
    object_key: str
    type: Literal["image", "video"]


# ── Publish ──

class PublishRequest(BaseModel):
    content: str = Field(default="", max_length=63206, description="Gönderi metni")
    hashtags: List[str] = Field(default=[], description="Etiketler")
    media: List[MediaItem] = Field(default=[], description="Medya dosyaları")
    account_ids: List[str] = Field(..., min_length=1, description="Paylaşım yapılacak hesap ID'leri")


class PlatformPublishStatus(BaseModel):
    account_id: str
    platform: PlatformName
    status: Literal["pending", "publishing", "success", "error"] = "pending"
    error_message: Optional[str] = None
    post_id: Optional[str] = None
    post_url: Optional[str] = None


class PublishResponse(BaseModel):
    job_id: str
    platforms: List[PlatformPublishStatus]


# ── OAuth ──

class ConnectedAccount(BaseModel):
    id: int
    platform: PlatformName
    account_id: str
    account_name: Optional[str] = None
    country: Optional[str] = None
    target_language: Optional[str] = None


class OAuthStatusResponse(BaseModel):
    accounts: List[ConnectedAccount]


class AccountSettingsUpdate(BaseModel):
    country: Optional[str] = None
    target_language: Optional[str] = None


# ── AI Module ──

class AISettingsSchema(BaseModel):
    provider: str = Field(default="gemini")
    model_name: str = Field(default="gemini-2.5-flash")
    api_key: Optional[str] = None

class BrandProfileSchema(BaseModel):
    brand_name: Optional[str] = None
    tone: Optional[str] = None
    target_audience: Optional[str] = None
    keywords: Optional[List[str]] = Field(default_factory=list)

class AIGenerateRequest(BaseModel):
    topic: str = Field(..., description="İçerik konusu")
    generate_image: bool = Field(default=True, description="Görsel üretilsin mi?")

class AIGenerateResponse(BaseModel):
    content: str
    hashtags: List[str]
    media_url: Optional[str] = None
    media_key: Optional[str] = None
