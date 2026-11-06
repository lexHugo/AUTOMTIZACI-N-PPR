from datetime import datetime
from typing import Optional
from app.application.dtos.indicadores_dto import IndicadorDTO
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.ports.ppr1001_interface import PPR1001Interface
from app.domain.entities.historico_ppr import HistoricoPPR
from app.domain.repositories.historico_ppr_repository import HistoricoPPRRepositoryInterface


class ProcesarPPR1001UseCase:
    """
    Caso de Uso Principal:
    Orquesta el flujo completo de:
    1. Lectura y filtrado del archivo Excel HIS.
    2. Aplicación de las fórmulas de las actividades operativas.
    3. Persistencia en SQL Server para registro histórico.
    4. Retorno de resultados consolidados para el frontend.
    """

    def __init__(
        self,
        his_reader: HISExcelReaderPort,
        ppr_calculator: PPR1001Interface,
        historico_repo: Optional[HistoricoPPRRepositoryInterface] = None,
    ):
        self.his_reader = his_reader
        self.ppr_calculator = ppr_calculator
        self.historico_repo = historico_repo

    def execute(self, file_content: bytes, nombre_archivo: str = "trama_his.xlsx") -> IndicadorDTO:
        # 1. Leer y filtrar el Excel a lista de entidades VariablesPPR
        variables = self.his_reader.read_his_excel(file_content)

        # 2. Calcular todas las fórmulas de las actividades operativas
        indicadores = self.ppr_calculator.calcular_todos(variables)

        # 3. Guardar en SQL Server para trazabilidad histórica si el repo está disponible
        if self.historico_repo:
            historico = HistoricoPPR(
                fecha_procesamiento=datetime.utcnow(),
                nombre_archivo=nombre_archivo,
                act_operativa_3325401=indicadores.act_operativa_3325401,
                act_operativa_3325402=indicadores.act_operativa_3325402,
                act_operativa_3325403=indicadores.act_operativa_3325403,
                act_operativa_3325404=indicadores.act_operativa_3325404,
                act_operativa_3325405=indicadores.act_operativa_3325405,
                act_operativa_3325406=indicadores.act_operativa_3325406,
                act_operativa_3325407=indicadores.act_operativa_3325407,
                act_operativa_3325408=indicadores.act_operativa_3325408,
                act_operativa_3325508=indicadores.act_operativa_3325508,
            )
            try:
                self.historico_repo.guardar(historico)
            except Exception as exc:
                print(f"[Warning] No se pudo guardar el histórico en BD: {exc}")

        # 4. Retornar DTO hacia la presentación (frontend)
        return indicadores
