from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.services.ppr1001_vacunas import PPR1001Service
from app.infrastructure.services.ppr1001_pediatria import PPR1001_Atenciones_Service
from app.infrastructure.services.pandas_his_excel_reader import PandasHISExcelReader
from app.infrastructure.repositories.sqlite_datamart_repository import SqliteDataMartRepository
from app.domain.repositories.datamart_repository import DataMartRepositoryInterface
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.ports.ppr_calculator_port import PPRCalculatorPort
from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase


def get_his_excel_reader() -> HISExcelReaderPort:
    """Provee el lector y filtro de archivos Excel/CSV HIS."""
    return PandasHISExcelReader()


def get_vacunas_service() -> PPRCalculatorPort:
    """Provee el servicio de cálculo de Inmunizaciones (ppr1001_vacunas.py)."""
    return PPR1001Service()


def get_pediatria_service() -> PPRCalculatorPort:
    """Provee el servicio de cálculo de Pediatría (ppr1001_pediatria.py)."""
    return PPR1001_Atenciones_Service()


def get_datamart_repository(db: Session = Depends(get_db)) -> DataMartRepositoryInterface:
    """Provee el repositorio para el Data Mart."""
    return SqliteDataMartRepository(db)


def get_procesar_ppr1001_use_case(
    reader: HISExcelReaderPort = Depends(get_his_excel_reader),
    vacunas_service: PPRCalculatorPort = Depends(get_vacunas_service),
    pediatria_service: PPRCalculatorPort = Depends(get_pediatria_service),
    datamart_repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
) -> ProcesarPPR1001UseCase:
    """
    Inyecta el caso de uso principal con calculadores y repositorio de Data Mart.
    """
    return ProcesarPPR1001UseCase(
        his_reader=reader,
        vacunas_calculator=vacunas_service,
        pediatria_calculator=pediatria_service,
        historico_repo=None,
        datamart_repo=datamart_repo,
    )
