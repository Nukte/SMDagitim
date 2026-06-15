from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import (
    PresignedUrlRequest,
    PresignedUrlResponse,
    UploadConfirmRequest,
    UploadConfirmResponse,
)
from services.storage import generate_presigned_post, generate_presigned_get
from routers.auth import get_current_user
from models.db_models import User

router = APIRouter(prefix="/api/upload", tags=["Upload"])

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
