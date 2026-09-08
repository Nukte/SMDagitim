import base64
import hashlib
import secrets
import time
import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from config import get_settings
from database import get_db
from models.db_models import User, OAuthToken, AISettings
from routers.auth import get_current_user
from services.canva_mcp import CanvaMCPService
from services.ai import translate_content

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/canva", tags=["canva"])

# Kaynak: https://www.canva.dev/docs/connect/authentication/ (PKCE) ve
# https://www.canva.dev/docs/connect/api-reference/authentication/generate-access-token/
CANVA_AUTH_URL = "https://www.canva.com/api/oauth/authorize"
CANVA_TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"

# PKCE code_verifier'ları state ile eşleştirmek için process-local geçici depo.
# NOT: OAuth state store'daki aynı sınırlamayı taşır (bkz. PROJECT_ANALYSIS.md §2.1) —
# process-local, restart'ta kaybolur, yatay ölçeklemede instance'lar arası paylaşılmaz.
# key: state -> (timestamp, user_id, code_verifier)
_canva_pkce_store: dict[str, tuple[float, int, str]] = {}


class TranslateRequest(BaseModel):
    design_url: str
    target_language: str


def _basic_auth_header(client_id: str, client_secret: str) -> dict:
    raw = f"{client_id}:{client_secret}".encode()
    return {"Authorization": f"Basic {base64.b64encode(raw).decode()}"}


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
    settings = get_settings()

    if not settings.CANVA_CLIENT_ID:
        raise HTTPException(status_code=500, detail="CANVA_CLIENT_ID ayarlanmamış! Lütfen .env dosyasını kontrol edin.")

    redirect_uri = f"{settings.BACKEND_URL}/api/canva/auth/callback"

    # PKCE code_verifier ve code_challenge üretimi
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("ascii")).digest()
    ).decode("ascii").rstrip("=")

    # Eski PKCE kayıtlarını temizle (10 dakikadan eski)
    now = time.time()
    expired = [k for k, v in _canva_pkce_store.items() if now - v[0] > 600]
    for k in expired:
        _canva_pkce_store.pop(k, None)

    state = secrets.token_urlsafe(32)
    _canva_pkce_store[state] = (now, current_user.id, code_verifier)

    # Canva Connect API Authorization URL
    auth_url = (
        f"{CANVA_AUTH_URL}?"
        f"code_challenge_method=s256&"
        f"response_type=code&"
        f"client_id={settings.CANVA_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"state={state}&"
        f"code_challenge={code_challenge}&"
        f"scope=design:content:read design:content:write"
    )
    return {"url": auth_url}


@router.get("/auth/callback")
async def canva_callback(code: str, state: str, db: Session = Depends(get_db)):
    """Canva OAuth dönüşünü işler ve gerçek PKCE token takasını yapar."""
    settings = get_settings()

    state_data = _canva_pkce_store.pop(state, None)
    if not state_data:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/create?canva_auth_error=invalid_state"
        )

    state_time, user_id, code_verifier = state_data
    if time.time() - state_time > 600:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/create?canva_auth_error=expired_state"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    redirect_uri = f"{settings.BACKEND_URL}/api/canva/auth/callback"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            token_resp = await client.post(
                CANVA_TOKEN_URL,
                headers={
                    **_basic_auth_header(settings.CANVA_CLIENT_ID, settings.CANVA_CLIENT_SECRET),
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "code_verifier": code_verifier,
                    "redirect_uri": redirect_uri,
                },
            )
    except httpx.HTTPError as e:
        logger.error(f"[canva] Token takası isteği başarısız: {e}")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/create?canva_auth_error=network_error")

    if token_resp.status_code != 200:
        logger.error(f"[canva] Token takası reddedildi ({token_resp.status_code}): {token_resp.text}")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/create?canva_auth_error=token_exchange_failed")

    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in", 14400)  # Canva varsayılanı: 4 saat

    if not access_token:
        logger.error(f"[canva] Token yanıtında access_token yok: {token_data}")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/create?canva_auth_error=token_exchange_failed")

    expires_at = int(time.time()) + int(expires_in)

    token_record = db.query(OAuthToken).filter(
        OAuthToken.user_id == user_id,
        OAuthToken.platform == "canva"
    ).first()

    if not token_record:
        token_record = OAuthToken(
            user_id=user_id,
            platform="canva",
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            account_name="Canva",
            account_id=f"canva_user_{user_id}",
        )
        db.add(token_record)
    else:
        token_record.access_token = access_token
        token_record.refresh_token = refresh_token
        token_record.expires_at = expires_at

    db.commit()

    return RedirectResponse(url=f"{settings.FRONTEND_URL}/create?canva_auth_success=1")


async def _get_valid_canva_access_token(token_record: OAuthToken, db: Session) -> str:
    """
    Canva access token'ı kısa ömürlüdür (~4 saat). Süresi dolmuşsa/dolmak
    üzereyse refresh_token ile yeniler. Canva'da her refresh_token TEK
    KULLANIMLIKTIR — yenilenen refresh_token mutlaka DB'ye kaydedilmeli.
    """
    settings = get_settings()
    now = int(time.time())

    if token_record.expires_at and (token_record.expires_at - now) > 60:
        return token_record.access_token

    if not token_record.refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Canva oturumunun süresi dolmuş ve yenileme token'ı yok. Lütfen Canva hesabını yeniden bağlayın.",
        )

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            CANVA_TOKEN_URL,
            headers={
                **_basic_auth_header(settings.CANVA_CLIENT_ID, settings.CANVA_CLIENT_SECRET),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": token_record.refresh_token,
            },
        )

    if resp.status_code != 200:
        logger.error(f"[canva] Token yenileme başarısız ({resp.status_code}): {resp.text}")
        raise HTTPException(
            status_code=401,
            detail="Canva oturumu yenilenemedi. Lütfen hesabı yeniden bağlayın.",
        )

    data = resp.json()
    token_record.access_token = data["access_token"]
    token_record.refresh_token = data.get("refresh_token", token_record.refresh_token)
    token_record.expires_at = now + int(data.get("expires_in", 14400))
    db.commit()

    return token_record.access_token


@router.post("/translate")
async def translate_canva_design(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Canva tasarımını okur, çevirir ve yeni bir (kopya) tasarım URL'si döndürür."""
    token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.id,
        OAuthToken.platform == "canva"
    ).first()

    if not token:
        raise HTTPException(status_code=401, detail="Canva hesabı bağlı değil.")

    access_token = await _get_valid_canva_access_token(token, db)

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
        mcp_service = CanvaMCPService(access_token=access_token)
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[canva] Çeviri hatası: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Çeviri hatası: {str(e)}")
