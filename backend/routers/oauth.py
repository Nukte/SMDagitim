"""
OAuth yetkilendirme router'ı.
Her sosyal medya platformu için OAuth akışını yönetir.
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
import urllib.parse
import httpx
import logging
import secrets
import time

from database import get_db
from models.db_models import OAuthToken
from models.schemas import ConnectedAccount, OAuthStatusResponse, PlatformName, AccountSettingsUpdate
from config import get_settings
from routers.auth import verify_token

logger = logging.getLogger(__name__)

# OAuth CSRF state store (basit in-memory, tek sunucu için yeterli)
_oauth_states: dict[str, float] = {}

router = APIRouter(prefix="/api/oauth", tags=["OAuth"])


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Geçersiz yetkilendirme başlığı")
    token = authorization.split(" ")[1]
    return verify_token(token)


@router.get("/status", response_model=OAuthStatusResponse)
async def get_oauth_status(
    _user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Tüm bağlı hesapların durumunu döndürür."""
    token_records = db.query(OAuthToken).all()
    accounts = []
    for record in token_records:
        accounts.append(ConnectedAccount(
            id=record.id,
            platform=PlatformName(record.platform),
            account_id=record.account_id,
            account_name=record.account_name,
            country=record.country,
            target_language=record.target_language
        ))

    return OAuthStatusResponse(accounts=accounts)


