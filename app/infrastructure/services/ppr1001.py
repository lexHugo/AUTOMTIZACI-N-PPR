from collections import defaultdict
from typing import Dict, List, Optional, Set
from app.domain.entities.variables_ppr import VariablesPPR
from app.application.dtos.indicadores_dto import IndicadorDTO
from app.application.ports.ppr1001_interface import PPR1001Interface


class PPR1001Service(PPR1001Interface):
    """
    Servicio de cálculo de las 9 Actividades Operativas del PPR1001
    según las especificaciones técnicas oficiales de HIS MINSA.
    """

    @staticmethod
    def _agrupar_por_cita(variables: List[VariablesPPR]) -> Dict[str, List[VariablesPPR]]:
        """Agrupa los registros del HIS por Id_cita."""
        citas = defaultdict(list)
        for v in variables:
            citas[v.Id_cita].append(v)
        return citas

    @staticmethod
    def _norm(val: Optional[str]) -> str:
        """Normaliza cadenas a mayúsculas sin espacios extremos."""
        return val.strip().upper() if val else ""

    # =========================================================================
    # AO: 3325401 - VACUNACION NINO < 1 ANO (PENTAVALENTE 3)
    # =========================================================================
    def calcular_3325401(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        cpt_validos: Set[str] = {"90723", "90722"}
        labs_validos: Set[str] = {"3", "D3", "B3"}
        cumplen = 0

        for items in citas.values():
            if any(
                item.edad_en_meses() < 12
                and self._norm(item.Codigo_Item) in cpt_validos
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            ):
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325402 - VACUNACION NINO = 1 ANO (SPR 1)
    # =========================================================================
    def calcular_3325402(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        labs_validos: Set[str] = {"1", "D1", "B1"}
        cumplen = 0

        for items in citas.values():
            if any(
                (item.edad_en_anios() == 1 or 12 <= item.edad_en_meses() <= 23)
                and self._norm(item.Codigo_Item) == "90707"
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            ):
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325403 - VACUNACION NINO = 4 ANOS (2º REFUERZO DPT)
    # =========================================================================
    def calcular_3325403(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        labs_validos: Set[str] = {"DA", "DDA", "BDA"}
        cumplen = 0

        for items in citas.values():
            if any(
                (item.edad_en_anios() == 4 or 48 <= item.edad_en_meses() <= 59)
                and self._norm(item.Codigo_Item) == "90701"
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            ):
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325404 - VACUNACION NINO RECIEN NACIDO (BCG + HvB)
    # =========================================================================
    def calcular_3325404(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        labs_validos: Set[str] = {"", "1", "DU", "BU"}
        cumplen = 0

        for items in citas.values():
            tiene_bcg = any(
                item.edad_en_dias() <= 28
                and self._norm(item.Codigo_Item) == "90585"
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            )
            tiene_hvb = any(
                item.edad_en_dias() <= 28
                and self._norm(item.Codigo_Item) == "90744"
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            )
            if tiene_bcg and tiene_hvb:
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325405 - VACUNACION NINO = 2 ANOS (INFLUENZA PEDIATRICA)
    # =========================================================================
    def calcular_3325405(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        labs_validos: Set[str] = {"", "1", "DU", "BU"}
        cumplen = 0

        for items in citas.values():
            if any(
                (item.edad_en_anios() == 2 or 24 <= item.edad_en_meses() <= 35)
                and self._norm(item.Codigo_Item) == "90657"
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            ):
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325406 - VACUNACION NINO = 3 ANOS (INFLUENZA)
    # =========================================================================
    def calcular_3325406(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        cpt_validos: Set[str] = {"90658", "90657"}
        labs_validos: Set[str] = {"", "1", "DU", "BU"}
        cumplen = 0

        for items in citas.values():
            if any(
                (item.edad_en_anios() == 3 or 36 <= item.edad_en_meses() <= 47)
                and self._norm(item.Codigo_Item) in cpt_validos
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            ):
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325407 - VACUNACION NINO DE MADRE CON VIH (NEUMOCOCO 3)
    # =========================================================================
    def calcular_3325407(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        cie_vih: Set[str] = {"Z206", "22061", "Z21X1", "Z21X"}
        labs_validos: Set[str] = {"3", "D3", "B3"}
        cumplen = 0

        for items in citas.values():
            # 1. Verificar dosis de Neumococo 3 en menor de 1 año
            tiene_neumococo = any(
                item.edad_en_meses() < 12
                and self._norm(item.Codigo_Item) == "90670"
                and self._norm(item.Tipo_Diagnostico) == "D"
                and self._norm(item.Valor_Lab) in labs_validos
                for item in items
            )

            # 2. Verificar comorbilidad asociada VIH en la misma cita
            tiene_comorbilidad = any(
                self._norm(item.Codigo_Item) in cie_vih
                and self._norm(item.Tipo_Diagnostico) in {"D", "R"}
                for item in items
            )

            if tiene_neumococo and tiene_comorbilidad:
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325408 - ATENCION DE EVENTOS ADVERSOS A VACUNAS (ESAVI)
    # =========================================================================
    def calcular_3325408(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        cie_esavi: Set[str] = {"T881", "Y590", "Y599"}
        cpt_reaccion: Set[str] = {"90702", "90744", "90648"}
        cumplen = 0

        for items in citas.values():
            es_esavi = any(
                (self._norm(item.Codigo_Item) in cie_esavi and self._norm(item.Tipo_Diagnostico) in {"P", "D", "R"})
                or (self._norm(item.Codigo_Item) in cpt_reaccion and self._norm(item.Valor_Lab) in {"2", "3"})
                for item in items
            )
            if es_esavi:
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # AO: 3325508 - SEGUIMIENTO DEL NINO Y NINA DE ALTO RIESGO
    # =========================================================================
    def calcular_3325508(self, variables: List[VariablesPPR]) -> str:
        citas = self._agrupar_por_cita(variables)
        labs_cred: Set[str] = {"1", "2", "3", "4", "5"}
        cumplen = 0

        for items in citas.values():
            es_alto_riesgo = any(
                (
                    self._norm(item.Id_ups) == "301202"
                    and self._norm(item.Codigo_Item) == "Z001"
                    and self._norm(item.Tipo_Diagnostico) in {"D", "R"}
                )
                or (
                    self._norm(item.Codigo_Item) == "99344"
                    and self._norm(item.Tipo_Diagnostico) == "D"
                    and self._norm(item.Valor_Lab) in labs_cred
                )
                for item in items
            )
            if es_alto_riesgo:
                cumplen += 1

        return str(cumplen)

    # =========================================================================
    # CONSOLIDADOR GENERAL
    # =========================================================================
    def calcular_todos(self, variables: List[VariablesPPR]) -> IndicadorDTO:
        """
        Ejecuta todas las fórmulas sobre las variables procesadas del Excel
        y consolida los resultados en el IndicadorDTO.
        """
        return IndicadorDTO(
            act_operativa_3325401=self.calcular_3325401(variables),
            act_operativa_3325402=self.calcular_3325402(variables),
            act_operativa_3325403=self.calcular_3325403(variables),
            act_operativa_3325404=self.calcular_3325404(variables),
            act_operativa_3325405=self.calcular_3325405(variables),
            act_operativa_3325406=self.calcular_3325406(variables),
            act_operativa_3325407=self.calcular_3325407(variables),
            act_operativa_3325408=self.calcular_3325408(variables),
            act_operativa_3325508=self.calcular_3325508(variables),
        )
