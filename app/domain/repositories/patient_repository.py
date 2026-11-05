from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.patient import Patient


class PatientRepositoryInterface(ABC):
    """
    Contrato abstracto (Puerto de Salida) para la persistencia de pacientes.
    Cualquier adaptador de persistencia (SQL Server, memoria, MongoDB, etc.)
    debe implementar esta interfaz.
    """

    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        """Crea un nuevo paciente en la persistencia."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        """Obtiene un paciente por su identificador único."""
        raise NotImplementedError

    @abstractmethod
    def get_by_medical_record_number(self, medical_record_number: str) -> Optional[Patient]:
        """Obtiene un paciente por su número de historia clínica."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Retorna una lista paginada de pacientes."""
        raise NotImplementedError

    @abstractmethod
    def update(self, patient: Patient) -> Patient:
        """Actualiza la información de un paciente."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, patient_id: int) -> bool:
        """Elimina un paciente del almacenamiento."""
        raise NotImplementedError