@router.put("/account/{account_id}")
async def update_account_settings(
    account_id: str,
    settings: AccountSettingsUpdate,
    _user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token_record = db.query(OAuthToken).filter(OAuthToken.account_id == account_id).first()
    if not token_record:
        raise HTTPException(status_code=404, detail="Hesap bulunamadı")
        
    token_record.country = settings.country
    token_record.target_language = settings.target_language
        
    db.commit()
    return {"message": "Hesap güncellendi"}


@router.delete("/account/{account_id}/disconnect")
async def disconnect_account(
    account_id: str,
    _user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Bir hesabın bağlantısını keser."""
    db_token = db.query(OAuthToken).filter(OAuthToken.account_id == account_id).first()
    if db_token:
        db.delete(db_token)
        db.commit()
    return {"message": "Hesap bağlantısı kesildi."}


@router.get("/{platform}/login")
async def oauth_login(platform: str):
    """Kullanıcıyı platformun OAuth yetkilendirme sayfasına yönlendirir."""
    settings = get_settings()

    # Eski state'leri temizle (10 dakikadan eski)
    current_time = time.time()
    expired = [k for k, v in _oauth_states.items() if current_time - v > 600]
    for k in expired:
        _oauth_states.pop(k, None)

    # Yeni state oluştur
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = time.time()

    if platform in ["facebook", "instagram"]:
        app_id = settings.META_CLIENT_ID
        if not app_id:
            raise HTTPException(status_code=500, detail="META_CLIENT_ID ayarlanmamış!")

        redirect_uri = f"{settings.BACKEND_URL}/api/oauth/{platform}/callback"
        scopes = "instagram_basic,instagram_content_publish,pages_read_engagement,pages_show_list,business_management,public_profile"

        auth_url = (
            f"https://www.facebook.com/v19.0/dialog/oauth"
            f"?client_id={app_id}"
            f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
            f"&scope={urllib.parse.quote(scopes)}"
            f"&response_type=code"
            f"&state={state}"
        )
        return RedirectResponse(url=auth_url)

    elif platform == "twitter":
        raise HTTPException(
            status_code=501,
            detail="Twitter OAuth henüz aktif değil. Developer hesabı oluşturulması gerekiyor."
        )

    elif platform == "linkedin":
        client_id = settings.LINKEDIN_CLIENT_ID
        if not client_id:
            raise HTTPException(status_code=500, detail="LINKEDIN_CLIENT_ID ayarlanmamış!")

        redirect_uri = f"{settings.BACKEND_URL}/api/oauth/linkedin/callback"
        scopes = "openid profile w_member_social"

        auth_url = (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
            f"&scope={urllib.parse.quote(scopes)}"
            f"&state={state}"
        )
        return RedirectResponse(url=auth_url)

    else:
        raise HTTPException(status_code=404, detail="Geçersiz platform.")


@router.get("/{platform}/callback")
async def oauth_callback(
    platform: str,
    db: Session = Depends(get_db),
    code: str = None,
    error: str = None,
    error_description: str = None,
    state: str = None,
):
    """Platformdan dönen code'u access_token'a çevirir ve kaydeder."""
    settings = get_settings()

    # OAuth hata durumu (kullanıcı izin vermedi veya başka bir hata)
    if error or not code:
        error_msg = error_description or error or "Yetkilendirme kodu alınamadı"
        logger.error(f"[{platform}] OAuth hatası: {error_msg}")
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/?auth_error={urllib.parse.quote(error_msg)}"
        )

    # CSRF state doğrulaması
    if not state or state not in _oauth_states:
        logger.warning(f"[{platform}] Geçersiz OAuth state parametresi")
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/?auth_error={urllib.parse.quote('Geçersiz yetkilendirme isteği (CSRF koruması)')}"
        )
    
    # State'i kullan ve sil (tek kullanımlık)
    state_time = _oauth_states.pop(state, 0)
    # 10 dakikadan eski state'leri reddet
    if time.time() - state_time > 600:
        logger.warning(f"[{platform}] Süresi dolmuş OAuth state")
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/?auth_error={urllib.parse.quote('Yetkilendirme süresi doldu, lütfen tekrar deneyin')}"
        )

    accounts_to_save = []

    if platform in ["facebook", "instagram"]:
        app_id = settings.META_CLIENT_ID
        app_secret = settings.META_CLIENT_SECRET
        redirect_uri = f"{settings.BACKEND_URL}/api/oauth/{platform}/callback"

        # Code → Access Token
        async with httpx.AsyncClient() as client:
            token_resp = await client.get(
                "https://graph.facebook.com/v19.0/oauth/access_token",
                params={
                    "client_id": app_id,
                    "client_secret": app_secret,
                    "redirect_uri": redirect_uri,
                    "code": code,
                },
            )
            if token_resp.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Meta token alınamadı: {token_resp.text}")

            token_data = token_resp.json()
            access_token = token_data.get("access_token")

            if platform == "instagram":
                # Facebook sayfalarını al
                pages_resp = await client.get(
                    f"https://graph.facebook.com/v19.0/me/accounts",
                    params={"access_token": access_token},
                )
                pages_data = pages_resp.json()
                pages = pages_data.get("data", [])

                for page in pages:
                    page_token = page.get("access_token")
                    page_id = page.get("id")

                    # Sayfaya bağlı Instagram hesabını bul
                    ig_resp = await client.get(
                        f"https://graph.facebook.com/v19.0/{page_id}",
                        params={
                            "fields": "instagram_business_account",
                            "access_token": page_token,
                        },
                    )
                    ig_data = ig_resp.json()
                    ig_account = ig_data.get("instagram_business_account", {})
                    account_id = ig_account.get("id")

                    if account_id:
                        # IG kullanıcı adını al
                        ig_info = await client.get(
                            f"https://graph.facebook.com/v19.0/{account_id}",
                            params={
                                "fields": "username",
                                "access_token": page_token,
                            },
                        )
                        ig_info_data = ig_info.json()
                        account_name = ig_info_data.get("username")
                        
                        accounts_to_save.append({
                            "platform": platform,
                            "account_id": account_id,
                            "account_name": account_name,
                            "access_token": page_token
                        })

            elif platform == "facebook":
                # Facebook sayfası bilgilerini al
                pages_resp = await client.get(
                    f"https://graph.facebook.com/v19.0/me/accounts",
                    params={"access_token": access_token},
                )
                pages_data = pages_resp.json()
                pages = pages_data.get("data", [])
                for page in pages:
                    account_id = page.get("id")
                    account_name = page.get("name")
                    page_token = page.get("access_token")
                    accounts_to_save.append({
                        "platform": platform,
                        "account_id": account_id,
                        "account_name": account_name,
                        "access_token": page_token
                    })

    elif platform == "linkedin":
        client_id = settings.LINKEDIN_CLIENT_ID
        client_secret = settings.LINKEDIN_CLIENT_SECRET
        redirect_uri = f"{settings.BACKEND_URL}/api/oauth/linkedin/callback"

        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                "https://www.linkedin.com/oauth/v2/accessToken",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                },
            )
            if token_resp.status_code != 200:
                raise HTTPException(status_code=400, detail=f"LinkedIn token alınamadı: {token_resp.text}")

            token_data = token_resp.json()
            access_token = token_data.get("access_token")
            account_id = None
            account_name = None

            # Person ID'yi al
            id_token = token_data.get("id_token")
            if id_token:
                try:
                    import json, base64
                    payload = id_token.split(".")[1]
                    payload += "=" * (4 - len(payload) % 4)
                    decoded = json.loads(base64.urlsafe_b64decode(payload))
                    account_id = decoded.get("sub")
                    account_name = decoded.get("name")
                except Exception as e:
                    pass

            if not account_id:
                userinfo_resp = await client.get(
                    "https://api.linkedin.com/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if userinfo_resp.status_code == 200:
                    profile = userinfo_resp.json()
                    account_id = profile.get("sub")
                    account_name = profile.get("name")

            if not account_id:
                me_resp = await client.get(
                    "https://api.linkedin.com/v2/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if me_resp.status_code == 200:
                    profile = me_resp.json()
                    account_id = profile.get("id")
                    first_name = profile.get("localizedFirstName", "")
                    last_name = profile.get("localizedLastName", "")
                    account_name = f"{first_name} {last_name}".strip() or None

            if account_id:
                accounts_to_save.append({
                    "platform": platform,
                    "account_id": account_id,
                    "account_name": account_name,
                    "access_token": access_token
                })

    else:
        raise HTTPException(status_code=404, detail="Geçersiz platform.")

    if not accounts_to_save:
         return RedirectResponse(url=f"{settings.FRONTEND_URL}/?auth_error={urllib.parse.quote('Hesap bilgileri alınamadı.')}")

    # Hesapları DB'ye kaydet
    for acc in accounts_to_save:
        db_token = db.query(OAuthToken).filter(
            OAuthToken.platform == acc["platform"],
            OAuthToken.account_id == acc["account_id"]
        ).first()
        
        if not db_token:
            db_token = OAuthToken(
                platform=acc["platform"],
                access_token=acc["access_token"],
                account_id=acc["account_id"],
                account_name=acc["account_name"],
            )
            db.add(db_token)
        else:
            db_token.access_token = acc["access_token"]
            db_token.account_name = acc["account_name"]

    db.commit()

    # Frontend'e yönlendir
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/?auth_success={platform}")
