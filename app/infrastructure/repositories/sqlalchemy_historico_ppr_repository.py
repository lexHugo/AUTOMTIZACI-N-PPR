from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.historico_ppr import HistoricoPPR
from app.domain.repositories.historico_ppr_repository import HistoricoPPRRepositoryInterface
from app.infrastructure.models.historico_ppr_model import HistoricoPPRModel


class SqlAlchemyHistoricoPPRRepository(HistoricoPPRRepositoryInterface):
    """
    Implementación del repositorio de histórico en SQL Server usando SQLAlchemy.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, historico: HistoricoPPR) -> HistoricoPPR:
        model = HistoricoPPRModel.from_domain(historico)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_domain()

    def listar_historico(self, limit: int = 50) -> List[HistoricoPPR]:
        models = (
            self.db.query(HistoricoPPRModel)
            .order_by(HistoricoPPRModel.fecha_procesamiento.desc())
            .limit(limit)
            .all()
        )
        return [m.to_domain() for m in models]
