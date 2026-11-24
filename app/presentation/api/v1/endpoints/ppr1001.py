from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase
from app.presentation.api.dependencies import (
    get_procesar_ppr1001_use_case,
    get_datamart_repository,
)
from app.domain.repositories.datamart_repository import DataMartRepositoryInterface
from app.presentation.schemas.indicadores_schema import (
    IndicadoresResponse,
    HistoricoPPRResponse,
)

router = APIRouter(prefix="/ppr1001", tags=["PPR1001 - Indicadores Pediátricos"])


@router.post(
    "/procesar",
    response_model=IndicadoresResponse,
    status_code=status.HTTP_200_OK,
    summary="Procesar Trama HIS (Excel o CSV) y acumular en Data Mart",
    description="Recibe el archivo exportado de HIS MINSA (.xlsx, .xls o .csv), lo desduplica y persiste en el Data Mart, y retorna los indicadores calculados con acumulación mensual.",
)
async def procesar_his_excel(
    file: UploadFile = File(..., description="Archivo HIS (.xlsx, .xls o .csv)"),
    use_case: ProcesarPPR1001UseCase = Depends(get_procesar_ppr1001_use_case),
):
    if not file.filename or not file.filename.lower().endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo inválido. Por favor sube un archivo con extensión .xlsx, .xls o .csv",
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
    "/acumulado",
    response_model=IndicadoresResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar indicadores acumulados en el Data Mart",
    description="Retorna el consolidado de indicadores calculados a partir de todas las tramas históricas almacenadas en el Data Mart.",
)
def obtener_indicadores_acumulados(
    use_case: ProcesarPPR1001UseCase = Depends(get_procesar_ppr1001_use_case),
):
    try:
        return use_case.obtener_resumen_acumulado()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar el acumulado del Data Mart: {str(e)}",
        )


@router.get(
    "/datamart/meses",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Listar meses disponibles en el Data Mart",
)
def listar_meses_datamart(
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    return repo.listar_meses_disponibles()


@router.get(
    "/datamart/archivos",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Listar auditoría de archivos cargados en el Data Mart",
)
def listar_archivos_datamart(
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    return repo.listar_archivos_cargados()


@router.delete(
    "/datamart/reiniciar",
    status_code=status.HTTP_200_OK,
    summary="Reiniciar Data Mart (elimina citas e items)",
)
def reiniciar_datamart(
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    repo.reiniciar_datamart()
    return {"mensaje": "Data Mart reiniciado con éxito."}


@router.get(
    "/historico",
    response_model=List[HistoricoPPRResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar histórico (bloqueado temporalmente)",
    description="Retorna el histórico de procesamientos una vez habilitada la base de datos.",
)
def obtener_historico():
    return []
