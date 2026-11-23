from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.infrastructure.config.settings import settings

# Base declarativa para los modelos ORM de SQLAlchemy
Base = declarative_base()

# Creación del engine de SQLAlchemy con soporte para SQLite y SQL Server
db_url = settings.database_url

if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        echo=settings.API_DEBUG,
        connect_args={"check_same_thread": False},  # Permite concurrencia de hilos en FastAPI con SQLite
    )
else:
    engine = create_engine(
        db_url,
        echo=settings.API_DEBUG,
        pool_pre_ping=True,  # Verifica conexiones activas antes de usarlas
        fast_executemany=True,  # Optimización específica para SQL Server / pyodbc
    )

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Generador de sesión de base de datos para inyección de dependencias.
    Asegura el cierre de la sesión al finalizar la petición HTTP.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa el Data Mart creando todas las tablas en la base de datos si aún no existen.
    """
    # Importar los modelos para que SQLAlchemy los registre en Base.metadata
    import app.infrastructure.models.datamart_models  # noqa: F401
    Base.metadata.create_all(bind=engine)
