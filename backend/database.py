"""
SQLAlchemy veritabanı bağlantısı ve session yönetimi.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import get_settings

settings = get_settings()

# Render ve benzeri platformlar 'postgres://' formatı verebilir, SQLAlchemy 'postgresql://' ister.
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# SQLite kullanılıyorsa özel connect_args gerekir, Postgres vb için gerekmez.
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — her request için yeni session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
