from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import db_models, schemas
from services.ai import generate_ai_content, analyze_brand_file

router = APIRouter(prefix="/api/ai", tags=["AI"])

@router.get("/settings", response_model=schemas.AISettingsSchema)
def get_ai_settings(db: Session = Depends(get_db)):
    settings = db.query(db_models.AISettings).first()
    if not settings:
        return schemas.AISettingsSchema()
    return schemas.AISettingsSchema(
        provider=settings.provider,
        model_name=settings.model_name,
        api_key=settings.api_key
    )

@router.post("/settings", response_model=schemas.AISettingsSchema)
def update_ai_settings(settings_in: schemas.AISettingsSchema, db: Session = Depends(get_db)):
    settings = db.query(db_models.AISettings).first()
    if not settings:
        settings = db_models.AISettings()
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
        api_key=settings.api_key
    )

@router.get("/brand", response_model=schemas.BrandProfileSchema)
def get_brand_profile(db: Session = Depends(get_db)):
    brand = db.query(db_models.BrandProfile).first()
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
def update_brand_profile(brand_in: schemas.BrandProfileSchema, db: Session = Depends(get_db)):
    brand = db.query(db_models.BrandProfile).first()
    if not brand:
        brand = db_models.BrandProfile()
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
async def generate_content(request: schemas.AIGenerateRequest, db: Session = Depends(get_db)):
    settings = db.query(db_models.AISettings).first()
    brand = db.query(db_models.BrandProfile).first()
    
    if not settings or not settings.api_key:
        raise HTTPException(status_code=400, detail="AI Ayarları veya API Key eksik.")
        
    ai_settings = {
        "provider": settings.provider,
        "model_name": settings.model_name,
        "api_key": settings.api_key
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
async def api_analyze_brand_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    settings = db.query(db_models.AISettings).first()
    if not settings or not settings.api_key:
        raise HTTPException(status_code=400, detail="AI Ayarları veya API Key eksik.")
        
    ai_settings = {
        "provider": settings.provider,
        "model_name": settings.model_name,
        "api_key": settings.api_key
    }
    
    try:
        content = await file.read()
        result = await analyze_brand_file(content, file.filename, ai_settings)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya analiz edilirken bilinmeyen bir hata oluştu: {str(e)}")
