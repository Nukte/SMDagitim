from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.db_models import User, AppSettings
from models.schemas import UserResponse, UserUpdate, AppSettingsResponse, AppSettingsUpdate
from routers.auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Mevcut kullanıcının admin olup olmadığını kontrol eder."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlem için yönetici yetkisi gereklidir."
        )
    return current_user


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """Tüm kullanıcıları listeler."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """Kullanıcının durumunu (aktiflik, adminlik) günceller."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    # Kendi yetkilerini ve aktiflik durumunu değiştiremez
    if user_id == admin_user.id:
        if user_update.is_superuser is False:
            raise HTTPException(status_code=400, detail="Kendi admin yetkinizi kaldıramazsınız.")
        if user_update.is_active is False:
            raise HTTPException(status_code=400, detail="Kendi hesabınızı pasife alamazsınız.")
        
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.is_superuser is not None:
        user.is_superuser = user_update.is_superuser
        
    db.commit()
    db.refresh(user)
    return user


@router.get("/settings", response_model=AppSettingsResponse)
async def get_app_settings(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """Genel uygulama ayarlarını getirir."""
    settings = db.query(AppSettings).first()
    if not settings:
        settings = AppSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.put("/settings", response_model=AppSettingsResponse)
async def update_app_settings(
    settings_update: AppSettingsUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """Genel uygulama ayarlarını günceller."""
    settings = db.query(AppSettings).first()
    if not settings:
        settings = AppSettings()
        db.add(settings)
    
    if settings_update.registration_enabled is not None:
        settings.registration_enabled = settings_update.registration_enabled
    if settings_update.global_ai_provider is not None:
        settings.global_ai_provider = settings_update.global_ai_provider
    if settings_update.global_ai_model is not None:
        settings.global_ai_model = settings_update.global_ai_model
    if settings_update.global_ai_api_key is not None:
        settings.global_ai_api_key = settings_update.global_ai_api_key
        
    db.commit()
    db.refresh(settings)
    return settings
