from typing import Optional
from fastapi import Depends

from app.infrastructure.services.ppr1001 import PPR1001Service
from app.infrastructure.services.pandas_his_excel_reader import PandasHISExcelReader
from app.application.ports.ppr1001_interface import PPR1001Interface
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase


def get_his_excel_reader() -> HISExcelReaderPort:
    """Provee el lector y filtro de archivos Excel HIS."""
    return PandasHISExcelReader()


def get_ppr1001_service() -> PPR1001Interface:
    """Provee el servicio de cálculo de actividades operativas e indicadores."""
    return PPR1001Service()


def get_procesar_ppr1001_use_case(
    reader: HISExcelReaderPort = Depends(get_his_excel_reader),
    calculator: PPR1001Interface = Depends(get_ppr1001_service),
) -> ProcesarPPR1001UseCase:
    """
    Inyecta el caso de uso principal.
    NOTA: El repositorio de SQL Server se pasa como None temporalmente
    mientras se prepara la base de datos para el histórico.
    """
    return ProcesarPPR1001UseCase(
        his_reader=reader,
        ppr_calculator=calculator,
        historico_repo=None,
    )
