from app.application.dtos.patient_dto import PatientImportResultDTO
from app.application.ports.patient_excel_port import PatientExcelPort
from app.domain.repositories.patient_repository import PatientRepositoryInterface


class ImportPatientsExcelUseCase:
    """Caso de uso: Importar pacientes masivamente desde un archivo Excel."""

    def __init__(
        self,
        patient_repository: PatientRepositoryInterface,
        excel_port: PatientExcelPort,
    ):
        self.patient_repository = patient_repository
        self.excel_port = excel_port

    def execute(self, file_content: bytes) -> PatientImportResultDTO:
        # 1. Parsear el archivo Excel a lista de DTOs
        parsed_dtos = self.excel_port.parse_patients(file_content)

        total_rows = len(parsed_dtos)
        imported_count = 0
        failed_count = 0
        errors = []

        # 2. Procesar cada fila validando reglas de negocio
        for index, dto in enumerate(parsed_dtos, start=2):  # start=2 considerando fila 1 de encabezados
            try:
                # Validar unicidad de historia clínica
                existing = self.patient_repository.get_by_medical_record_number(
                    dto.medical_record_number
                )
                if existing:
                    failed_count += 1
                    errors.append(
                        f"Fila {index}: Ya existe un paciente con historia clínica '{dto.medical_record_number}'."
                    )
                    continue

                patient = dto.to_entity()

                # Validar regla de edad pediátrica
                if not patient.is_pediatric():
                    failed_count += 1
                    errors.append(
                        f"Fila {index}: El paciente '{dto.first_name} {dto.last_name}' tiene {patient.calculate_age_in_years()} años y excede el límite pediátrico."
                    )
                    continue

                # Guardar en repositorio
                self.patient_repository.create(patient)
                imported_count += 1

            except Exception as ex:
                failed_count += 1
                errors.append(f"Fila {index}: Error inesperado al procesar registro: {str(ex)}")

        return PatientImportResultDTO(
            total_rows=total_rows,
            imported_count=imported_count,
            failed_count=failed_count,
            errors=errors,
        )
