"""
Instagram Graph API Publisher.
Instagram Business hesabına resim/video paylaşımı yapar.
Meta Graph API üzerinden çalışır.
"""
import httpx
import asyncio
import logging
from typing import Optional, List

from models.schemas import MediaItem
from services.platforms.base import BasePlatformPublisher

logger = logging.getLogger(__name__)

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


class InstagramPublisher(BasePlatformPublisher):
    platform_name = "instagram"

    async def publish(
        self,
        content: str,
        hashtags: List[str],
        media: List[MediaItem],
        access_token: str,
        account_id: Optional[str] = None,
    ) -> dict:
        """Instagram Business hesabına paylaşım yapar."""
        if not account_id:
            raise Exception("Instagram Business Account ID bulunamadı. Hesabı yeniden bağlayın.")

        caption = self.build_caption(content, hashtags)

        async with httpx.AsyncClient(timeout=60.0) as client:
            if not media:
                raise Exception("Instagram'da paylaşım yapmak için en az 1 medya gereklidir.")

            if len(media) == 1:
                # Tek medya paylaşımı
                return await self._publish_single(client, account_id, access_token, caption, media[0])
            else:
                # Carousel (çoklu medya) paylaşımı
                return await self._publish_carousel(client, account_id, access_token, caption, media)

    async def _publish_single(
        self, client: httpx.AsyncClient, ig_user_id: str,
        access_token: str, caption: str, media_item: MediaItem
    ) -> dict:
        """Tek resim veya video paylaşır."""
        # 1. Media container oluştur
        container_params = {
            "caption": caption,
            "access_token": access_token,
        }

        if media_item.type == "image":
            container_params["image_url"] = media_item.url
            container_params["media_type"] = "IMAGE"
        elif media_item.type == "video":
            container_params["video_url"] = media_item.url
            container_params["media_type"] = "REELS"

        resp = await client.post(
            f"{GRAPH_API_BASE}/{ig_user_id}/media",
            data=container_params,
        )
        resp_data = resp.json()

        if "id" not in resp_data:
            error = resp_data.get("error", {}).get("message", str(resp_data))
            raise Exception(f"Instagram container oluşturulamadı: {error}")

        container_id = resp_data["id"]
        logger.info(f"[instagram] Container oluşturuldu: {container_id}")

        # Video ise işlenmesini bekle
        if media_item.type == "video":
            await self._wait_for_processing(client, container_id, access_token)

        # 2. Container'ı yayınla
        publish_resp = await client.post(
            f"{GRAPH_API_BASE}/{ig_user_id}/media_publish",
            data={
                "creation_id": container_id,
                "access_token": access_token,
            },
        )
        publish_data = publish_resp.json()

        if "id" not in publish_data:
            error = publish_data.get("error", {}).get("message", str(publish_data))
            raise Exception(f"Instagram yayınlama hatası: {error}")

        post_id = publish_data["id"]
        logger.info(f"[instagram] Paylaşım başarılı! Post ID: {post_id}")

        return {
            "post_id": post_id,
            "post_url": f"https://www.instagram.com/p/{post_id}/",
        }

    async def _publish_carousel(
        self, client: httpx.AsyncClient, ig_user_id: str,
        access_token: str, caption: str, media_items: List[MediaItem]
    ) -> dict:
        """Carousel (çoklu medya) paylaşımı yapar."""
        children_ids = []

        # Her medya için container oluştur
        for item in media_items[:10]:  # Instagram max 10 medya
            params = {"access_token": access_token, "is_carousel_item": "true"}

            if item.type == "image":
                params["image_url"] = item.url
                params["media_type"] = "IMAGE"
            elif item.type == "video":
                params["video_url"] = item.url
                params["media_type"] = "VIDEO"

            resp = await client.post(
                f"{GRAPH_API_BASE}/{ig_user_id}/media", data=params
            )
            data = resp.json()
            if "id" not in data:
                error = data.get("error", {}).get("message", str(data))
                raise Exception(f"Carousel item oluşturulamadı: {error}")
            children_ids.append(data["id"])

        # Ana carousel container'ı oluştur
        carousel_params = {
            "caption": caption,
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "access_token": access_token,
        }
        resp = await client.post(
            f"{GRAPH_API_BASE}/{ig_user_id}/media", data=carousel_params
        )
        data = resp.json()
        if "id" not in data:
            error = data.get("error", {}).get("message", str(data))
            raise Exception(f"Carousel container oluşturulamadı: {error}")

        container_id = data["id"]

        # Yayınla
        publish_resp = await client.post(
            f"{GRAPH_API_BASE}/{ig_user_id}/media_publish",
            data={"creation_id": container_id, "access_token": access_token},
        )
        publish_data = publish_resp.json()
        if "id" not in publish_data:
            error = publish_data.get("error", {}).get("message", str(publish_data))
            raise Exception(f"Carousel yayınlama hatası: {error}")

        post_id = publish_data["id"]
        return {"post_id": post_id, "post_url": f"https://www.instagram.com/p/{post_id}/"}

    async def _wait_for_processing(
        self, client: httpx.AsyncClient, container_id: str,
        access_token: str, max_wait: int = 120
    ):
        """Video işlenene kadar bekler."""
        for _ in range(max_wait // 5):
            resp = await client.get(
                f"{GRAPH_API_BASE}/{container_id}",
                params={"fields": "status_code", "access_token": access_token},
            )
            data = resp.json()
            status_code = data.get("status_code")

            if status_code == "FINISHED":
                return
            elif status_code == "ERROR":
                raise Exception("Instagram video işleme hatası.")

            await asyncio.sleep(5)

        raise Exception("Instagram video işleme zaman aşımına uğradı.")
