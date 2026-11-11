from abc import ABC, abstractmethod
from typing import Dict, List, Union
from app.domain.entities.variables_ppr import VariablesPPR
from app.application.dtos.indicadores_dto import IndicadorVacunasDTO, IndicadorDTO

DatosCitas = Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]


class PPR1001Interface(ABC):
    """
    Puerto de cálculo para las Actividades Operativas del PPR1001.
    Define las firmas para calcular cada fórmula individual y el consolidado general.
    """

    @abstractmethod
    def calcular_3325401(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325401."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325402(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325402."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325403(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325403."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325404(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325404."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325405(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325405."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325406(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325406."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325407(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325407."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325408(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325408."""
        raise NotImplementedError

    @abstractmethod
    def calcular_3325508(self, datos: DatosCitas) -> str:
        """Cálculo de la Actividad Operativa 3325508."""
        raise NotImplementedError

    @abstractmethod
    def calcular_todos(self, variables: DatosCitas) -> Union[IndicadorVacunasDTO, IndicadorDTO]:
        """Calcula todas las actividades operativas y consolida en DTO."""
        raise NotImplementedError

    def ppr1001(self, variables: DatosCitas) -> Union[IndicadorVacunasDTO, IndicadorDTO]:
        """Método de compatibilidad."""
        return self.calcular_todos(variables)
