from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn

from app.domain.exceptions.domain_exceptions import (
    DomainException,
    InvalidPPRException,
)
from app.infrastructure.config.settings import settings
from app.presentation.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación. Conexión a BD pausada temporalmente."""
    print(">> [App] Pediatría PPR1001 API iniciada correctamente.")
    yield


app = FastAPI(
    title="Pediatría PPR1001 - Monitor de Actividades Operativas",
    description="Panel interactivo y API para cálculo de indicadores del programa presupuestal PPR1001 con tramas HIS MINSA.",
    version="1.0.0",
    lifespan=lifespan,
)

# -------------------------------------------------------------
# Manejadores de Excepciones de Dominio (Mapeo a HTTP Status)
# -------------------------------------------------------------
@app.exception_handler(InvalidPPRException)
async def invalid_ppr_handler(request: Request, exc: InvalidPPRException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc), "error_type": "InvalidPPRData"},
    )


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_type": "DomainRuleViolation"},
    )


# -------------------------------------------------------------
# Registro de Routers API
# -------------------------------------------------------------
app.include_router(api_v1_router, prefix="/api/v1")


# -------------------------------------------------------------
# Frontend UI y Archivos Estáticos (CSS, JS)
# -------------------------------------------------------------
WEB_DIR = Path(__file__).parent / "app" / "presentation" / "web"
UI_FILE_PATH = WEB_DIR / "index.html"
CIE10_FILE_PATH = WEB_DIR / "cie10.html"

# Montar directorio estático para servir css/ y js/
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_ui():
    """Sirve la interfaz web simple para cargar el Excel y ver los indicadores."""
    if UI_FILE_PATH.exists():
        return HTMLResponse(content=UI_FILE_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>UI en construcción</h1>")


@app.get("/desglose-cie10", response_class=HTMLResponse, tags=["Frontend UI"])
@app.get("/cie10", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_cie10_ui():
    """Sirve la página con el desglose de códigos CIE-10 y sus contadores."""
    if CIE10_FILE_PATH.exists():
        return HTMLResponse(content=CIE10_FILE_PATH.read_text(encoding="utf-8"))
    return RedirectResponse(url="/?tab=cie10", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG,
    )
