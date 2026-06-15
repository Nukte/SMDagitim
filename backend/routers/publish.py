from fastapi import APIRouter, Depends, HTTPException
import asyncio
import uuid
import logging

from models.schemas import (
    PublishRequest,
    PublishResponse,
    PlatformPublishStatus,
    PlatformName,
)
from routers.auth import get_current_user
from database import SessionLocal, get_db
from models.db_models import OAuthToken, AISettings, User
from sqlalchemy.orm import Session
from services.platforms.instagram import InstagramPublisher
from services.platforms.facebook import FacebookPublisher
from services.platforms.twitter import TwitterPublisher
from services.platforms.linkedin import LinkedInPublisher
from services.ai import translate_content

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/publish", tags=["Publishing"])

# In-memory job status tracking
job_statuses: dict[str, list[PlatformPublishStatus]] = {}

# Platform publisher instances
PUBLISHERS = {
    PlatformName.instagram.value: InstagramPublisher(),
    PlatformName.facebook.value: FacebookPublisher(),
    PlatformName.twitter.value: TwitterPublisher(),
    PlatformName.linkedin.value: LinkedInPublisher(),
}

async def publish_to_single_account(
    job_id: str,
    account_id: str,
    request: PublishRequest,
    user_id: int
):
    """Tek bir hesaba asenkron paylaşım yapar."""
    for p in job_statuses.get(job_id, []):
        if p.account_id == account_id:
            p.status = "publishing"

    try:
        db = SessionLocal()
        try:
            token_record = db.query(OAuthToken).filter(
                OAuthToken.account_id == account_id,
                OAuthToken.user_id == user_id
            ).first()

            if not token_record:
                raise Exception(f"{account_id} ID'li hesap bulunamadı veya bağlı değil.")

            access_token = token_record.access_token
            real_account_id = token_record.account_id
            platform_val = token_record.platform
            target_language = token_record.target_language
            
            content = request.content
            hashtags = request.hashtags
            
            if target_language:
                ai_settings_record = db.query(AISettings).filter(AISettings.user_id == user_id).first()
                if ai_settings_record and ai_settings_record.api_key:
                    ai_settings = {
                        "provider": ai_settings_record.provider,
                        "model_name": ai_settings_record.model_name,
                        "api_key": ai_settings_record.api_key
                    }
                    content, hashtags = await translate_content(content, hashtags, target_language, ai_settings)
                    
        finally:
            db.close()

        publisher = PUBLISHERS.get(platform_val)
        if not publisher:
            raise Exception(f"Desteklenmeyen platform: {platform_val}")

        result = await publisher.publish(
            content=content,
            hashtags=hashtags,
            media=request.media,
            access_token=access_token,
            account_id=real_account_id,
        )

        for p in job_statuses.get(job_id, []):
            if p.account_id == account_id:
                p.status = "success"
                p.post_id = result.get("post_id")
                p.post_url = result.get("post_url")

    except Exception as e:
        logger.error(f"[{account_id}] Paylaşım hatası: {e}")
        for p in job_statuses.get(job_id, []):
            if p.account_id == account_id:
                p.status = "error"
                p.error_message = str(e)


@router.post("", response_model=PublishResponse)
async def publish_post(
    request: PublishRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Seçilen hesaplara asenkron paylaşım başlatır."""
    job_id = f"{current_user.id}_{uuid.uuid4()}"

    initial_statuses = []
    
    for acc_id in request.account_ids:
        token_record = db.query(OAuthToken).filter(
            OAuthToken.account_id == acc_id,
            OAuthToken.user_id == current_user.id
        ).first()
        platform_name = PlatformName(token_record.platform) if token_record else PlatformName.instagram
        initial_statuses.append(
            PlatformPublishStatus(account_id=acc_id, platform=platform_name, status="pending")
        )
        
    job_statuses[job_id] = initial_statuses

    for acc_id in request.account_ids:
        asyncio.create_task(
            publish_to_single_account(job_id, acc_id, request, current_user.id)
        )

    return PublishResponse(job_id=job_id, platforms=initial_statuses)


@router.get("/{job_id}", response_model=PublishResponse)
async def get_publish_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
):
    """Paylaşım durumunu sorgular (polling ile)."""
    if not job_id.startswith(f"{current_user.id}_"):
        raise HTTPException(status_code=403, detail="Erişim reddedildi")
        
    statuses = job_statuses.get(job_id)
    if statuses is None:
        raise HTTPException(status_code=404, detail="İş bulunamadı")

    return PublishResponse(job_id=job_id, platforms=statuses)
