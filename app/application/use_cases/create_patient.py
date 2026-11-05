from app.application.dtos.patient_dto import PatientCreateDTO, PatientResponseDTO
from app.domain.exceptions.domain_exceptions import (
    PatientAlreadyExistsException,
    InvalidPatientAgeException,
)
from app.domain.repositories.patient_repository import PatientRepositoryInterface


class CreatePatientUseCase:
    """Caso de uso: Registrar un nuevo paciente pediátrico."""

    def __init__(self, patient_repository: PatientRepositoryInterface):
        self.patient_repository = patient_repository

    def execute(self, dto: PatientCreateDTO) -> PatientResponseDTO:
        # 1. Verificar si ya existe un paciente con el mismo registro médico
        existing_patient = self.patient_repository.get_by_medical_record_number(
            dto.medical_record_number
        )
        if existing_patient:
            raise PatientAlreadyExistsException(dto.medical_record_number)

        # 2. Instanciar entidad del dominio
        patient = dto.to_entity()

        # 3. Validar regla de negocio pediátrica
        if not patient.is_pediatric():
            raise InvalidPatientAgeException(patient.calculate_age_in_years())

        # 4. Guardar a través del repositorio abstracto
        created_patient = self.patient_repository.create(patient)

        # 5. Retornar DTO de respuesta
        return PatientResponseDTO.from_entity(created_patient)
