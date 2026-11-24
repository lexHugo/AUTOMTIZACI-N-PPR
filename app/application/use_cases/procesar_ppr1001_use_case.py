from collections import defaultdict
from datetime import datetime
from typing import Any, Optional, List
from app.application.dtos.indicadores_dto import (
    IndicadorDTO,
    IndicadorVacunasDTO,
    IndicadorPediatriaDTO,
    ResumenPeriodoDTO,
)
from app.application.ports.his_excel_reader_port import HISExcelReaderPort
from app.application.ports.ppr_calculator_port import PPRCalculatorPort
from app.domain.entities.variables_ppr import VariablesPPR
from app.domain.entities.historico_ppr import HistoricoPPR
from app.domain.repositories.historico_ppr_repository import HistoricoPPRRepositoryInterface
from app.domain.repositories.datamart_repository import DataMartRepositoryInterface


class ProcesarPPR1001UseCase:
    """
    Caso de Uso Principal:
    Orquesta el flujo completo de:
    1. Lectura y filtrado del archivo Excel HIS.
    2. Persistencia y desduplicación en el Data Mart (SQLite/SQL Server).
    3. Recuperación de variables acumuladas multimensuales.
    4. Agrupamiento en memoria por cita (UNA SOLA VEZ).
    5. Cálculo de actividades de Inmunizaciones (ppr1001_vacunas.py).
    6. Cálculo de actividades de Pediatría (ppr1001_pediatria.py).
    7. Consolidación separada de ambos bloques en IndicadorDTO por cada mes detectado.
    8. Persistencia histórica opcional.
    """

    def __init__(
        self,
        his_reader: HISExcelReaderPort,
        vacunas_calculator: PPRCalculatorPort,
        pediatria_calculator: Optional[PPRCalculatorPort] = None,
        historico_repo: Optional[HistoricoPPRRepositoryInterface] = None,
        datamart_repo: Optional[DataMartRepositoryInterface] = None,
    ):
        self.his_reader = his_reader
        self.vacunas_calculator = vacunas_calculator
        self.pediatria_calculator = pediatria_calculator
        self.historico_repo = historico_repo
        self.datamart_repo = datamart_repo

    def execute(
        self,
        file_content: bytes,
        nombre_archivo: str = "trama_his.xlsx",
        guardar_en_datamart: bool = True,
    ) -> IndicadorDTO:
        # 1. Leer y filtrar el archivo (Excel/CSV) a lista de entidades VariablesPPR
        variables = self.his_reader.read_his_excel(file_content, filename=nombre_archivo)

        # 2. Persistencia y acumulación en Data Mart si está activo
        if self.datamart_repo and guardar_en_datamart:
            tipo_formato = "CSV" if nombre_archivo.lower().endswith(".csv") else "EXCEL"
            self.datamart_repo.guardar_trama(
                nombre_archivo=nombre_archivo,
                tipo_formato=tipo_formato,
                variables=variables,
            )
            # Recuperar universo acumulado de variables de todos los periodos registrados
            variables = self.datamart_repo.obtener_variables_acumuladas()

        # 3. Calcular indicadores sobre las variables resultantes
        indicadores = self.calcular_desde_variables(variables)

        # 4. Guardar histórico si el repo está configurado
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

    @staticmethod
    def _generar_rango_meses_continuo(meses_con_datos: List[str]) -> List[str]:
        """
        Genera la secuencia continua de meses 'YYYY-MM' entre el mes mínimo y el mes máximo detectados.
        Garantiza que la matriz no tenga huecos y muestre los meses faltantes con valor cero.
        """
        periodos_validos = []
        for m in meses_con_datos:
            try:
                parts = m.split("-")
                if len(parts) == 2:
                    y, m_int = int(parts[0]), int(parts[1])
                    if 1 <= m_int <= 12:
                        periodos_validos.append((y, m_int))
            except (ValueError, TypeError):
                continue

        if not periodos_validos:
            return sorted(meses_con_datos)

        periodos_validos.sort()
        min_y, min_m = periodos_validos[0]
        max_y, max_m = periodos_validos[-1]

        meses_continuos = []
        curr_y, curr_m = min_y, min_m
        while (curr_y < max_y) or (curr_y == max_y and curr_m <= max_m):
            meses_continuos.append(f"{curr_y:04d}-{curr_m:02d}")
            curr_m += 1
            if curr_m > 12:
                curr_m = 1
                curr_y += 1

        return meses_continuos

    def calcular_desde_variables(self, variables: List[VariablesPPR]) -> IndicadorDTO:
        """
        Agrupa variables por cita y calcula indicadores para el Total General y para cada mes.
        Aplica la Alternativa B: Relleno continuo de meses entre el inicio y fin para evidenciar meses faltantes.
        """
        citas_total = defaultdict(list)
        citas_por_mes = defaultdict(lambda: defaultdict(list))

        for v in variables:
            citas_total[v.Id_cita].append(v)
            if v.Fecha_Atencion:
                periodo = v.Fecha_Atencion.strftime("%Y-%m")
            else:
                periodo = "Sin fecha"
            citas_por_mes[periodo][v.Id_cita].append(v)

        # 1. Total General Inmunizaciones
        inm_dto = self.vacunas_calculator.calcular_todos(citas_total)
        if not isinstance(inm_dto, IndicadorVacunasDTO):
            if hasattr(inm_dto, "inmunizaciones"):
                inm_dto = inm_dto.inmunizaciones

        # 2. Total General Pediatría
        ped_dto = IndicadorPediatriaDTO()
        if self.pediatria_calculator:
            ped_dto = self.pediatria_calculator.calcular_todos(citas_total)
            if hasattr(ped_dto, "pediatria"):
                ped_dto = ped_dto.pediatria

        # 3. Desglose Mensual Continuo (Alternativa B: Detección y relleno de meses faltantes)
        meses_reales = {k for k in citas_por_mes.keys() if k != "Sin fecha"}
        meses_continuos = self._generar_rango_meses_continuo(list(meses_reales))
        
        # Identificar qué meses están ausentes en los datos registrados (meses hueco/pendientes)
        meses_faltantes = [m for m in meses_continuos if m not in meses_reales]

        # Si hay citas sin fecha identificable, se agregan al final
        meses_para_matriz = list(meses_continuos)
        if "Sin fecha" in citas_por_mes:
            meses_para_matriz.append("Sin fecha")

        mensual_dict = {}
        for mes in meses_para_matriz:
            citas_m = citas_por_mes.get(mes, {})

            inm_m = self.vacunas_calculator.calcular_todos(citas_m)
            if not isinstance(inm_m, IndicadorVacunasDTO) and hasattr(inm_m, "inmunizaciones"):
                inm_m = inm_m.inmunizaciones

            ped_m = IndicadorPediatriaDTO()
            if self.pediatria_calculator:
                ped_m = self.pediatria_calculator.calcular_todos(citas_m)
                if hasattr(ped_m, "pediatria"):
                    ped_m = ped_m.pediatria

            mensual_dict[mes] = ResumenPeriodoDTO(
                inmunizaciones=inm_m,
                pediatria=ped_m,
            )

        return IndicadorDTO(
            inmunizaciones=inm_dto,
            pediatria=ped_dto,
            mensual=mensual_dict,
            meses=meses_para_matriz,
            meses_faltantes=meses_faltantes,
        )

    def obtener_resumen_acumulado(
        self,
        meses: Optional[List[str]] = None,
        anio: Optional[int] = None,
    ) -> IndicadorDTO:
        """
        Calcula y retorna indicadores acumulados desde el Data Mart sin requerir carga de archivo.
        """
        if not self.datamart_repo:
            raise ValueError("El repositorio de Data Mart no está configurado.")
        variables = self.datamart_repo.obtener_variables_acumuladas(meses=meses, anio=anio)
        return self.calcular_desde_variables(variables)
