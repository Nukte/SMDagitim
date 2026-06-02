"""
Dosya yükleme router'ı.
Presigned URL oluşturma ve yükleme onaylama endpoint'leri.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header

from models.schemas import (
    PresignedUrlRequest,
    PresignedUrlResponse,
    UploadConfirmRequest,
    UploadConfirmResponse,
)
from services.storage import generate_presigned_post, generate_presigned_get
from routers.auth import verify_token

router = APIRouter(prefix="/api/upload", tags=["Upload"])


def get_current_user(authorization: str = Header(...)):
    """JWT token'dan kullanıcıyı doğrular."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Geçersiz yetkilendirme başlığı")
    token = authorization.split(" ")[1]
    return verify_token(token)


@router.post("/presign", response_model=PresignedUrlResponse)
async def get_presigned_url(
    request: PresignedUrlRequest,
    _user: dict = Depends(get_current_user),
):
    """
    Adım 1 & 2: Frontend dosya yüklemek istediğinde,
    MinIO'ya doğrudan yükleme için presigned POST URL döndürür.
    """
    try:
        upload_url, fields, object_key = generate_presigned_post(
            request.filename, request.content_type
        )

        # Public okuma URL'ini de hesapla
        public_url = generate_presigned_get(object_key, expiration=86400)

        return PresignedUrlResponse(
            upload_url=upload_url,
            upload_fields=fields,
            object_key=object_key,
            public_url=public_url,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Presigned URL oluşturulamadı: {str(e)}",
        )


@router.post("/confirm", response_model=UploadConfirmResponse)
async def confirm_upload(
    request: UploadConfirmRequest,
    _user: dict = Depends(get_current_user),
):
    """
    Adım 4: Frontend MinIO'ya yüklemeyi tamamladığında,
    object_key'i onaylar ve public URL döndürür.
    """
    # Medya tipini belirle
    media_type = "video" if request.content_type.startswith("video/") else "image"

    # Yeni bir okuma URL'i oluştur (sosyal medya platformları için)
    public_url = generate_presigned_get(request.object_key, expiration=86400)

    return UploadConfirmResponse(
        object_key=request.object_key,
        public_url=public_url,
        media_type=media_type,
    )
