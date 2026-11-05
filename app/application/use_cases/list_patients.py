from typing import List
from app.application.dtos.patient_dto import PatientResponseDTO
from app.domain.repositories.patient_repository import PatientRepositoryInterface


class ListPatientsUseCase:
    """Caso de uso: Listar pacientes con paginación."""

    def __init__(self, patient_repository: PatientRepositoryInterface):
        self.patient_repository = patient_repository

    def execute(self, skip: int = 0, limit: int = 100) -> List[PatientResponseDTO]:
        patients = self.patient_repository.list_all(skip=skip, limit=limit)
        return [PatientResponseDTO.from_entity(p) for p in patients]
