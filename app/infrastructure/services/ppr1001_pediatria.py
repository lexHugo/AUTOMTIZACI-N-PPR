from collections import defaultdict
from typing import Callable, Dict, List, Optional, Set, Union
from app.domain.entities.variables_ppr import VariablesPPR
from app.application.dtos.indicadores_dto import IndicadorPediatriaDTO
from app.application.ports.ppr_calculator_port import PPRCalculatorPort


class PPR1001_Atenciones_Service(PPRCalculatorPort):
    """
    Servicio de cálculo de Actividades Operativas de Pediatría (Atenciones Médicas)
    para el Programa Presupuestal PPR1001 según normas técnicas del MINSA.
    
    Lógica de procesamiento:
    - Se procesan todas las citas sin importar el paciente.
    - Se contabilizan las apariciones de cada código CIE-10 definido para cada método.
    - Cuando todos los códigos de un método alcancen como mínimo 1 unidad, se incrementa
      el contador principal 'cumplen' (según la cantidad de unidades completas alcanzadas por todos).
    - Los conteos individuales de cada CIE-10 quedan guardados en 'self.conteos_cie'.
    """
    #ups: str = "303712"
    #ups: Set[str] = {"301204", "301202", "303712", "303305","303604","303701","303702","303703","303704","303705","303706","303707","303708","303709","303710","303711","304002","304103"}

    def __init__(self):
        # Almacena el conteo individual de cada código CIE-10 por cada actividad operativa
        self.conteos_cie: Dict[str, Dict[str, int]] = {}

    @staticmethod
    def _agrupar_por_cita(variables: List[VariablesPPR]) -> Dict[str, List[VariablesPPR]]:
        """Agrupa los registros del HIS por Id_cita."""
        citas = defaultdict(list)
        for v in variables:
            citas[v.Id_cita].append(v)
        return citas

    def _obtener_citas(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> Dict[str, List[VariablesPPR]]:
        """
        Retorna el diccionario de citas de forma eficiente:
        - Si ya viene agrupado (dict), lo usa directamente en O(1) tiempo sin re-agrupar.
        - Si viene como lista plana (list), lo agrupa una sola vez.
        """
        if isinstance(datos, dict):
            return datos
        return self._agrupar_por_cita(datos)

    @staticmethod
    def _norm(val: Optional[str]) -> str:
        """Normaliza cadenas a mayúsculas sin espacios extremos."""
        return val.strip().upper() if val else ""

    def _procesar_conteo_cie(
        self,
        datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]],
        cie_validos: Set[str],
        validador_edad: Callable[[VariablesPPR], bool],
        nombre_metodo: str = "",
    ) -> str:
        """
        Procesa todas las citas sin importar el paciente, contando las apariciones
        de cada código CIE-10. Cuando todos los códigos de un método lleguen a mínimo
        1 unidad, se incrementa su contador principal 'cumplen'.
        """
        citas = self._obtener_citas(datos)
        conteo_cie: Dict[str, int] = {cie: 0 for cie in cie_validos}

        # Procesar todas las citas y contar apariciones de cada CIE-10
        for items in citas.values():
            for item in items:
                if (
                    validador_edad(item)
                    #and self._norm(item.Id_ups) in self.ups
                    and self._norm(item.Tipo_Diagnostico) == "D"
                ):
                    codigo = self._norm(item.Codigo_Item)
                    if codigo in conteo_cie:
                        conteo_cie[codigo] += 1

        # Guardar el desglose detallado de CIE-10
        if nombre_metodo:
            self.conteos_cie[nombre_metodo] = conteo_cie

        # Cuando todos los códigos alcancen mínimo 1 unidad, sube el contador principal
        cumplen = min(conteo_cie.values()) if conteo_cie else 0
        return str(cumplen)

    # =========================================================================
    # AO: 3331501 - ENFERMEDADES PREVALENTES (ANEMIA)
    # =========================================================================
    def calcular_3331501(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"D509", "D649"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331501",
        )

    # =========================================================================
    # AO: 3341401 - ATEN. NIÑOS Y NIÑAS CON PARASITOSIS INTESTINAL
    # =========================================================================
    def calcular_3341401(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"B680", "B681", "B689", "B779", "B780", "B79", "B80", "A071", "A06", "B829"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3341401",
        )

    # =========================================================================
    # AO: 3331101 - IRA NO COMPLICADA - ATENCION IRA 
    # =========================================================================
    def calcular_3331101(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"J00X", "J040", "J041", "J042", "J060", "J068", "J069", "J209"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331101",
        )

    # =========================================================================
    # AO: 3331102 - FAPA - ATENCION IRA
    # =========================================================================
    def calcular_3331102(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"J020", "J029", "J030", "J038", "J039"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331102",
        )

    # =========================================================================
    # AO: 3331103 - OMA - ATENCION IRA
    # =========================================================================
    def calcular_3331103(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"H650", "H651", "H660", "H669"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331103",
        )

    # =========================================================================
    # AO: 3331104 - SINUSITIS AGUDA - ATENCION IRA
    # =========================================================================
    def calcular_3331104(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"J010", "J011", "J012", "J013", "J014", "J019"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331104",
        )

    # =========================================================================
    # AO: 3331105 - NEUMONIA SIN COMPLICACIONES Y OTROS - ATENCION IRA
    # =========================================================================
    def calcular_3331105(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"J129", "J159", "J181"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331105",
        )

    # =========================================================================
    # AO: NEUMONIA - IRA CON COMPLICACIONES
    # =========================================================================
    def calcular_neumonia(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "A369", "A370", "A371", "A378", "A379", "J120", "J121", "J122",
            "J123", "J128", "J13X", "J14X", "J150", "J151", "J152", "J153",
            "J154", "J157", "J158", "J160", "J168"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="neumonia",
        )

    # =========================================================================
    # AO: 3331301 - NEUMONIA MUY GRAVE EN NIÑOS < 2M - IRA CON COMPLICACIONES
    # =========================================================================    
    def calcular_3331301(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "J050", "J051", "J851", "J860", "J869", "J90X", "J939", "J100",
            "J110", "J155", "J156", "J180", "J181", "J182", "J188"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_meses() < 2,
            nombre_metodo="3331301",
        )

    # =========================================================================
    # AO: 3331305 - NEUMONIA MUY GRAVE EN NIÑOS 2M a 4A - IRA CON COMPLICACIONES
    # =========================================================================
    def calcular_3331305(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "J050", "J051", "J181", "J182", "J851", "J860", "J869", "J90X",
            "J939", "J100", "J110", "J155", "J156", "J180", "J181", "J182", "J188"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_meses() > 2 and item.edad_en_anios() < 5,
            nombre_metodo="3331305",
        )

    # =========================================================================
    # AO: 3331502 - SOBA/ASMA - IRA CON COMPLICACIONES
    # =========================================================================
    def calcular_3331502(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "J210", "J211", "J218", "J219", "J440", "J441", "J448", "J449",
            "J450", "J451", "J459", "J46X"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331502",
        )

    # =========================================================================
    # AO: 3331201 - EDA NO COMPLICADA - ATENCION EN EDA
    # =========================================================================    
    def calcular_3331201(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "A009", "A010", "A011", "A012", "A013", "A014", "A020", "A040",
            "A041", "A049", "A059", "A070", "A072", "A08", "A082", "A083",
            "A084", "A090", "A099"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331201",
        )

    # =========================================================================
    # AO: 3331203 - EDA DISENT - ATENCION EN EDA
    # =========================================================================    
    def calcular_3331203(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"A030", "A039", "A042", "A043", "A045", "A060"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331203",
        )

    # =========================================================================
    # AO: 3331204 - EDA PERST - ATENCION EN EDA
    # =========================================================================
    def calcular_3331204(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {"A09X"}
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331204",
        )

    # =========================================================================
    # AO: 3331401 - EDA CON DESH - ATENCION EN EDA CON COMPLICACIONES
    # =========================================================================    
    def calcular_3331401(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "A009", "A010", "A011", "A012", "A013", "A014", "A020", "A040",
            "A041", "A049", "A059", "A070", "A072", "A08", "A082", "A083",
            "A084", "A090", "A099", "E86X"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331401",
        )

    # =========================================================================
    # AO: 3331305 (SHOCK) - EDA CON DESH Y SHOCK - ATENCION EN EDA CON COMPLICACIONES
    # =========================================================================
    def calcular_3331305_shock(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> str:
        cie_validos: Set[str] = {
            "A009", "A010", "A011", "A012", "A013", "A014", "A020", "A040",
            "A041", "A049", "A059", "A070", "A072", "A08", "A082", "A083",
            "A084", "A090", "A099", "E86X", "R571", "E872", "K560"
        }
        return self._procesar_conteo_cie(
            datos=datos,
            cie_validos=cie_validos,
            validador_edad=lambda item: item.edad_en_anios() < 5,
            nombre_metodo="3331305_shock",
        )

    # =========================================================================
    # CONSOLIDADOR GENERAL (AGRUPA EXACTAMENTE 1 VEZ EN MEMORIA)
    # =========================================================================
    def calcular_todos(
        self, datos: Union[Dict[str, List[VariablesPPR]], List[VariablesPPR]]
    ) -> IndicadorPediatriaDTO:
        """
        Agrupa los datos UNA SOLA VEZ (o reutiliza el dict si ya viene agrupado)
        y ejecuta todas las fórmulas en O(1) para máxima velocidad y seguridad.
        """
        self.conteos_cie = {}
        citas = self._obtener_citas(datos)

        return IndicadorPediatriaDTO(
            act_operativa_3331501=self.calcular_3331501(citas),
            act_operativa_3341401=self.calcular_3341401(citas),
            act_operativa_3331101=self.calcular_3331101(citas),
            act_operativa_3331102=self.calcular_3331102(citas),
            act_operativa_3331103=self.calcular_3331103(citas),
            act_operativa_3331104=self.calcular_3331104(citas),
            act_operativa_3331105=self.calcular_3331105(citas),
            act_operativa_nuemonia=self.calcular_neumonia(citas),
            act_operativa_3331301=self.calcular_3331301(citas),
            act_operativa_3331305=self.calcular_3331305(citas),
            act_operativa_3331502=self.calcular_3331502(citas),
            act_operativa_3331201=self.calcular_3331201(citas),
            act_operativa_3331203=self.calcular_3331203(citas),
            act_operativa_3331204=self.calcular_3331204(citas),
            act_operativa_3331401=self.calcular_3331401(citas),
            act_operativa_3331305_shock=self.calcular_3331305_shock(citas),
            conteos_cie=dict(self.conteos_cie),
        )
