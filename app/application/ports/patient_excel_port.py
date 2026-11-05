from abc import ABC, abstractmethod
from typing import List
from app.application.dtos.patient_dto import PatientCreateDTO
from app.domain.entities.patient import Patient


class PatientExcelPort(ABC):
    """
    Puerto de Salida (Output Port) para operaciones con hojas de cálculo Excel.
    Permite desacoplar los casos de uso de la librería específica (Pandas, OpenPyXL, etc.).
    """

    @abstractmethod
    def export_patients(self, patients: List[Patient]) -> bytes:
        """Convierte una lista de entidades Patient en un archivo Excel binario (.xlsx)."""
        raise NotImplementedError

    @abstractmethod
    def parse_patients(self, content: bytes) -> List[PatientCreateDTO]:
        """Lee el contenido binario de un Excel (.xlsx) y lo convierte en lista de PatientCreateDTO."""
        raise NotImplementedError

    @abstractmethod
    def generate_template(self) -> bytes:
        """Genera una plantilla vacía de Excel con los encabezados requeridos y un ejemplo."""
        raise NotImplementedError
