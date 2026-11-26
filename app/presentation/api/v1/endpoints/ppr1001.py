from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.application.use_cases.procesar_ppr1001_use_case import ProcesarPPR1001UseCase
from app.presentation.api.dependencies import (
    get_procesar_ppr1001_use_case,
    get_datamart_repository,
)
from app.domain.repositories.datamart_repository import DataMartRepositoryInterface
from app.presentation.schemas.indicadores_schema import (
    IndicadoresResponse,
    HistoricoPPRResponse,
)

router = APIRouter(prefix="/ppr1001", tags=["PPR1001 - Indicadores Pediátricos"])


@router.post(
    "/procesar",
    response_model=IndicadoresResponse,
    status_code=status.HTTP_200_OK,
    summary="Procesar Trama HIS (Excel o CSV) y acumular en Data Mart",
    description="Recibe el archivo exportado de HIS MINSA (.xlsx, .xls o .csv), lo desduplica y persiste en el Data Mart, y retorna los indicadores calculados con acumulación mensual.",
)
async def procesar_his_excel(
    file: UploadFile = File(..., description="Archivo HIS (.xlsx, .xls o .csv)"),
    use_case: ProcesarPPR1001UseCase = Depends(get_procesar_ppr1001_use_case),
):
    if not file.filename or not file.filename.lower().endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo inválido. Por favor sube un archivo con extensión .xlsx, .xls o .csv",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado está vacío.",
        )

    resultado = use_case.execute(file_content=file_bytes, nombre_archivo=file.filename)
    return resultado


@router.get(
    "/acumulado",
    response_model=IndicadoresResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar indicadores acumulados en el Data Mart",
    description="Retorna el consolidado de indicadores calculados a partir de todas las tramas históricas almacenadas en el Data Mart.",
)
def obtener_indicadores_acumulados(
    use_case: ProcesarPPR1001UseCase = Depends(get_procesar_ppr1001_use_case),
):
    try:
        return use_case.obtener_resumen_acumulado()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar el acumulado del Data Mart: {str(e)}",
        )


