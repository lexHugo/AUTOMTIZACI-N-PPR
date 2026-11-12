from collections import defaultdict
from datetime import datetime
from typing import Any, Optional
from app.application.dtos.indicadores_dto import (
    IndicadorDTO,
    IndicadorVacunasDTO,
    IndicadorPediatriaDTO,
)
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.ports.ppr_calculator_port import PPRCalculatorPort
from app.domain.entities.historico_ppr import HistoricoPPR
from app.domain.repositories.historico_ppr_repository import HistoricoPPRRepositoryInterface


class ProcesarPPR1001UseCase:
    """
    Caso de Uso Principal:
    Orquesta el flujo completo de:
    1. Lectura y filtrado del archivo Excel HIS.
    2. Agrupamiento en memoria por cita (UNA SOLA VEZ).
    3. Cálculo de actividades de Inmunizaciones (ppr1001_vacunas.py).
    4. Cálculo de actividades de Pediatría (ppr1001_pediatria.py).
    5. Consolidación separada de ambos bloques en IndicadorDTO.
    6. Persistencia histórica opcional en SQL Server.
    """

    def __init__(
        self,
        his_reader: HISExcelReaderPort,
        vacunas_calculator: PPRCalculatorPort,
        pediatria_calculator: Optional[PPRCalculatorPort] = None,
        historico_repo: Optional[HistoricoPPRRepositoryInterface] = None,
    ):
        self.his_reader = his_reader
        self.vacunas_calculator = vacunas_calculator
        self.pediatria_calculator = pediatria_calculator
        self.historico_repo = historico_repo

    def execute(self, file_content: bytes, nombre_archivo: str = "trama_his.xlsx") -> IndicadorDTO:
        # 1. Leer y filtrar el Excel a lista de entidades VariablesPPR
        variables = self.his_reader.read_his_excel(file_content)

        # 2. Agrupar por cita UNA SOLA VEZ en memoria para compartir entre ambos servicios
        citas = defaultdict(list)
        for v in variables:
            citas[v.Id_cita].append(v)

        # 3. Calcular Inmunizaciones
        inm_dto = self.vacunas_calculator.calcular_todos(citas)
        if not isinstance(inm_dto, IndicadorVacunasDTO):
            if hasattr(inm_dto, "inmunizaciones"):
                inm_dto = inm_dto.inmunizaciones

        # 4. Calcular Pediatría
        ped_dto = IndicadorPediatriaDTO()
        if self.pediatria_calculator:
            ped_dto = self.pediatria_calculator.calcular_todos(citas)
            if hasattr(ped_dto, "pediatria"):
                ped_dto = ped_dto.pediatria

        # 5. Consolidar en el IndicadorDTO principal separado en dos bloques
        indicadores = IndicadorDTO(
            inmunizaciones=inm_dto,
            pediatria=ped_dto,
        )

        # 6. Guardar en SQL Server si el repo está configurado
        if self.historico_repo:
            historico = HistoricoPPR(
                fecha_procesamiento=datetime.utcnow(),
                nombre_archivo=nombre_archivo,
                act_operativa_3325401=indicadores.inmunizaciones.act_operativa_3325401,
                act_operativa_3325402=indicadores.inmunizaciones.act_operativa_3325402,
                act_operativa_3325403=indicadores.inmunizaciones.act_operativa_3325403,
                act_operativa_3325404=indicadores.inmunizaciones.act_operativa_3325404,
                act_operativa_3325405=indicadores.inmunizaciones.act_operativa_3325405,
                act_operativa_3325406=indicadores.inmunizaciones.act_operativa_3325406,
                act_operativa_3325407=indicadores.inmunizaciones.act_operativa_3325407,
                act_operativa_3325408=indicadores.inmunizaciones.act_operativa_3325408,
                act_operativa_3325508=indicadores.inmunizaciones.act_operativa_3325508,
            )
            try:
                self.historico_repo.guardar(historico)
            except Exception as exc:
                print(f"[Warning] No se pudo guardar el histórico en BD: {exc}")

        return indicadores
