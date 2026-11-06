from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.domain.entities.historico_ppr import HistoricoPPR
from app.infrastructure.database.session import Base


class HistoricoPPRModel(Base):
    """
    Modelo ORM de SQLAlchemy para la tabla de histórico de indicadores PPR1001 en SQL Server.
    """
    __tablename__ = "historico_ppr1001"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fecha_procesamiento = Column(DateTime, default=datetime.utcnow, nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    act_operativa_3325401 = Column(String(100), nullable=False)
    act_operativa_3325402 = Column(String(100), nullable=False)
    act_operativa_3325403 = Column(String(100), nullable=False)
    act_operativa_3325404 = Column(String(100), nullable=False)
    act_operativa_3325405 = Column(String(100), nullable=False)
    act_operativa_3325406 = Column(String(100), nullable=False)
    act_operativa_3325407 = Column(String(100), nullable=False)
    act_operativa_3325408 = Column(String(100), nullable=False)
    act_operativa_3325508 = Column(String(100), nullable=False)

    def to_domain(self) -> HistoricoPPR:
        return HistoricoPPR(
            id=self.id,
            fecha_procesamiento=self.fecha_procesamiento,
            nombre_archivo=self.nombre_archivo,
            act_operativa_3325401=self.act_operativa_3325401,
            act_operativa_3325402=self.act_operativa_3325402,
            act_operativa_3325403=self.act_operativa_3325403,
            act_operativa_3325404=self.act_operativa_3325404,
            act_operativa_3325405=self.act_operativa_3325405,
            act_operativa_3325406=self.act_operativa_3325406,
            act_operativa_3325407=self.act_operativa_3325407,
            act_operativa_3325408=self.act_operativa_3325408,
            act_operativa_3325508=self.act_operativa_3325508,
        )

    @classmethod
    def from_domain(cls, entity: HistoricoPPR) -> "HistoricoPPRModel":
        return cls(
            id=entity.id,
            fecha_procesamiento=entity.fecha_procesamiento or datetime.utcnow(),
            nombre_archivo=entity.nombre_archivo,
            act_operativa_3325401=entity.act_operativa_3325401,
            act_operativa_3325402=entity.act_operativa_3325402,
            act_operativa_3325403=entity.act_operativa_3325403,
            act_operativa_3325404=entity.act_operativa_3325404,
            act_operativa_3325405=entity.act_operativa_3325405,
            act_operativa_3325406=entity.act_operativa_3325406,
            act_operativa_3325407=entity.act_operativa_3325407,
            act_operativa_3325408=entity.act_operativa_3325408,
            act_operativa_3325508=entity.act_operativa_3325508,
        )
