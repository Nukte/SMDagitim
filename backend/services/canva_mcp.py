"""
Canva MCP (Model Context Protocol) entegrasyon servisi.
Canva'nın resmi MCP sunucusuna (mcp.canva.com) OAuth access token'ı ile
Streamable HTTP transport üzerinden bağlanır; tasarımdaki metinleri okur,
çevirir ve bir KOPYA tasarım üzerine yazar (orijinal tasarım değiştirilmez).

DOĞRULAMA NOTU: MCP taşıma katmanı (streamablehttp_client, ClientSession,
call_tool/CallToolResult şeması) resmi `mcp` Python SDK kaynak kodundan
doğrulanmıştır. Tool adları/parametreleri (get-design-content, copy-design,
start-editing-transaction, perform-editing-operations, commit-editing-transaction)
Canva'nın MCP entegrasyonunun bilinen sözleşmesine göre yazılmıştır; canlı bir
Canva hesabı ve tasarımıyla ilk kullanımda `session.list_tools()` çıktısıyla
doğrulanması ve özellikle `_parse_text_elements` fonksiyonunun (gerçek
`get-design-content` yanıt şekline göre) teyit edilmesi gerekir.
"""
import json
import logging
import re
from typing import Any, Awaitable, Callable, Dict, List, Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

logger = logging.getLogger(__name__)

MCP_SERVER_URL = "https://mcp.canva.com/mcp"

_DESIGN_ID_RE = re.compile(r"/design/([A-Za-z0-9_-]{11})")


def _extract_design_id(design_url_or_id: str) -> str:
    """Bir Canva paylaşım URL'sinden veya doğrudan ID'den 11 karakterlik design ID'yi çıkarır."""
    candidate = design_url_or_id.strip()
    if candidate.startswith("D") and "/" not in candidate and len(candidate) == 11:
        return candidate
    match = _DESIGN_ID_RE.search(candidate)
    if not match:
        raise ValueError(f"Canva design ID, verilen URL'den çıkarılamadı: {design_url_or_id}")
    return match.group(1)


def _tool_data(result) -> Dict[str, Any]:
    """CallToolResult'tan yapılandırılmış veriyi çıkarır (structuredContent öncelikli)."""
    if getattr(result, "isError", False):
        detail = result.content[0].text if result.content else "bilinmeyen hata"
        raise RuntimeError(f"Canva MCP tool hatası: {detail}")

    if result.structuredContent is not None:
        return result.structuredContent

    for block in result.content:
        if getattr(block, "type", None) == "text":
            try:
                return json.loads(block.text)
            except json.JSONDecodeError:
                continue

    raise RuntimeError(
        "Canva MCP tool yanıtı ayrıştırılamadı (structuredContent yok, text bloğu JSON değil)."
    )


class CanvaMCPService:
    """Canva MCP sunucusuna bağlanıp tasarım okuma/çeviri/yazma akışını yürütür."""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def _parse_text_elements(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        `get-design-content` (content_types=["richtexts"]) yanıtındaki metin
        elemanlarını düz {"id": ..., "content": ...} listesine indirger.

        Canva'nın MCP yanıt şeması sayfa/eleman ağacı biçimindedir; birden
        fazla makul şekli tolere edecek şekilde yazılmıştır. Hiçbiri
        eşleşmezse (canlı testte şema farklı çıkarsa) sessizce boş liste
        dönmek yerine ham veriyi loglayıp açıkça uyarır.
        """
        elements: List[Dict[str, str]] = []
        pages = data.get("pages") or data.get("content") or []

        for page in pages:
            items = page.get("elements") or page.get("richtexts") or page.get("items") or []
            for el in items:
                element_id = el.get("id") or el.get("element_id")
                text = el.get("text") or el.get("content") or el.get("plain_text")
                if element_id and text:
                    elements.append({"id": element_id, "content": text})

        if not elements and pages:
            logger.warning(
                "[Canva MCP] get-design-content yanıtında beklenen şema bulunamadı, "
                "ham veri: %s",
                json.dumps(data)[:2000],
            )

        return elements

    async def translate_design(
        self,
        design_url: str,
        target_language: str,
        translate_func: Callable[[str, str], Awaitable[str]],
    ) -> str:
        """
        Ana iş akışı (tek MCP oturumu içinde, doğru sırayla):
        1. Orijinal tasarımı KOPYALA (orijinal asla değiştirilmez).
        2. Kopyadaki metinleri oku (element ID'ler kopyaya ait olmalı).
        3. Metinleri çevir.
        4. Kopya üzerinde bir düzenleme oturumu aç, çevrilmiş metinleri yaz, kaydet.
        """
        design_id = _extract_design_id(design_url)

        async with streamablehttp_client(MCP_SERVER_URL, headers=self._headers()) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                copy_result = await session.call_tool("copy-design", {"design_id": design_id})
                copy_data = _tool_data(copy_result)
                new_design_id = copy_data.get("design_id") or copy_data.get("id")
                if not new_design_id:
                    raise RuntimeError(f"copy-design yanıtında design_id bulunamadı: {copy_data}")
                new_design_url: str = (
                    copy_data.get("url")
                    or copy_data.get("edit_url")
                    or f"https://www.canva.com/design/{new_design_id}/edit"
                )

                content_result = await session.call_tool(
                    "get-design-content",
                    {"design_id": new_design_id, "content_types": ["richtexts"]},
                )
                elements = self._parse_text_elements(_tool_data(content_result))

                if not elements:
                    logger.warning(
                        "[Canva MCP] Kopyalanan tasarımda çevrilecek metin bulunamadı: %s",
                        new_design_id,
                    )
                    return new_design_url

                translated_elements = []
                for el in elements:
                    translated_text = await translate_func(el["content"], target_language)
                    translated_elements.append({"id": el["id"], "content": translated_text})

                tx_result = await session.call_tool(
                    "start-editing-transaction", {"design_id": new_design_id}
                )
                tx_data = _tool_data(tx_result)
                transaction_id = tx_data["transaction_id"]
                pages = tx_data.get("pages", [])

                operations = [
                    {"type": "replace_text", "element_id": t["id"], "text": t["content"]}
                    for t in translated_elements
                ]

                await session.call_tool(
                    "perform-editing-operations",
                    {
                        "transaction_id": transaction_id,
                        "operations": operations,
                        "page_index": 1,
                        "pages": pages,
                    },
                )
                await session.call_tool(
                    "commit-editing-transaction", {"transaction_id": transaction_id}
                )

                logger.info(
                    "[Canva MCP] Çeviri tamamlandı: %d eleman, yeni tasarım: %s",
                    len(translated_elements),
                    new_design_id,
                )

        return new_design_url
