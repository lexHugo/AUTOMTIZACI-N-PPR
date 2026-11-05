import io
from datetime import date, datetime
from typing import List
import pandas as pd

from app.application.dtos.patient_dto import PatientCreateDTO
from app.application.ports.patient_excel_port import PatientExcelPort
from app.domain.entities.patient import Patient
from app.domain.exceptions.domain_exceptions import DomainException


class PandasPatientExcelService(PatientExcelPort):
    """
    Implementación del puerto de hojas de cálculo usando Pandas y OpenPyXL.
    Pertenece a la capa de Infraestructura.
    """

    # Mapeo de sinónimos de columnas para mayor tolerancia al importar
    COLUMN_MAPPINGS = {
        "first_name": ["nombres", "nombre", "first_name", "primer_nombre"],
        "last_name": ["apellidos", "apellido", "last_name", "segundo_nombre_y_apellidos"],
        "birth_date": ["fecha_nacimiento", "fecha de nacimiento", "fecha_de_nacimiento", "birth_date", "f_nacimiento"],
        "medical_record_number": ["historia_clinica", "historia clínica", "numero_historia", "no_historia", "medical_record_number", "hc"],
        "guardian_name": ["tutor", "tutor_responsable", "responsable", "guardian_name", "nombre_tutor", "acudiente"],
        "guardian_phone": ["telefono", "teléfono", "telefono_tutor", "teléfono_tutor", "celular", "guardian_phone", "contacto"],
    }

    def export_patients(self, patients: List[Patient]) -> bytes:
        """Exporta una lista de entidades Patient a un archivo Excel (.xlsx) con formato estilizado."""
        data = []
        for p in patients:
            data.append({
                "ID": p.id,
                "Nombres": p.first_name,
                "Apellidos": p.last_name,
                "Fecha de Nacimiento": p.birth_date.strftime("%Y-%m-%d") if isinstance(p.birth_date, (date, datetime)) else str(p.birth_date),
                "Historia Clínica": p.medical_record_number,
                "Tutor / Responsable": p.guardian_name,
                "Teléfono de Contacto": p.guardian_phone,
                "Edad (Años)": p.calculate_age_in_years(),
                "Fecha de Registro": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else "",
            })

        df = pd.DataFrame(data)

        # Si no hay pacientes, creamos el dataframe con las columnas vacías
        if df.empty:
            df = pd.DataFrame(columns=[
                "ID", "Nombres", "Apellidos", "Fecha de Nacimiento",
                "Historia Clínica", "Tutor / Responsable", "Teléfono de Contacto",
                "Edad (Años)", "Fecha de Registro"
            ])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Pacientes")

            # Auto-ajuste de ancho de columnas si openpyxl está disponible
            worksheet = writer.sheets["Pacientes"]
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

        output.seek(0)
        return output.getvalue()

    def parse_patients(self, content: bytes) -> List[PatientCreateDTO]:
        """Lee el contenido binario de un Excel y lo transforma en lista de PatientCreateDTO."""
        try:
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        except Exception as ex:
            raise DomainException(f"No se pudo leer el archivo Excel. Verifica que sea un archivo .xlsx válido: {ex}")

        if df.empty:
            return []

        # Normalizar nombres de columnas a minúsculas sin espacios
        df_columns = {col: str(col).strip().lower().replace(" ", "_") for col in df.columns}
        df.rename(columns=df_columns, inplace=True)

        # Resolver nombres de columnas esperadas
        resolved_cols = {}
        for target_field, candidates in self.COLUMN_MAPPINGS.items():
            found_col = None
            for candidate in candidates:
                cand_normalized = candidate.lower().replace(" ", "_")
                if cand_normalized in df.columns:
                    found_col = cand_normalized
                    break
            if not found_col:
                raise DomainException(
                    f"Falta la columna obligatoria '{target_field}' en el Excel. Columnas encontradas: {list(df.columns)}"
                )
            resolved_cols[target_field] = found_col

        dtos: List[PatientCreateDTO] = []

        for index, row in df.iterrows():
            # Saltar filas completamente vacías
            if row.isna().all():
                continue

            try:
                first_name = str(row[resolved_cols["first_name"]]).strip()
                last_name = str(row[resolved_cols["last_name"]]).strip()
                medical_record = str(row[resolved_cols["medical_record_number"]]).strip()
                guardian_name = str(row[resolved_cols["guardian_name"]]).strip()
                
                # Tratar teléfono para evitar que '3001234567.0' ocurra por inferencia numérica de pandas
                raw_phone = row[resolved_cols["guardian_phone"]]
                if pd.isna(raw_phone):
                    guardian_phone = ""
                elif isinstance(raw_phone, float) and raw_phone.is_integer():
                    guardian_phone = str(int(raw_phone))
                else:
                    guardian_phone = str(raw_phone).strip()

                # Parsear fecha de nacimiento
                raw_date = row[resolved_cols["birth_date"]]
                parsed_date = pd.to_datetime(raw_date, errors="coerce").date()
                if pd.isna(parsed_date):
                    raise ValueError(f"Fecha de nacimiento inválida: '{raw_date}'")

                dto = PatientCreateDTO(
                    first_name=first_name,
                    last_name=last_name,
                    birth_date=parsed_date,
                    medical_record_number=medical_record,
                    guardian_name=guardian_name,
                    guardian_phone=guardian_phone,
                )
                dtos.append(dto)
            except Exception as row_error:
                raise DomainException(f"Error procesando fila {index + 2}: {row_error}")

        return dtos

    def generate_template(self) -> bytes:
        """Crea una plantilla de Excel con columnas requeridas y un registro de ejemplo."""
        template_data = [
            {
                "Nombres": "Mateo",
                "Apellidos": "Gómez Restrepo",
                "Fecha de Nacimiento": "2020-05-15",
                "Historia Clínica": "PED-2024-001",
                "Tutor / Responsable": "Laura Restrepo (Madre)",
                "Teléfono Tutor": "+57 300 1234567",
            }
        ]
        df = pd.DataFrame(template_data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Plantilla Pacientes")
            worksheet = writer.sheets["Plantilla Pacientes"]
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 4, 15)

        output.seek(0)
        return output.getvalue()
