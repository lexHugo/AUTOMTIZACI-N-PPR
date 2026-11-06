from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.variables_ppr import VariablesPPR
from app.application.dtos.indicadores_dto import IndicadorDTO


class PPR1001Interface(ABC):
    """
    Puerto de cálculo para las Actividades Operativas del PPR1001.
    Define las firmas para calcular cada fórmula individual y el consolidado general.
    """

    @abstractmethod
    def calcular_3325401(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325401."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325402(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325402."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325403(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325403."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325404(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325404."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325405(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325405."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325406(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325406."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325407(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325407."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325408(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325408."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325508(self, variables: List[VariablesPPR]) -> str:
        """Cálculo de la Actividad Operativa 3325508."""
        raise NotImplementedError

    @abstractmethod
    def calcular_todos(self, variables: List[VariablesPPR]) -> IndicadorDTO:
        """Calcula todas las actividades operativas y consolida en IndicadorDTO."""
        raise NotImplementedError

    def ppr1001(self, variables: List[VariablesPPR]) -> IndicadorDTO:
        """Método de compatibilidad."""
        return self.calcular_todos(variables)
