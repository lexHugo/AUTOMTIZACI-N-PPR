from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase
from app.presentation.api.dependencies import get_procesar_ppr1001_use_case
from app.presentation.schemas.indicadores_schema import (
    IndicadoresResponse,
    HistoricoPPRResponse,
)

router = APIRouter(prefix="/ppr1001", tags=["PPR1001 - Indicadores Pediátricos"])


@router.post(
    "/procesar",
    response_model=IndicadoresResponse,
    status_code=status.HTTP_200_OK,
    summary="Procesar Excel HIS y calcular los 9 indicadores",
    description="Recibe el archivo Excel exportado de HIS MINSA, filtra variables y calcula las 9 actividades operativas.",
)
async def procesar_his_excel(
    file: UploadFile = File(..., description="Archivo Excel HIS (.xlsx o .xls)"),
    use_case: ProcesarPPR1001UseCase = Depends(get_procesar_ppr1001_use_case),
):
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo inválido. Por favor sube un archivo con extensión .xlsx o .xls",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado está vacío.",
        )

    resultado = use_case.execute(file_content=file_bytes, nombre_archivo=file.filename)
    return resultado


@router.get(
    "/historico",
    response_model=List[HistoricoPPRResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar histórico (bloqueado temporalmente)",
    description="Retorna el histórico de procesamientos una vez habilitada la base de datos.",
)
def obtener_historico():
    # Flujo de base de datos pausado temporalmente
    return []
