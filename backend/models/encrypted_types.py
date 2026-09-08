"""
Şifreli veritabanı kolon tipi.
Hassas alanları (OAuth token, AI API key) yazarken şifreler, okurken çözer;
uygulama katmanı için tamamen şeffaftır (normal bir `Text` kolonu gibi kullanılır).
"""
from sqlalchemy.types import TypeDecorator, Text

from services.crypto import encrypt_value, decrypt_value


class EncryptedText(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return encrypt_value(value)

    def process_result_value(self, value, dialect):
        return decrypt_value(value)
