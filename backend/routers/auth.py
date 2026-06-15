"""
Kimlik doğrulama router'ı.
Müşteriler için kayıt olma (Register) ve giriş yapma (Login) işlemlerini yönetir.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import get_settings
from database import get_db
from models.schemas import LoginRequest, TokenResponse, UserCreate, UserResponse, AppSettingsResponse
from models.db_models import User, AppSettings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """JWT token oluşturur."""
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """JWT token'dan kullanıcıyı doğrular ve User nesnesini döndürür."""
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulama yapılamadı",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token süresi dolmuş"
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Kullanıcı hesabı pasif",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Mevcut giriş yapmış kullanıcının bilgilerini döndürür."""
    return current_user

@router.get("/public-settings")
async def get_public_settings(db: Session = Depends(get_db)):
    """Kayıt dışarıya açık mı vb. bilgileri döner."""
    settings = db.query(AppSettings).first()
    registration_enabled = settings.registration_enabled if settings else True
    return {"registration_enabled": registration_enabled}


@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Yeni müşteri kaydı oluşturur."""
    app_settings = db.query(AppSettings).first()
    if app_settings and not app_settings.registration_enabled:
        raise HTTPException(
            status_code=403,
            detail="Şu an yeni üye alımı kapalıdır."
        )

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Bu e-posta adresi sistemde zaten kayıtlı."
        )
    
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    E-posta ve şifre ile giriş yapar.
    Başarılı girişte JWT token döndürür.
    """
    settings = get_settings()

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta veya şifre hatalı"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hesabınız pasife alınmıştır. Lütfen yönetici ile iletişime geçin."
        )

    expire_delta = timedelta(hours=settings.JWT_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=expire_delta
    )

    return TokenResponse(
        access_token=access_token,
        expires_in=settings.JWT_EXPIRE_HOURS * 3600
    )
