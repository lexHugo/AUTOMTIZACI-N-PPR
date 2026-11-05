from app.application.dtos.patient_dto import PatientResponseDTO
from app.domain.exceptions.domain_exceptions import PatientNotFoundException
from app.domain.repositories.patient_repository import PatientRepositoryInterface


class GetPatientByIdUseCase:
    """Caso de uso: Consultar paciente por su ID."""

    def __init__(self, patient_repository: PatientRepositoryInterface):
        self.patient_repository = patient_repository

    def execute(self, patient_id: int) -> PatientResponseDTO:
        patient = self.patient_repository.get_by_id(patient_id)
        if not patient:
            raise PatientNotFoundException(patient_id)
        return PatientResponseDTO.from_entity(patient)
