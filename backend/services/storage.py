"""
MinIO depolama servisi.
Presigned URL oluşturma, bucket yönetimi ve dosya erişimi.
"""
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import logging
import uuid
from pathlib import Path

from config import get_settings

logger = logging.getLogger(__name__)


def get_s3_client():
    """MinIO S3 istemcisi döndürür."""
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def initialize_bucket():
    """
    Uygulama başlangıcında bucket'ı oluşturur (yoksa) ve
    24 saatlik lifecycle policy uygular.
    """
    settings = get_settings()
    s3 = get_s3_client()

    try:
        s3.head_bucket(Bucket=settings.MINIO_BUCKET_NAME)
        logger.info(f"Bucket '{settings.MINIO_BUCKET_NAME}' zaten var.")
    except ClientError:
        logger.info(f"Bucket '{settings.MINIO_BUCKET_NAME}' oluşturuluyor...")
        try:
            s3.create_bucket(Bucket=settings.MINIO_BUCKET_NAME)
            logger.info("Bucket oluşturuldu.")
        except Exception as e:
            logger.error(f"Bucket oluşturma hatası: {e}")
            return

    # Bucket varsa veya yeni oluşturulduysa her halükarda kuralları uygula
    try:
        # 24 saat sonra dosyaları sil
        lifecycle_config = {
            "Rules": [
                {
                    "ID": "auto-delete-24h",
                    "Filter": {"Prefix": ""},
                    "Status": "Enabled",
                    "Expiration": {"Days": 1},
                }
            ]
        }
        s3.put_bucket_lifecycle_configuration(
            Bucket=settings.MINIO_BUCKET_NAME,
            LifecycleConfiguration=lifecycle_config,
        )

        # CORS Policy (Frontend'in dosyaları doğrudan yükleyebilmesi için gerekli)
        cors_config = {
            'CORSRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'PUT', 'POST', 'HEAD'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': ['ETag']
                }
            ]
        }
        s3.put_bucket_cors(
            Bucket=settings.MINIO_BUCKET_NAME,
            CORSConfiguration=cors_config
        )

        logger.info("Lifecycle ve CORS poliçeleri başarıyla güncellendi.")
    except Exception as e:
        logger.error(f"Bucket policy/cors güncelleme hatası: {e}")


def generate_presigned_post(filename: str, content_type: str, expiration: int = 300):
    """
    Frontend'in doğrudan MinIO'ya yükleme yapabilmesi için
    presigned POST URL ve form alanları oluşturur.
    
    Returns: (upload_url, fields, object_key)
    """
    settings = get_settings()
    s3 = get_s3_client()

    # Benzersiz object key oluştur
    ext = Path(filename).suffix
    object_key = f"uploads/{uuid.uuid4().hex}{ext}"

    try:
        response = s3.generate_presigned_post(
            settings.MINIO_BUCKET_NAME,
            object_key,
            Fields={"Content-Type": content_type},
            Conditions=[
                {"Content-Type": content_type},
                ["content-length-range", 1, 500 * 1024 * 1024],  # Max 500MB
            ],
            ExpiresIn=expiration,
        )

        upload_url = response["url"]

        # Public URL ile değiştir (Cloudflare Tunnel vb.)
        if settings.MINIO_ENDPOINT != settings.minio_public_url:
            upload_url = upload_url.replace(
                settings.MINIO_ENDPOINT, settings.minio_public_url
            )

        return upload_url, response["fields"], object_key

    except ClientError as e:
        logger.error(f"Presigned POST hatası: {e}")
        raise


def generate_presigned_get(object_key: str, expiration: int = 3600) -> str:
    """
    MinIO'daki bir dosya için okuma/indirme URL'i oluşturur.
    Sosyal medya API'leri bu URL'den medyayı çeker.
    """
    settings = get_settings()
    s3 = get_s3_client()

    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.MINIO_BUCKET_NAME, "Key": object_key},
            ExpiresIn=expiration,
        )

        # Public URL ile değiştir
        if settings.MINIO_ENDPOINT != settings.minio_public_url:
            url = url.replace(settings.MINIO_ENDPOINT, settings.minio_public_url)

        return url

    except ClientError as e:
        logger.error(f"Presigned GET hatası: {e}")
        raise
