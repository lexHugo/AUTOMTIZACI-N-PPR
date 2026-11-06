import io
from datetime import date, datetime
from typing import Any, Dict, List, Optional
import pandas as pd

from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.domain.entities.variables_ppr import VariablesPPR
from app.domain.exceptions.domain_exceptions import DomainException


class PandasHISExcelReader(HISExcelReaderPort):
    """
    Implementación del lector de tramas HIS de MINSA usando Pandas y OpenPyXL.
    Filtra de manera eficiente solo las columnas requeridas para la entidad VariablesPPR.
    """

    # Mapeo de campos requeridos de la entidad hacia posibles nombres de columna en el Excel HIS
    COLUMN_MAPPING: Dict[str, List[str]] = {
        "Id_cita": ["id_cita", "idcita"],
        "Fecha_Atencion": ["fecha_atencion", "f_atencion"],
        "Lote": ["lote"],
        "Id_ups": ["id_ups", "idups"],
        "Edad": ["edad_reg", "edad"],
        "Tipo_Edad": ["tipo_edad"],
        "Codigo_Item": ["codigo_item", "codigoitem", "item"],
        "Tipo_Diagnostico": ["tipo_diagnostico", "tipodiagnostico"],
        "Valor_Lab": ["valor_lab", "valorlab"],
        "Correlativo1": ["correlativo1", "id_correlativo", "idcorrelativo"],
        "Correlativo2": ["correlativo2"],
        "Correlativo3": ["correlativo3"],
        "Lab1": ["lab1", "id_correlativo_lab", "idcorrelativolab"],
        "Lab2": ["lab2"],
        "Lab3": ["lab3"],
    }

    REQUIRED_FIELDS = [
        "Id_cita",
        "Fecha_Atencion",
        "Lote",
        "Id_ups",
        "Edad",
        "Tipo_Edad",
        "Codigo_Item",
        "Tipo_Diagnostico",
    ]

    def read_his_excel(self, file_content: bytes) -> List[VariablesPPR]:
        """
        Lee el Excel HIS aplicando usecols para optimizar memoria,
        sanitiza tipos de datos y retorna la lista de VariablesPPR.
        """
        try:
            # 1. Leer solo los encabezados (nrows=0) para identificar las columnas presentes
            sample_df = pd.read_excel(io.BytesIO(file_content), nrows=0, engine="openpyxl")
        except Exception as exc:
            raise DomainException(f"Error al abrir el archivo Excel HIS: {exc}")

        # Normalizar los nombres de columnas del Excel para búsqueda insensible a mayúsculas/espacios
        excel_columns = {str(col).strip().lower(): col for col in sample_df.columns}

        # 2. Determinar cuáles columnas del Excel necesitamos leer
        fields_to_excel_col: Dict[str, str] = {}
        missing_required = []

        for field_name, candidates in self.COLUMN_MAPPING.items():
            matched_col = None
            for candidate in candidates:
                if candidate in excel_columns:
                    matched_col = excel_columns[candidate]
                    break
            if matched_col:
                fields_to_excel_col[field_name] = matched_col
            elif field_name in self.REQUIRED_FIELDS:
                missing_required.append(f"{field_name} (se esperaba: {', '.join(candidates)})")

        if missing_required:
            raise DomainException(
                f"El archivo Excel HIS no contiene las siguientes columnas obligatorias: {', '.join(missing_required)}"
            )

        # 3. Leer únicamente las columnas que coinciden (usecols)
        cols_to_read = list(fields_to_excel_col.values())
        dtype_spec = {
            fields_to_excel_col["Id_cita"]: str,
            fields_to_excel_col["Lote"]: str,
            fields_to_excel_col["Id_ups"]: str,
            fields_to_excel_col["Codigo_Item"]: str,
            fields_to_excel_col["Tipo_Diagnostico"]: str,
            fields_to_excel_col["Tipo_Edad"]: str,
        }

        try:
            df = pd.read_excel(
                io.BytesIO(file_content),
                usecols=cols_to_read,
                dtype=dtype_spec,
                engine="openpyxl",
            )
        except Exception as exc:
            raise DomainException(f"Error procesando columnas del Excel HIS: {exc}")

        if df.empty:
            return []

        # 4. Invertir mapeo para acceder por nombre de campo de la entidad
        col_to_field = {original_col: field for field, original_col in fields_to_excel_col.items()}
        df.rename(columns=col_to_field, inplace=True)

        # 5. Normalizar Fechas
        df["Fecha_Atencion"] = pd.to_datetime(df["Fecha_Atencion"], errors="coerce")

        # 6. Construir entidades VariablesPPR
        entities: List[VariablesPPR] = []

        for index, row in df.iterrows():
            # Descartar filas vacías
            if row.isna().all():
                continue

            fecha_atencion = row["Fecha_Atencion"]
            if pd.isna(fecha_atencion):
                parsed_fecha = date.today()
            elif isinstance(fecha_atencion, (datetime, pd.Timestamp)):
                parsed_fecha = fecha_atencion.date()
            elif isinstance(fecha_atencion, date):
                parsed_fecha = fecha_atencion
            else:
                parsed_fecha = date.today()

            def clean_str(val: Any) -> str:
                if pd.isna(val) or val is None:
                    return ""
                return str(val).strip()

            def clean_optional_str(val: Any) -> Optional[str]:
                if pd.isna(val) or val is None or str(val).strip() == "":
                    return None
                return str(val).strip()

            def clean_optional_int(val: Any) -> Optional[int]:
                if pd.isna(val) or val is None or str(val).strip() == "":
                    return None
                try:
                    return int(float(val))
                except (ValueError, TypeError):
                    return None

            try:
                raw_edad = row["Edad"]
                edad = int(float(raw_edad)) if not pd.isna(raw_edad) else 0
            except (ValueError, TypeError):
                edad = 0

            entity = VariablesPPR(
                Id_cita=clean_str(row["Id_cita"]),
                Fecha_Atencion=parsed_fecha,
                Lote=clean_str(row["Lote"]),
                Id_ups=clean_str(row["Id_ups"]),
                Edad=edad,
                Tipo_Edad=clean_str(row["Tipo_Edad"]),
                Codigo_Item=clean_str(row["Codigo_Item"]),
                Tipo_Diagnostico=clean_str(row["Tipo_Diagnostico"]),
                Valor_Lab=clean_optional_str(row.get("Valor_Lab")),
                Correlativo1=clean_optional_int(row.get("Correlativo1")),
                Correlativo2=clean_optional_int(row.get("Correlativo2")),
                Correlativo3=clean_optional_int(row.get("Correlativo3")),
                Lab1=clean_optional_int(row.get("Lab1")),
                Lab2=clean_optional_int(row.get("Lab2")),
                Lab3=clean_optional_int(row.get("Lab3")),
            )
            entities.append(entity)

        return entities
