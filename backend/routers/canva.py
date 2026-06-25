import os
import json
import base64
import hashlib
import secrets
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.db_models import User, OAuthToken
from routers.auth import get_current_user
from services.canva_mcp import CanvaMCPService
from services.ai import translate_content
from models.db_models import User, OAuthToken, AISettings

router = APIRouter(prefix="/api/canva", tags=["canva"])

class TranslateRequest(BaseModel):
    design_url: str
    target_language: str

@router.get("/status")
async def get_canva_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Kullanıcının Canva bağlantı durumunu döndürür."""
    token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.id,
        OAuthToken.platform == "canva"
    ).first()
    
    return {
        "connected": token is not None,
        "account_name": token.account_name if token else None
    }

@router.get("/auth/login")
async def canva_login(current_user: User = Depends(get_current_user)):
    """Canva OAuth akışını başlatır (PKCE Desteği ile)."""
    # Proje kök dizinindeki .env dosyasını yükle
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    
    client_id = os.environ.get("CANVA_CLIENT_ID")
    if not client_id:
        raise HTTPException(status_code=500, detail="CANVA_CLIENT_ID bulunamadı. Lütfen .env dosyasını kontrol edin.")
        
    redirect_uri = f"{os.environ.get('BACKEND_URL', 'http://localhost:8000')}/api/canva/auth/callback"
    
    # PKCE code_verifier ve code_challenge üretimi
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("ascii")).digest()
    ).decode("ascii").rstrip("=")
    
    # Güvenlik için state (normalde verifier ile eşleştirilip DB'de veya Cache'de tutulmalı)
    # Şimdilik kullanıcı id'si ve verifier'ı basitçe şifreli veya encode edilmiş bir state'te tutalım.
    state_payload = f"{current_user.id}:{code_verifier}"
    state = base64.urlsafe_b64encode(state_payload.encode()).decode()
    
    # Canva Connect API Authorization URL
    auth_url = (
        f"https://www.canva.com/api/oauth/authorize?"
        f"code_challenge_method=s256&"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"state={state}&"
        f"code_challenge={code_challenge}&"
        f"scope=design:read design:write"
    )
    return {"url": auth_url}

@router.get("/auth/callback")
async def canva_callback(code: str, state: str, db: Session = Depends(get_db)):
    """Canva OAuth dönüşünü işler ve PKCE token takasını yapar."""
    try:
        decoded_state = base64.urlsafe_b64decode(state).decode()
        user_id_str, code_verifier = decoded_state.split(":")
        user_id = int(user_id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz state parametresi.")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    # MOCK IMPLEMENTATION: Gerçekte token takası (code -> access_token) yapılır.
    mock_access_token = f"canva_mock_token_for_{code}"
    
    token_record = db.query(OAuthToken).filter(
        OAuthToken.user_id == user_id, 
        OAuthToken.platform == "canva"
    ).first()
    
    if not token_record:
        token_record = OAuthToken(
            user_id=user_id,
            platform="canva",
            access_token=mock_access_token,
            account_name="Canva User",
            account_id="canva_account_1"
        )
        db.add(token_record)
    else:
        token_record.access_token = mock_access_token
        
    db.commit()
    
    frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
    return RedirectResponse(url=f"{frontend_url}/create?canva_auth_success=1")

@router.post("/translate")
async def translate_canva_design(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Canva tasarımını okur, çevirir ve yeni bir tasarım URL'si döndürür."""
    token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.id,
        OAuthToken.platform == "canva"
    ).first()
    
    if not token:
        raise HTTPException(status_code=401, detail="Canva hesabı bağlı değil.")
        
    # AI çeviri adaptörü (Mevcut AI servisimizi kullanır)
    async def translate_func(text: str, target_lang: str) -> str:
        ai_settings_record = db.query(AISettings).filter(AISettings.user_id == current_user.id).first()
        ai_settings = {}
        if ai_settings_record:
            ai_settings = {
                "provider": ai_settings_record.provider,
                "model_name": ai_settings_record.model_name,
                "api_key": ai_settings_record.api_key
            }
            
        translated_text, _ = await translate_content(
            content=text, 
            hashtags=[], 
            target_language=target_lang, 
            ai_settings=ai_settings
        )
        return translated_text

    try:
        # MCP Servisini başlat
        mcp_service = CanvaMCPService(access_token=token.access_token)
        
        # Süreci çalıştır
        new_url = await mcp_service.translate_design(
            design_url=request.design_url, 
            target_language=request.target_language,
            translate_func=translate_func
        )
        
        return {
            "status": "success",
            "message": "Tasarım başarıyla çevrildi.",
            "original_url": request.design_url,
            "translated_url": new_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çeviri hatası: {str(e)}")
