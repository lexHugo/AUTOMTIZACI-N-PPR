from app.application.ports.patient_excel_port import PatientExcelPort
from app.domain.repositories.patient_repository import PatientRepositoryInterface


class ExportPatientsExcelUseCase:
    """Caso de uso: Exportar la base de datos de pacientes a un archivo Excel (.xlsx)."""

    def __init__(
        self,
        patient_repository: PatientRepositoryInterface,
        excel_port: PatientExcelPort,
    ):
        self.patient_repository = patient_repository
        self.excel_port = excel_port

    def execute(self, skip: int = 0, limit: int = 10000) -> bytes:
        patients = self.patient_repository.list_all(skip=skip, limit=limit)
        return self.excel_port.export_patients(patients)
