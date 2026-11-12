from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
from app.domain.entities.variables_ppr import VariablesPPR

DatosCitas = Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]


class PPRCalculatorPort(ABC):
    """
    Puerto general de cálculo para Actividades Operativas (Clean Architecture).
    Define el contrato minimalista que el Caso de Uso requiere:
    recibir datos de atenciones y retornar los indicadores calculados.
    """

    @abstractmethod
    def calcular_todos(self, datos: DatosCitas) -> Any:
        """
        Calcula todas las actividades operativas del área respectiva
        (Inmunizaciones o Pediatría) a partir de los datos provistos.
        """
        raise NotImplementedError
