from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status

from app.application.dtos.patient_dto import PatientCreateDTO
from app.application.use_cases.create_patient import CreatePatientUseCase
from app.application.use_cases.get_patient import GetPatientByIdUseCase
from app.application.use_cases.list_patients import ListPatientsUseCase
from app.application.use_cases.export_patients_excel import ExportPatientsExcelUseCase
from app.application.use_cases.import_patients_excel import ImportPatientsExcelUseCase
from app.application.use_cases.generate_patient_template import GeneratePatientTemplateUseCase
from app.presentation.api.dependencies import (
    get_create_patient_use_case,
    get_patient_by_id_use_case,
    get_list_patients_use_case,
    get_export_patients_excel_use_case,
    get_import_patients_excel_use_case,
    get_generate_patient_template_use_case,
)
from app.presentation.schemas.patient_schema import PatientCreateRequest, PatientResponse
from app.presentation.schemas.excel_schema import ImportResultResponse

router = APIRouter(prefix="/patients", tags=["Pacientes Pediátricos"])

EXCEL_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


# -------------------------------------------------------------
# Endpoints de Excel (Exportación, Importación y Plantilla)
# Definidos antes de /{patient_id} para evitar colisiones de rutas
# -------------------------------------------------------------
@router.get(
    "/export/excel",
    response_class=Response,
    summary="Exportar pacientes a archivo Excel (.xlsx)",
    description="Genera y descarga un archivo Excel con el listado completo de pacientes registrados.",
)
def export_patients_to_excel(
    skip: int = 0,
    limit: int = 10000,
    use_case: ExportPatientsExcelUseCase = Depends(get_export_patients_excel_use_case),
):
    excel_bytes = use_case.execute(skip=skip, limit=limit)
    return Response(
        content=excel_bytes,
        media_type=EXCEL_MEDIA_TYPE,
        headers={"Content-Disposition": "attachment; filename=pacientes_pediatria.xlsx"},
    )


@router.get(
    "/template/excel",
    response_class=Response,
    summary="Descargar plantilla de Excel para importación masiva",
    description="Descarga un archivo Excel con los encabezados requeridos y una fila de ejemplo.",
)
def download_excel_template(
    use_case: GeneratePatientTemplateUseCase = Depends(get_generate_patient_template_use_case),
):
    template_bytes = use_case.execute()
    return Response(
        content=template_bytes,
        media_type=EXCEL_MEDIA_TYPE,
        headers={"Content-Disposition": "attachment; filename=plantilla_importacion_pacientes.xlsx"},
    )


@router.post(
    "/import/excel",
    response_model=ImportResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Importar pacientes masivamente desde un archivo Excel",
    description="Sube un archivo .xlsx para registrar múltiples pacientes a la vez aplicando reglas de negocio.",
)
async def import_patients_from_excel(
    file: UploadFile = File(..., description="Archivo de hoja de cálculo .xlsx"),
    use_case: ImportPatientsExcelUseCase = Depends(get_import_patients_excel_use_case),
):
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo inválido. Por favor sube un archivo con extensión .xlsx o .xls",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado está vacío.",
        )

    result = use_case.execute(file_content=file_bytes)
    return result


# -------------------------------------------------------------
# Endpoints CRUD de Pacientes
# -------------------------------------------------------------
@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo paciente",
)
def create_patient(
    request: PatientCreateRequest,
    use_case: CreatePatientUseCase = Depends(get_create_patient_use_case),
):
    dto = PatientCreateDTO(
        first_name=request.first_name,
        last_name=request.last_name,
        birth_date=request.birth_date,
        medical_record_number=request.medical_record_number,
        guardian_name=request.guardian_name,
        guardian_phone=request.guardian_phone,
    )
    result = use_case.execute(dto)
    return result


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un paciente por su ID",
)
def get_patient(
    patient_id: int,
    use_case: GetPatientByIdUseCase = Depends(get_patient_by_id_use_case),
):
    return use_case.execute(patient_id=patient_id)


@router.get(
    "",
    response_model=List[PatientResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los pacientes",
)
def list_patients(
    skip: int = 0,
    limit: int = 100,
    use_case: ListPatientsUseCase = Depends(get_list_patients_use_case),
):
    return use_case.execute(skip=skip, limit=limit)
