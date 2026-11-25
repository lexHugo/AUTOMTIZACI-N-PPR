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
        "Id_ups": ["id_ups", "idups", "ups"],
        "Edad": ["edad_reg", "edad"],
        "Tipo_Edad": ["tipo_edad"],
        "Codigo_Item": ["codigo_item", "codigoitem", "item"],
        "Tipo_Diagnostico": ["tipo_diagnostico", "tipodiagnostico"],
        "Valor_Lab": ["valor_lab", "valorlab"],
        "Id_Correlativo": ["id_correlativo", "idcorrelativo", "correlativo"],
        "Id_Correlativo_Lab": ["id_correlativo_lab", "idcorrelativolab", "correlativo_lab", "correlativolab"],
        "Id_Personal": ["id_personal", "idpersonal", "personal", "nro_doc_personal", "doc_personal", "id_personal_atiende"],
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

    # Filtro de UPS pediátricas: 301204 (Inmunizaciones), 301202 (CRED) y 303712 (Pediatría)
    # UPS_PERMITIDAS = {"301204", "301202", "303712"}
    UPS_PERMITIDAS = {}

    @staticmethod
    def _detect_csv_params(file_content: bytes) -> tuple[str, str]:
        """Detecta la codificación (utf-8 / latin-1) y el delimitador (, ; | \t) del CSV."""
        encoding = "utf-8"
        for enc in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
            try:
                head = file_content[:8192].decode(enc)
                encoding = enc
                break
            except UnicodeDecodeError:
                continue
        else:
            encoding = "latin-1"
            head = file_content[:8192].decode("latin-1", errors="replace")

        first_line = head.splitlines()[0] if head.splitlines() else ""
        counts = {
            ";": first_line.count(";"),
            ",": first_line.count(","),
            "|": first_line.count("|"),
            "\t": first_line.count("\t"),
        }
        best_sep = max(counts, key=counts.get)
        if counts[best_sep] == 0:
            best_sep = ","
        return encoding, best_sep

    def read_his_excel(self, file_content: bytes, filename: str = "") -> List[VariablesPPR]:
        """
        Lee el archivo HIS (Excel .xlsx/.xls o CSV .csv) aplicando usecols para optimizar memoria,
        sanitiza tipos de datos y retorna la lista de VariablesPPR.
        """
        is_excel = (
            file_content.startswith(b"PK\x03\x04")
            or file_content.startswith(b"\xd0\xcf\x11\xe0")
            or filename.lower().endswith((".xlsx", ".xls"))
        ) and not filename.lower().endswith(".csv")

        csv_enc = "utf-8"
        csv_sep = ","
        engine_to_use = "calamine"

        if is_excel:
            try:
                # 1. Leer solo los encabezados (nrows=0) para identificar las columnas presentes
                sample_df = pd.read_excel(io.BytesIO(file_content), nrows=0, engine="calamine")
                engine_to_use = "calamine"
            except Exception:
                try:
                    sample_df = pd.read_excel(io.BytesIO(file_content), nrows=0, engine="openpyxl")
                    engine_to_use = "openpyxl"
                except Exception as exc:
                    raise DomainException(f"Error al abrir el archivo Excel HIS: {exc}")
        else:
            # Procesamiento de archivo CSV
            try:
                csv_enc, csv_sep = self._detect_csv_params(file_content)
                sample_df = pd.read_csv(
                    io.BytesIO(file_content),
                    nrows=0,
                    sep=csv_sep,
                    encoding=csv_enc,
                )
            except Exception as exc:
                raise DomainException(f"Error al abrir el archivo CSV HIS: {exc}")

        # Normalizar los nombres de columnas para búsqueda insensible a mayúsculas/espacios
        excel_columns = {str(col).strip().lower(): col for col in sample_df.columns}

        # 2. Determinar cuáles columnas necesitamos leer
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
            tipo_doc = "Excel" if is_excel else "CSV"
            raise DomainException(
                f"El archivo {tipo_doc} HIS no contiene las siguientes columnas obligatorias: {', '.join(missing_required)}"
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
        if "Valor_Lab" in fields_to_excel_col:
            dtype_spec[fields_to_excel_col["Valor_Lab"]] = str

        if is_excel:
            try:
                df = pd.read_excel(
                    io.BytesIO(file_content),
                    usecols=cols_to_read,
                    dtype=dtype_spec,
                    engine=engine_to_use,
                )
            except Exception:
                # Fallback a openpyxl por seguridad
                try:
                    df = pd.read_excel(
                        io.BytesIO(file_content),
                        usecols=cols_to_read,
                        dtype=dtype_spec,
                        engine="openpyxl",
                    )
                except Exception as exc:
                    raise DomainException(f"Error procesando columnas del Excel HIS: {exc}")
        else:
            try:
                df = pd.read_csv(
                    io.BytesIO(file_content),
                    usecols=cols_to_read,
                    dtype=dtype_spec,
                    sep=csv_sep,
                    encoding=csv_enc,
                    low_memory=False,
                )
            except Exception as exc:
                raise DomainException(f"Error procesando columnas del CSV HIS: {exc}")

        if df.empty:
            return []

        # 4. Invertir mapeo para acceder por nombre de campo de la entidad
        col_to_field = {original_col: field for field, original_col in fields_to_excel_col.items()}
        df.rename(columns=col_to_field, inplace=True)

        # 5. Filtrar de inmediato en Pandas solo las UPS pediátricas: 301204 (Inmunizaciones), 301202 (CRED) y 303712 (Pediatría)
        def normalizar_ups(val: Any) -> str:
            if pd.isna(val) or val is None:
                return ""
            s = str(val).strip()
            if s.endswith(".0"):
                s = s[:-2]
            return s

        #df["Id_ups"] = df["Id_ups"].apply(normalizar_ups)
        #df = df[df["Id_ups"].isin(self.UPS_PERMITIDAS)]

        if df.empty:
            return []

        # 6. Normalizar Fechas
        df["Fecha_Atencion"] = pd.to_datetime(df["Fecha_Atencion"], errors="coerce")

        # 7. Funciones de limpieza de tipos (definidas fuera del bucle para máxima velocidad)
        def clean_str(val: Any) -> str:
            if pd.isna(val) or val is None:
                return ""
            return str(val).strip()

        def clean_optional_str(val: Any) -> Optional[str]:
            if pd.isna(val) or val is None or str(val).strip() == "":
                return None
            s = str(val).strip()
            if isinstance(val, float) and val.is_integer():
                return str(int(val))
            if s.endswith(".0"):
                try:
                    f = float(s)
                    if f.is_integer():
                        return str(int(f))
                except ValueError:
                    pass
            return s

        def clean_optional_int(val: Any) -> Optional[int]:
            if pd.isna(val) or val is None or str(val).strip() == "":
                return None
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return None

        # 8. Construir entidades VariablesPPR usando to_dict('records') de alta velocidad
        entities: List[VariablesPPR] = []

        for row in df.to_dict("records"):
            fecha_atencion = row.get("Fecha_Atencion")
            if pd.isna(fecha_atencion):
                parsed_fecha = date.today()
            elif isinstance(fecha_atencion, (datetime, pd.Timestamp)):
                parsed_fecha = fecha_atencion.date()
            elif isinstance(fecha_atencion, date):
                parsed_fecha = fecha_atencion
            else:
                parsed_fecha = date.today()

            raw_edad = row.get("Edad")
            try:
                edad = int(float(raw_edad)) if not pd.isna(raw_edad) else 0
            except (ValueError, TypeError):
                edad = 0

            entity = VariablesPPR(
                Id_cita=clean_str(row.get("Id_cita")),
                Fecha_Atencion=parsed_fecha,
                Lote=clean_str(row.get("Lote")),
                Id_ups=clean_str(row.get("Id_ups")),
                Edad=edad,
                Tipo_Edad=clean_str(row.get("Tipo_Edad")),
                Codigo_Item=clean_str(row.get("Codigo_Item")),
                Tipo_Diagnostico=clean_str(row.get("Tipo_Diagnostico")),
                Valor_Lab=clean_optional_str(row.get("Valor_Lab")),
                Id_Correlativo=clean_optional_int(row.get("Id_Correlativo")),
                Id_Correlativo_Lab=clean_optional_int(row.get("Id_Correlativo_Lab")),
                Id_Personal=clean_optional_str(row.get("Id_Personal")),
            )
            entities.append(entity)

        # Salida por terminal: Muestra las primeras entidades pobladas para inspección
        print("\n" + "=" * 105)
        print(f"📋 [HIS MINSA - INSPECCIÓN DE POBLADO] Total entidades generadas: {len(entities)}")
        print(f"👉 Mostrando las primeras {min(20, len(entities))} filas cargadas en VariablesPPR:")
        print("-" * 105)
        header = f"{'#':<3} | {'Id_Cita':<12} | {'Fecha':<10} | {'UPS':<6} | {'Edad':<4} | {'T.E':<3} | {'Item':<7} | {'Dx':<2} | {'Valor_Lab':<9} | {'Corr':<4} | {'Corr_Lab':<8}"
        print(header)
        print("-" * 105)
        for i, e in enumerate(entities[:20], start=1):
            f_str = e.Fecha_Atencion.strftime("%Y-%m-%d") if hasattr(e.Fecha_Atencion, "strftime") else str(e.Fecha_Atencion)
            v_lab = str(e.Valor_Lab) if e.Valor_Lab is not None else "-"
            c_diag = str(e.Id_Correlativo) if e.Id_Correlativo is not None else "-"
            c_lab = str(e.Id_Correlativo_Lab) if e.Id_Correlativo_Lab is not None else "-"
            row_str = f"{i:<3} | {e.Id_cita:<12} | {f_str:<10} | {e.Id_ups:<6} | {e.Edad:<4} | {e.Tipo_Edad:<3} | {e.Codigo_Item:<7} | {e.Tipo_Diagnostico:<2} | {v_lab:<9} | {c_diag:<4} | {c_lab:<8}"
            print(row_str)
        print("=" * 105 + "\n")

        return entities
