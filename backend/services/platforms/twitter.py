"""
X / Twitter API v2 Publisher.
Tweet oluşturma ve medya yükleme.
Şu an mock implementasyon — developer hesabı oluşturulunca gerçek API'ye geçilecek.
"""
import asyncio
import logging
from typing import Optional, List

from models.schemas import MediaItem
from services.platforms.base import BasePlatformPublisher

logger = logging.getLogger(__name__)


class TwitterPublisher(BasePlatformPublisher):
    platform_name = "twitter"

    async def publish(
        self,
        content: str,
        hashtags: List[str],
        media: List[MediaItem],
        access_token: str,
        account_id: Optional[str] = None,
    ) -> dict:
        """
        X/Twitter'a tweet gönderir.
        
        TODO: Developer hesabı oluşturulunca gerçek implementasyon:
        1. Media upload: POST https://upload.twitter.com/1.1/media/upload.json
        2. Tweet create: POST https://api.twitter.com/2/tweets
        """
        caption = self.build_caption(content, hashtags)

        # Twitter'da 280 karakter limiti
        if len(caption) > 280:
            caption = caption[:277] + "..."

        logger.info(f"[twitter] Tweet gönderiliyor: {caption[:50]}...")
        await asyncio.sleep(1)  # Mock gecikme

        # Mock response
        return {
            "post_id": "mock_tweet_id_12345",
            "post_url": "https://x.com/user/status/mock_tweet_id_12345",
        }
