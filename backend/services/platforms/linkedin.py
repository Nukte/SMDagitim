"""
LinkedIn Publisher — UGC Posts API (v2)
"Share on LinkedIn" ürünü + w_member_social scope ile çalışır.

Akış:
  1. Person URN al (account_id yoksa token'dan çek)
  2. (Resimli) POST /v2/assets?action=registerUpload → uploadUrl + asset URN
  3. (Resimli) PUT uploadUrl → binary upload
  4. POST /v2/ugcPosts → post oluştur
"""
import json
import base64
import httpx
import logging
from typing import Optional, List

from models.schemas import MediaItem
from services.platforms.base import BasePlatformPublisher

logger = logging.getLogger(__name__)


class LinkedInPublisher(BasePlatformPublisher):
    platform_name = "linkedin"

    async def publish(
        self,
        content: str,
        hashtags: List[str],
        media: List[MediaItem],
        access_token: str,
        account_id: Optional[str] = None,
    ) -> dict:
        caption = self.build_caption(content, hashtags)
        if len(caption) > 3000:
            caption = caption[:2997] + "..."

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Person ID yoksa token'dan çıkar
            if not account_id:
                account_id = await self._get_person_id(client, access_token)

            if not account_id:
                raise Exception(
                    "LinkedIn person ID alınamadı. "
                    "Lütfen Dashboard'dan LinkedIn bağlantısını kesip yeniden bağlayın."
                )

            person_urn = f"urn:li:person:{account_id}"
            logger.info(f"[linkedin] Person URN: {person_urn}")

            # Medya varsa yükle
            asset_urn = None
            if media and media[0].type == "image":
                asset_urn = await self._register_and_upload_image(
                    client, access_token, person_urn, media[0]
                )

            # Post oluştur
            post_payload = self._build_ugc_post(person_urn, caption, asset_urn)
            logger.info(f"[linkedin] UGC post gönderiliyor...")

            resp = await client.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=self._headers(access_token),
                json=post_payload,
            )

            if resp.status_code == 201:
                post_id = resp.headers.get("x-restli-id", "")
                post_url = f"https://www.linkedin.com/feed/update/{post_id}/"
                logger.info(f"[linkedin] ✅ Post başarılı: {post_id}")
                return {"post_id": post_id, "post_url": post_url}
            else:
                logger.error(f"[linkedin] ❌ Post hatası {resp.status_code}: {resp.text}")
                raise Exception(f"LinkedIn post oluşturulamadı ({resp.status_code}): {resp.text}")

    # ── Yardımcı metodlar ──────────────────────────────────────────────────

    def _headers(self, access_token: str) -> dict:
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    async def _get_person_id(self, client: httpx.AsyncClient, access_token: str) -> Optional[str]:
        """Person ID'yi çeşitli yöntemlerle almaya çalışır."""

        # Yöntem 1: /v2/userinfo (OpenID scope varsa)
        try:
            r = await client.get(
                "https://api.linkedin.com/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if r.status_code == 200:
                pid = r.json().get("sub")
                if pid:
                    logger.info(f"[linkedin] Person ID (userinfo): {pid}")
                    return pid
        except Exception:
            pass

        # Yöntem 2: /v2/me
        try:
            r = await client.get(
                "https://api.linkedin.com/v2/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if r.status_code == 200:
                pid = r.json().get("id")
                if pid:
                    logger.info(f"[linkedin] Person ID (/v2/me): {pid}")
                    return pid
        except Exception:
            pass

        # Yöntem 3: Access token JWT decode
        try:
            parts = access_token.split(".")
            if len(parts) >= 2:
                payload = parts[1] + "=" * (4 - len(parts[1]) % 4)
                decoded = json.loads(base64.urlsafe_b64decode(payload))
                pid = decoded.get("sub") or decoded.get("id")
                if pid:
                    logger.info(f"[linkedin] Person ID (JWT): {pid}")
                    return pid
        except Exception:
            pass

        logger.error("[linkedin] Person ID hiçbir yöntemle alınamadı")
        return None

    async def _register_and_upload_image(
        self,
        client: httpx.AsyncClient,
        access_token: str,
        person_urn: str,
        media_item: MediaItem,
    ) -> Optional[str]:
        """Resmi LinkedIn'e yükler, asset URN döndürür."""

        # Adım 1: registerUpload
        reg_resp = await client.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=self._headers(access_token),
            json={
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": person_urn,
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent",
                        }
                    ],
                }
            },
        )

        if reg_resp.status_code != 200:
            logger.error(f"[linkedin] registerUpload hatası {reg_resp.status_code}: {reg_resp.text}")
            return None  # Hata olursa resim olmadan devam et

        reg_data = reg_resp.json()
        upload_mechanism = reg_data["value"]["uploadMechanism"]
        upload_url = upload_mechanism[
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]
        asset_urn = reg_data["value"]["asset"]
        logger.info(f"[linkedin] Asset URN: {asset_urn}")

        # Adım 2: Medyayı indirip yükle
        media_url = str(media_item.url)
        dl_resp = await client.get(media_url)
        if dl_resp.status_code != 200:
            logger.error(f"[linkedin] Medya indirilemedi: {media_url}")
            return None

        up_resp = await client.put(
            upload_url,
            headers={"Authorization": f"Bearer {access_token}"},
            content=dl_resp.content,
        )

        if up_resp.status_code not in (200, 201):
            logger.error(f"[linkedin] Resim upload hatası {up_resp.status_code}: {up_resp.text}")
            return None

        logger.info(f"[linkedin] Resim upload başarılı ✅")
        return asset_urn

    def _build_ugc_post(
        self,
        person_urn: str,
        text: str,
        asset_urn: Optional[str] = None,
    ) -> dict:
        """UGC Posts API payload oluşturur."""
        if asset_urn:
            share_content = {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "media": asset_urn,
                    }
                ],
            }
        else:
            share_content = {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }

        return {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": share_content,
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
            },
        }
