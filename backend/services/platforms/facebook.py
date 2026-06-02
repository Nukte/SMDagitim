"""
Facebook Graph API Publisher.
Facebook Sayfasına metin, resim ve video paylaşımı yapar.
"""
import httpx
import logging
from typing import Optional, List

from models.schemas import MediaItem
from services.platforms.base import BasePlatformPublisher

logger = logging.getLogger(__name__)

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


class FacebookPublisher(BasePlatformPublisher):
    platform_name = "facebook"

    async def publish(
        self,
        content: str,
        hashtags: List[str],
        media: List[MediaItem],
        access_token: str,
        account_id: Optional[str] = None,
    ) -> dict:
        """Facebook Sayfasına gönderi paylaşır."""
        target_id = account_id or "me"
        caption = self.build_caption(content, hashtags)

        async with httpx.AsyncClient(timeout=60.0) as client:
            if not media:
                # Sadece metin paylaşımı
                return await self._publish_text(client, target_id, access_token, caption)
            elif len(media) == 1:
                item = media[0]
                if item.type == "image":
                    return await self._publish_photo(client, target_id, access_token, caption, item)
                else:
                    return await self._publish_video(client, target_id, access_token, caption, item)
            else:
                # Çoklu fotoğraf paylaşımı
                return await self._publish_multi_photo(client, target_id, access_token, caption, media)

    async def _publish_text(self, client, target_id, access_token, message) -> dict:
        resp = await client.post(
            f"{GRAPH_API_BASE}/{target_id}/feed",
            data={"message": message, "access_token": access_token},
        )
        data = resp.json()
        if "id" not in data:
            error = data.get("error", {}).get("message", str(data))
            raise Exception(f"Facebook metin paylaşım hatası: {error}")

        post_id = data["id"]
        logger.info(f"[facebook] Metin paylaşıldı: {post_id}")
        return {"post_id": post_id, "post_url": f"https://www.facebook.com/{post_id}"}

    async def _publish_photo(self, client, target_id, access_token, message, media_item) -> dict:
        resp = await client.post(
            f"{GRAPH_API_BASE}/{target_id}/photos",
            data={
                "url": media_item.url,
                "message": message,
                "access_token": access_token,
            },
        )
        data = resp.json()
        if "id" not in data:
            error = data.get("error", {}).get("message", str(data))
            raise Exception(f"Facebook fotoğraf paylaşım hatası: {error}")

        post_id = data["id"]
        logger.info(f"[facebook] Fotoğraf paylaşıldı: {post_id}")
        return {"post_id": post_id, "post_url": f"https://www.facebook.com/{post_id}"}

    async def _publish_video(self, client, target_id, access_token, message, media_item) -> dict:
        resp = await client.post(
            f"{GRAPH_API_BASE}/{target_id}/videos",
            data={
                "file_url": media_item.url,
                "description": message,
                "access_token": access_token,
            },
        )
        data = resp.json()
        if "id" not in data:
            error = data.get("error", {}).get("message", str(data))
            raise Exception(f"Facebook video paylaşım hatası: {error}")

        post_id = data["id"]
        logger.info(f"[facebook] Video paylaşıldı: {post_id}")
        return {"post_id": post_id, "post_url": f"https://www.facebook.com/{post_id}"}

    async def _publish_multi_photo(self, client, target_id, access_token, message, media_items) -> dict:
        """Çoklu fotoğraf paylaşımı (unpublished photos + feed post)."""
        photo_ids = []
        for item in media_items:
            if item.type != "image":
                continue
            resp = await client.post(
                f"{GRAPH_API_BASE}/{target_id}/photos",
                data={
                    "url": item.url,
                    "published": "false",
                    "access_token": access_token,
                },
            )
            data = resp.json()
            if "id" in data:
                photo_ids.append(data["id"])

        # Tüm fotoğrafları tek bir post olarak yayınla
        feed_data = {"message": message, "access_token": access_token}
        for i, pid in enumerate(photo_ids):
            feed_data[f"attached_media[{i}]"] = f'{{"media_fbid":"{pid}"}}'

        resp = await client.post(f"{GRAPH_API_BASE}/{target_id}/feed", data=feed_data)
        data = resp.json()
        if "id" not in data:
            error = data.get("error", {}).get("message", str(data))
            raise Exception(f"Facebook çoklu fotoğraf paylaşım hatası: {error}")

        post_id = data["id"]
        return {"post_id": post_id, "post_url": f"https://www.facebook.com/{post_id}"}
