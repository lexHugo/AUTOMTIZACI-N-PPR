from app.application.ports.patient_excel_port import PatientExcelPort


class GeneratePatientTemplateUseCase:
    """Caso de uso: Descargar plantilla oficial vacía con columnas para importación."""

    def __init__(self, excel_port: PatientExcelPort):
        self.excel_port = excel_port

    def execute(self) -> bytes:
        return self.excel_port.generate_template()