@router.get(
    "/datamart/meses",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Listar meses disponibles en el Data Mart",
)
def listar_meses_datamart(
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    return repo.listar_meses_disponibles()


@router.get(
    "/datamart/archivos",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Listar auditoría de archivos cargados en el Data Mart",
)
def listar_archivos_datamart(
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    return repo.listar_archivos_cargados()


@router.post(
    "/datamart/personal/cargar-maestro",
    status_code=status.HTTP_200_OK,
    summary="Cargar archivo Excel o CSV Maestro de Personal de Salud (Médicos y Enfermeras)",
    description="Recibe el archivo maestro con las columnas Id_Personal, Cod_Profesion, Nombres y DNI.",
)
async def cargar_maestro_personal(
    file: UploadFile = File(..., description="Archivo Excel (.xlsx, .xls) o CSV con el catálogo maestro de personal"),
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    import io
    import pandas as pd

    if not file.filename or not file.filename.lower().endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo inválido. Por favor sube un archivo con extensión .xlsx, .xls o .csv",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado está vacío.",
        )

    try:
        if file.filename.lower().endswith(".csv"):
            # Auto-detección de codificación (soporte para 'Ñ' y tildes en latin-1/cp1252) y separador
            encoding_detectado = "latin-1"
            delimitador_detectado = ","

            for enc in ["utf-8-sig", "utf-8", "latin-1", "cp1252", "iso-8859-1"]:
                try:
                    head = file_bytes[:16384].decode(enc)
                    encoding_detectado = enc
                    first_line = head.splitlines()[0] if head.splitlines() else ""
                    counts = {
                        ";": first_line.count(";"),
                        ",": first_line.count(","),
                        "|": first_line.count("|"),
                        "\t": first_line.count("\t"),
                    }
                    best_sep = max(counts, key=counts.get)
                    if counts[best_sep] > 0:
                        delimitador_detectado = best_sep
                    break
                except UnicodeDecodeError:
                    continue

            df = pd.read_csv(
                io.BytesIO(file_bytes),
                dtype=str,
                encoding=encoding_detectado,
                sep=delimitador_detectado,
            )
        else:
            try:
                df = pd.read_excel(io.BytesIO(file_bytes), dtype=str, engine="calamine")
            except Exception:
                df = pd.read_excel(io.BytesIO(file_bytes), dtype=str, engine="openpyxl")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al leer el archivo de personal: {str(exc)}",
        )

    # Normalizar nombres de columnas para detección flexible
    col_dict = {str(c).strip().lower(): c for c in df.columns}

    def buscar_columna(posibles: List[str]) -> Optional[str]:
        for p in posibles:
            if p in col_dict:
                return col_dict[p]
        return None

    col_id = buscar_columna(["id_personal", "idpersonal", "id", "personal", "id_personal_declarado"])
    col_prof = buscar_columna([
        "cod_profesion", "codprofesion", "id_profesion", "profesion_cod",
        "profesion", "cod_prof", "codigo_profesion", "idprofesion"
    ])
    col_nom = buscar_columna([
        "nombres", "nombre", "personal", "nombres_apellidos", "apellidos_nombres",
        "personal_salud", "doctor", "enfermera", "descripcion_personal"
    ])
    col_dni = buscar_columna([
        "dni", "nro_doc", "documento", "numero_documento", "num_doc", "nro_documento"
    ])

    if not col_id or not col_prof:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El archivo debe contener obligatoriamente las columnas 'Id_Personal' y 'Cod_Profesion'. Columnas detectadas: {list(df.columns)}",
        )

    registros = []
    for _, row in df.iterrows():
        id_val = str(row[col_id]).strip() if pd.notna(row[col_id]) else ""
        prof_val = str(row[col_prof]).strip() if pd.notna(row[col_prof]) else ""
        if not id_val or id_val.lower() == "nan":
            continue

        if prof_val.endswith(".0"):
            prof_val = str(int(float(prof_val)))

        nom_val = str(row[col_nom]).strip() if (col_nom and pd.notna(row[col_nom])) else None
        if nom_val and nom_val.lower() == "nan":
            nom_val = None

        dni_val = str(row[col_dni]).strip() if (col_dni and pd.notna(row[col_dni])) else None
        if dni_val and dni_val.lower() == "nan":
            dni_val = None

        registros.append({
            "id_personal": id_val,
            "cod_profesion": prof_val,
            "nombres": nom_val,
            "dni": dni_val,
        })

    resultado = repo.guardar_personal_maestro(registros)
    return {
        "mensaje": "Maestro de personal cargado exitosamente en el Data Mart.",
        "nombre_archivo": file.filename,
        "total_filas_archivo": len(df),
        "total_registros_procesados": resultado.get("total_procesados", 0),
    }


@router.get(
    "/datamart/personal",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Listar personal de salud registrado en el Data Mart",
)
def listar_personal_datamart(
    cod_profesion: Optional[str] = None,
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    return repo.listar_personal(cod_profesion=cod_profesion)


@router.get(
    "/calculos/ups",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Calcular atenciones (citas únicas) por UPS y por mes",
    description="Cuenta 1 atención por cada cita médica única, desglosada por UPS y mes, excluyendo código 29 y con filtro opcional de profesión.",
)
def calcular_atenciones_ups(
    cod_profesion: Optional[str] = None,
    anio: Optional[int] = None,
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    from app.infrastructure.services.ppr1001_seguimiento import PPR1001SeguimientoService

    service = PPR1001SeguimientoService()
    target_ups = list(service.UPS_PEDIATRIA | service.UPS_NEONATOLOGIA)

    # Opción 1: Consulta agregada directa a base de datos (Ultra-rápida, 0 MB sobrecarga de objetos)
    resumen_db = repo.obtener_resumen_atenciones_ups(
        target_ups=target_ups,
        cod_profesion=cod_profesion,
        anio=anio,
        excluir_cod_profesion="29",
    )

    resultado = service.calcular_desde_resumen_db(resumen_db=resumen_db)
    return resultado


@router.delete(
    "/datamart/reiniciar",
    status_code=status.HTTP_200_OK,
    summary="Reiniciar Data Mart (elimina citas e items)",
)
def reiniciar_datamart(
    repo: DataMartRepositoryInterface = Depends(get_datamart_repository),
):
    repo.reiniciar_datamart()
    return {"mensaje": "Data Mart reiniciado con éxito."}


@router.get(
    "/historico",
    response_model=List[HistoricoPPRResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar histórico (bloqueado temporalmente)",
    description="Retorna el histórico de procesamientos una vez habilitada la base de datos.",
)
def obtener_historico():
    return []
