"""
Kimlik doğrulama router'ı.
Sabit admin kullanıcı/şifre ile JWT token üretir. Kayıt olma özelliği yok.
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
import hmac

from config import get_settings
from models.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """JWT token oluşturur."""
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """JWT token'ı doğrular ve payload döndürür."""
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token süresi dolmuş"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz token"
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Sabit admin kullanıcı adı/şifre ile giriş yapar.
    Başarılı girişte JWT token döndürür.
    """
    settings = get_settings()

    if not (hmac.compare_digest(request.username, settings.ADMIN_USERNAME) and 
            hmac.compare_digest(request.password, settings.ADMIN_PASSWORD)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı"
        )

    expire_delta = timedelta(hours=settings.JWT_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": request.username},
        expires_delta=expire_delta
    )

    return TokenResponse(
        access_token=access_token,
        expires_in=settings.JWT_EXPIRE_HOURS * 3600
    )
