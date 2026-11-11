from typing import Optional
from fastapi import Depends

from app.infrastructure.services.ppr1001_vacunas import PPR1001Service
from app.infrastructure.services.ppr1001_pediatria import PPR1001_Atenciones_Service
from app.infrastructure.services.pandas_his_excel_reader import PandasHISExcelReader
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase


def get_his_excel_reader() -> HISExcelReaderPort:
    """Provee el lector y filtro de archivos Excel HIS."""
    return PandasHISExcelReader()


def get_vacunas_service() -> PPR1001Service:
    """Provee el servicio de cálculo de Inmunizaciones (ppr1001_vacunas.py)."""
    return PPR1001Service()


def get_pediatria_service() -> PPR1001_Atenciones_Service:
    """Provee el servicio de cálculo de Pediatría (ppr1001_pediatria.py)."""
    return PPR1001_Atenciones_Service()


def get_procesar_ppr1001_use_case(
    reader: HISExcelReaderPort = Depends(get_his_excel_reader),
    vacunas_service: PPR1001Service = Depends(get_vacunas_service),
    pediatria_service: PPR1001_Atenciones_Service = Depends(get_pediatria_service),
) -> ProcesarPPR1001UseCase:
    """
    Inyecta el caso de uso principal con ambos calculadores (Inmunizaciones y Pediatría).
    NOTA: El repositorio de SQL Server se pasa como None temporalmente
    mientras se prepara la base de datos para el histórico.
    """
    return ProcesarPPR1001UseCase(
        his_reader=reader,
        vacunas_calculator=vacunas_service,
        pediatria_calculator=pediatria_service,
        historico_repo=None,
    )
