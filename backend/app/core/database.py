from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import text

from app.core.config import settings


def build_database_url() -> str:
    
    password = settings.DATABASE_PASSWORD or ""

    return (
        f"mysql+pymysql://"
        f"{settings.DATABASE_USER}:{password}"
        f"@{settings.DATABASE_HOST}:"
        f"{settings.DATABASE_PORT}/"
        f"{settings.DATABASE_NAME}"
    )


DATABASE_URL = build_database_url()


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Conexión a MySQL exitosa.")
    except Exception as e:
        print(f"❌ Error al conectar con MySQL: {e}")