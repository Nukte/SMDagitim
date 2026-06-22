from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from models.schemas import (
    PresignedUrlRequest,
    PresignedUrlResponse,
    UploadConfirmRequest,
    UploadConfirmResponse,
)
from services.storage import generate_presigned_post, generate_presigned_get, upload_file_to_storage
from routers.auth import get_current_user
from models.db_models import User
import os
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("/direct", response_model=UploadConfirmResponse)
async def upload_direct(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Dosyayı backend üzerinden doğrudan MinIO'ya yükler.
    (Presigned URL sorunlarına alternatif garanti yöntem)
    """
    try:
        content_type = file.content_type
        media_type = "video" if content_type and content_type.startswith("video/") else "image"
        
        # Dosya uzantısını al
        ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
        
        # Dosyayı oku
        file_bytes = await file.read()
        
        # Storage servisini kullanarak yükle
        public_url, object_key = upload_file_to_storage(file_bytes, content_type or "application/octet-stream", ext)
        
        return UploadConfirmResponse(
            object_key=object_key,
            public_url=public_url,
            media_type=media_type,
        )
    except Exception as e:
        logger.error(f"Doğrudan yükleme hatası: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dosya yüklenemedi: {str(e)}",
        )


@router.post("/presign", response_model=PresignedUrlResponse)
async def get_presigned_url(
    request: PresignedUrlRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Adım 1 & 2: Frontend dosya yüklemek istediğinde,
    MinIO'ya doğrudan yükleme için presigned POST URL döndürür.
    """
    try:
        # Dosya adını izole et (tenant başına klasör)
        import os
        safe_filename = os.path.basename(request.filename)
        prefixed_filename = f"user_{current_user.id}/{safe_filename}"
        
        upload_url, fields, object_key = generate_presigned_post(
            prefixed_filename, request.content_type
        )

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
    current_user: User = Depends(get_current_user),
):
    """
    Adım 4: Frontend MinIO'ya yüklemeyi tamamladığında,
    object_key'i onaylar ve public URL döndürür.
    """
    if not request.object_key.startswith(f"user_{current_user.id}/"):
        raise HTTPException(status_code=403, detail="Geçersiz dosya anahtarı")
        
    media_type = "video" if request.content_type.startswith("video/") else "image"
    public_url = generate_presigned_get(request.object_key, expiration=86400)

    return UploadConfirmResponse(
        object_key=request.object_key,
        public_url=public_url,
        media_type=media_type,
    )
