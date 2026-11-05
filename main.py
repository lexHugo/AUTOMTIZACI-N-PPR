from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn

from app.domain.exceptions.domain_exceptions import (
    DomainException,
    PatientNotFoundException,
    PatientAlreadyExistsException,
    InvalidPatientAgeException,
)
from app.infrastructure.config.settings import settings
from app.infrastructure.database.session import Base, engine
from app.presentation.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejo del ciclo de vida de la aplicación.
    Intenta crear las tablas si la base de datos está disponible.
    """
    try:
        # Crea las tablas en SQL Server si no existen
        Base.metadata.create_all(bind=engine)
        print(">> [Database] Conexión y tablas verificadas con éxito en SQL Server.")
    except Exception as exc:
        print(f">> [Database Warning] No se pudo conectar a SQL Server al iniciar: {exc}")
        print(">> Asegúrate de configurar correctamente el archivo .env con las credenciales de SQL Server.")
    yield


app = FastAPI(
    title="Pediatría PPR API - Clean Architecture",
    description="Backend con Arquitectura Limpia en Python usando SQL Server con SQLAlchemy y FastAPI.",
    version="1.0.0",
    lifespan=lifespan,
)

# -------------------------------------------------------------
# Manejadores de Excepciones de Dominio (Mapeo a HTTP Status)
# -------------------------------------------------------------
@app.exception_handler(PatientNotFoundException)
async def patient_not_found_handler(request: Request, exc: PatientNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "error_type": "PatientNotFound"},
    )


@app.exception_handler(PatientAlreadyExistsException)
async def patient_already_exists_handler(request: Request, exc: PatientAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc), "error_type": "PatientAlreadyExists"},
    )


@app.exception_handler(InvalidPatientAgeException)
async def invalid_patient_age_handler(request: Request, exc: InvalidPatientAgeException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc), "error_type": "InvalidPatientAge"},
    )


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_type": "DomainRuleViolation"},
    )


# -------------------------------------------------------------
# Registro de Routers
# -------------------------------------------------------------
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": "Pediatría PPR API",
        "architecture": "Clean Architecture (Hexagonal)",
        "database": "Microsoft SQL Server con SQLAlchemy",
        "presentation": "FastAPI",
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG,
    )
