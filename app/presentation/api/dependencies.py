from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sqlalchemy_patient_repository import SqlAlchemyPatientRepository
from app.infrastructure.services.pandas_patient_excel_service import PandasPatientExcelService
from app.domain.repositories.patient_repository import PatientRepositoryInterface
from app.application.ports.patient_excel_port import PatientExcelPort
from app.application.use_cases.create_patient import CreatePatientUseCase
from app.application.use_cases.get_patient import GetPatientByIdUseCase
from app.application.use_cases.list_patients import ListPatientsUseCase
from app.application.use_cases.export_patients_excel import ExportPatientsExcelUseCase
from app.application.use_cases.import_patients_excel import ImportPatientsExcelUseCase
from app.application.use_cases.generate_patient_template import GeneratePatientTemplateUseCase


def get_patient_repository(
    db: Session = Depends(get_db)
) -> PatientRepositoryInterface:
    """Provee la implementación concreta del repositorio de SQL Server."""
    return SqlAlchemyPatientRepository(db_session=db)


def get_patient_excel_service() -> PatientExcelPort:
    """Provee el servicio de manipulación de hojas de cálculo con Pandas."""
    return PandasPatientExcelService()


def get_create_patient_use_case(
    repo: PatientRepositoryInterface = Depends(get_patient_repository),
) -> CreatePatientUseCase:
    """Inyecta el caso de uso para crear pacientes."""
    return CreatePatientUseCase(patient_repository=repo)


def get_patient_by_id_use_case(
    repo: PatientRepositoryInterface = Depends(get_patient_repository),
) -> GetPatientByIdUseCase:
    """Inyecta el caso de uso para consultar pacientes por ID."""
    return GetPatientByIdUseCase(patient_repository=repo)


def get_list_patients_use_case(
    repo: PatientRepositoryInterface = Depends(get_patient_repository),
) -> ListPatientsUseCase:
    """Inyecta el caso de uso para listar pacientes."""
    return ListPatientsUseCase(patient_repository=repo)


def get_export_patients_excel_use_case(
    repo: PatientRepositoryInterface = Depends(get_patient_repository),
    excel_service: PatientExcelPort = Depends(get_patient_excel_service),
) -> ExportPatientsExcelUseCase:
    """Inyecta el caso de uso para exportar a Excel."""
    return ExportPatientsExcelUseCase(patient_repository=repo, excel_port=excel_service)


def get_import_patients_excel_use_case(
    repo: PatientRepositoryInterface = Depends(get_patient_repository),
    excel_service: PatientExcelPort = Depends(get_patient_excel_service),
) -> ImportPatientsExcelUseCase:
    """Inyecta el caso de uso para importar desde Excel."""
    return ImportPatientsExcelUseCase(patient_repository=repo, excel_port=excel_service)


def get_generate_patient_template_use_case(
    excel_service: PatientExcelPort = Depends(get_patient_excel_service),
) -> GeneratePatientTemplateUseCase:
    """Inyecta el caso de uso para descargar la plantilla de Excel."""
    return GeneratePatientTemplateUseCase(excel_port=excel_service)
