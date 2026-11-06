from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.historico_ppr import HistoricoPPR


class HistoricoPPRRepositoryInterface(ABC):
    """
    Puerto de persistencia para el histórico de indicadores PPR1001.
    """

    @abstractmethod
    def guardar(self, historico: HistoricoPPR) -> HistoricoPPR:
        """Guarda un registro de indicadores históricos en la base de datos."""
        raise NotImplementedError

    @abstractmethod
    def listar_historico(self, limit: int = 50) -> List[HistoricoPPR]:
        """Obtiene la lista de los últimos procesamientos realizados."""
        raise NotImplementedError
