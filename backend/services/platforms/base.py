"""
Soyut platform publisher base class.
Tüm platformlar bu interface'i implement eder.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from models.schemas import MediaItem
import logging

logger = logging.getLogger(__name__)


class BasePlatformPublisher(ABC):
    """Sosyal medya platform publisher base class."""

    platform_name: str = ""

    @abstractmethod
    async def publish(
        self,
        content: str,
        hashtags: List[str],
        media: List[MediaItem],
        access_token: str,
        account_id: Optional[str] = None,
    ) -> dict:
        """
        Platforma gönderi yayınlar.

        Returns:
            dict: {"post_id": "...", "post_url": "..."}
        """
        pass

    def build_caption(self, content: str, hashtags: List[str]) -> str:
        """İçerik ve etiketleri birleştirerek caption oluşturur."""
        caption = content
        if hashtags:
            tags = " ".join(f"#{tag.strip('#')}" for tag in hashtags)
            caption = f"{content}\n\n{tags}"
        return caption
