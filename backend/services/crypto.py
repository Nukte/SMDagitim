"""
Simetrik şifreleme yardımcıları (Fernet: AES-128-CBC + HMAC-SHA256).
OAuth access/refresh token'ları ve AI API key'leri gibi hassas alanları
veritabanında düz metin yerine şifreli tutmak için kullanılır.
"""
import logging
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken

from config import get_settings

logger = logging.getLogger(__name__)

_fernet: Optional[Fernet] = None


def get_fernet() -> Fernet:
    """Fernet nesnesini (ayarlardaki ENCRYPTION_KEY ile) lazy oluşturur ve cache'ler."""
    global _fernet
    if _fernet is None:
        settings = get_settings()
        try:
            _fernet = Fernet(settings.ENCRYPTION_KEY.encode())
        except Exception as e:
            raise RuntimeError(
                "ENCRYPTION_KEY geçersiz. Geçerli bir Fernet anahtarı üretmek için:\n"
                "  python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
            ) from e
    return _fernet


def encrypt_value(value: Optional[str]) -> Optional[str]:
    """Verilen string'i şifreler. None/boş değerleri olduğu gibi geçirir."""
    if value is None or value == "":
        return value
    return get_fernet().encrypt(value.encode()).decode()


def decrypt_value(value: Optional[str]) -> Optional[str]:
    """
    Şifrelenmiş değeri çözer. Şifreleme öncesinden kalan (eski) düz metin
    kayıtlarla geriye dönük uyumluluk için, çözme başarısız olursa değeri
    ham haliyle döndürür — bu sayede geçiş, tek seferlik bir migration
    scripti gerektirmeden, kayıtlar bir sonraki yazımda (ör. hesabı yeniden
    bağlama, AI ayarını güncelleme) kendiliğinden şifrelenerek tamamlanır.
    """
    if value is None or value == "":
        return value
    try:
        return get_fernet().decrypt(value.encode()).decode()
    except InvalidToken:
        logger.warning(
            "Şifre çözme başarısız (InvalidToken) — değer eski/düz metin kayıt olarak kabul edildi."
        )
        return value
    except Exception:
        logger.warning("Şifre çözme sırasında beklenmeyen hata; ham değer döndürülüyor.", exc_info=True)
        return value
