from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import db_models, schemas
from services.ai import generate_ai_content, analyze_brand_file
from routers.auth import get_current_user

router = APIRouter(prefix="/api/ai", tags=["AI"])

def _mask_api_key(key: Optional[str]) -> str:
    """API key'i maskeler. Sadece son 4 karakteri gösterir."""
    if not key or len(key) < 8:
        return "****" if key else ""
    return "*" * (len(key) - 4) + key[-4:]

@router.get("/settings", response_model=schemas.AISettingsSchema)
def get_ai_settings(db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    settings = db.query(db_models.AISettings).filter(db_models.AISettings.user_id == current_user.id).first()
    if not settings:
        return schemas.AISettingsSchema()
    return schemas.AISettingsSchema(
        provider=settings.provider,
        model_name=settings.model_name,
        api_key=_mask_api_key(settings.api_key)
    )

@router.post("/settings", response_model=schemas.AISettingsSchema)
def update_ai_settings(settings_in: schemas.AISettingsSchema, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    settings = db.query(db_models.AISettings).filter(db_models.AISettings.user_id == current_user.id).first()
    if not settings:
        settings = db_models.AISettings(user_id=current_user.id)
        db.add(settings)
    
    settings.provider = settings_in.provider
    settings.model_name = settings_in.model_name
    if settings_in.api_key:
        settings.api_key = settings_in.api_key
        
    db.commit()
    db.refresh(settings)
    return schemas.AISettingsSchema(
        provider=settings.provider,
        model_name=settings.model_name,
        api_key=_mask_api_key(settings.api_key)
    )

@router.get("/brand", response_model=schemas.BrandProfileSchema)
def get_brand_profile(db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    brand = db.query(db_models.BrandProfile).filter(db_models.BrandProfile.user_id == current_user.id).first()
    if not brand:
        return schemas.BrandProfileSchema()
        
    import json
    keywords = []
    if brand.keywords:
        try:
            keywords = json.loads(brand.keywords)
        except:
            pass
            
    return schemas.BrandProfileSchema(
        brand_name=brand.brand_name,
        tone=brand.tone,
        target_audience=brand.target_audience,
        keywords=keywords
    )

@router.post("/brand", response_model=schemas.BrandProfileSchema)
def update_brand_profile(brand_in: schemas.BrandProfileSchema, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    brand = db.query(db_models.BrandProfile).filter(db_models.BrandProfile.user_id == current_user.id).first()
    if not brand:
        brand = db_models.BrandProfile(user_id=current_user.id)
        db.add(brand)
        
    brand.brand_name = brand_in.brand_name
    brand.tone = brand_in.tone
    brand.target_audience = brand_in.target_audience
    
    import json
    if brand_in.keywords is not None:
        brand.keywords = json.dumps(brand_in.keywords)
        
    db.commit()
    db.refresh(brand)
    
    return brand_in

@router.post("/generate", response_model=schemas.AIGenerateResponse)
async def generate_content(request: schemas.AIGenerateRequest, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    user_settings = db.query(db_models.AISettings).filter(db_models.AISettings.user_id == current_user.id).first()
    app_settings = db.query(db_models.AppSettings).first()
    brand = db.query(db_models.BrandProfile).filter(db_models.BrandProfile.user_id == current_user.id).first()
    
    provider = user_settings.provider if user_settings else (app_settings.global_ai_provider if app_settings else "gemini")
    model_name = user_settings.model_name if user_settings else (app_settings.global_ai_model if app_settings else "gemini-2.5-flash")
    api_key = user_settings.api_key if user_settings and user_settings.api_key else (app_settings.global_ai_api_key if app_settings else None)

    if not api_key:
        raise HTTPException(status_code=400, detail="AI Ayarları veya API Key eksik. Lütfen ayarlardan API anahtarınızı girin.")
        
    ai_settings = {
        "provider": provider,
        "model_name": model_name,
        "api_key": api_key
    }
    
    import json
    keywords = []
    if brand and brand.keywords:
        try:
            keywords = json.loads(brand.keywords)
        except:
            pass
            
    brand_profile = {
        "brand_name": brand.brand_name if brand else "",
        "tone": brand.tone if brand else "",
        "target_audience": brand.target_audience if brand else "",
        "keywords": keywords
    }
    
    try:
        content, hashtags, media_url, media_key = await generate_ai_content(
            topic=request.topic,
            generate_image=request.generate_image,
            brand_profile=brand_profile,
            ai_settings=ai_settings
        )
        return schemas.AIGenerateResponse(
            content=content,
            hashtags=hashtags,
            media_url=media_url,
            media_key=media_key
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="İçerik üretilirken bilinmeyen bir hata oluştu.")

@router.post("/analyze-brand-file")
async def api_analyze_brand_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    user_settings = db.query(db_models.AISettings).filter(db_models.AISettings.user_id == current_user.id).first()
    app_settings = db.query(db_models.AppSettings).first()

    provider = user_settings.provider if user_settings else (app_settings.global_ai_provider if app_settings else "gemini")
    model_name = user_settings.model_name if user_settings else (app_settings.global_ai_model if app_settings else "gemini-2.5-flash")
    api_key = user_settings.api_key if user_settings and user_settings.api_key else (app_settings.global_ai_api_key if app_settings else None)

    if not api_key:
        raise HTTPException(status_code=400, detail="AI Ayarları veya API Key eksik. Lütfen ayarlardan API anahtarınızı girin.")
        
    ai_settings = {
        "provider": provider,
        "model_name": model_name,
        "api_key": api_key
    }
    
    try:
        # Dosya boyutu kontrolü (max 10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Dosya boyutu 10MB'dan büyük olamaz.")
            
        result = await analyze_brand_file(content, file.filename, ai_settings)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Dosya analiz edilirken bilinmeyen bir hata oluştu.")
