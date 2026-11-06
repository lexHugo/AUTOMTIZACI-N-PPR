from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.services.ppr1001 import PPR1001Service
from app.infrastructure.services.pandas_his_excel_reader import PandasHISExcelReader
from app.infrastructure.repositories.sqlalchemy_historico_ppr_repository import (
    SqlAlchemyHistoricoPPRRepository,
)
from app.domain.repositories.historico_ppr_repository import HistoricoPPRRepositoryInterface
from app.application.ports.ppr1001_interface import PPR1001Interface
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase


def get_his_excel_reader() -> HISExcelReaderPort:
    """Provee el lector y filtro de archivos Excel HIS."""
    return PandasHISExcelReader()


def get_ppr1001_service() -> PPR1001Interface:
    """Provee el servicio de cálculo de actividades operativas e indicadores."""
    return PPR1001Service()


def get_historico_repository(
    db: Session = Depends(get_db),
) -> HistoricoPPRRepositoryInterface:
    """Provee el repositorio de almacenamiento histórico en SQL Server."""
    return SqlAlchemyHistoricoPPRRepository(db_session=db)


def get_procesar_ppr1001_use_case(
    reader: HISExcelReaderPort = Depends(get_his_excel_reader),
    calculator: PPR1001Interface = Depends(get_ppr1001_service),
    repo: HistoricoPPRRepositoryInterface = Depends(get_historico_repository),
) -> ProcesarPPR1001UseCase:
    """Inyecta el caso de uso principal para procesar el Excel y calcular indicadores."""
    return ProcesarPPR1001UseCase(
        his_reader=reader,
        ppr_calculator=calculator,
        historico_repo=repo,
    )
