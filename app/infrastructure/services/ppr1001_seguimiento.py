from collections import defaultdict
from typing import Dict, List, Optional, Set, Any
from app.domain.entities.variables_ppr import VariablesPPR

# Conjunto de UPS que consolidan el Servicio de Pediatría:
# Incluye la lista explícita indicada ('303701', '303703', '300704', '300706', '300708', '300709', '300705', '300710', '300712', '304002', '304103')
# y sus variantes de codificación equivalentes en el registro HIS MINSA (3037xx / 3007xx).
UPS_PEDIATRIA: Set[str] = {
    "303705", "303708", "303703", "303704", "303712", "303701"
}

# Conjunto de UPS que corresponden al Servicio de Neonatología
UPS_NEONATOLOGIA: Set[str] = {
    "303707", "300707", "304202",
}


class PPR1001SeguimientoService:
    """
    Servicio de Cálculo de Seguimiento y Producción de Atenciones por Servicio.
    
    Regla Técnica:
    - Se muestran ÚNICAMENTE los servicios de Pediatría y Neonatología.
    - Pediatría es la suma de las citas obtenidas de las UPS pediátricas definidas.
    - Se cuenta una sola vez cada cita médica (Id_cita único) para evitar inflar atenciones.
    - Aplica la Alternativa B: Relleno continuo de meses entre el inicio y fin del período.
    - Soporta filtro estricto por profesional y exclusión del código 29.
    """

    UPS_PEDIATRIA = UPS_PEDIATRIA
    UPS_NEONATOLOGIA = UPS_NEONATOLOGIA

    @staticmethod
    def _generar_rango_meses_continuo(meses_con_datos: List[str]) -> List[str]:
        """Genera el rango continuo de meses YYYY-MM entre el mes mínimo y máximo."""
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

    def calcular_atenciones_por_ups(
        self,
        variables: List[VariablesPPR],
        ids_personal_permitidos: Optional[Set[str]] = None,
        ids_personal_excluidos: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        """
        Calcula el número de atenciones (citas únicas) para Pediatría y Neonatología por mes.
        
        Args:
            variables: Lista de registros del HIS.
            ids_personal_permitidos: Conjunto opcional de Id_Personal válidos (ej: solo médicos).
            ids_personal_excluidos: Conjunto opcional de Id_Personal excluidos (ej: código profesión 29).
        """
        # 1. Deduplicar citas: Extraer la cabecera única de cada Id_cita
        citas_unicas: Dict[str, Dict[str, Any]] = {}

        for v in variables:
            if not v.Id_cita:
                continue

            if v.Id_cita not in citas_unicas:
                periodo = (
                    v.Fecha_Atencion.strftime("%Y-%m")
                    if v.Fecha_Atencion
                    else "Sin fecha"
                )
                ups = str(v.Id_ups).strip() if v.Id_ups else "SIN_UPS"
                citas_unicas[v.Id_cita] = {
                    "id_ups": ups,
                    "periodo": periodo,
                    "id_personal": str(v.Id_Personal).strip() if v.Id_Personal else "",
                }

        # 2. Filtrado:
        # - Exclusión obligatoria (ej: personal código 29)
        # - Filtro restrictivo de profesión (si fue seleccionado)
        # - Filtro de servicios: ÚNICAMENTE Pediatría y Neonatología
        total_evaluadas = len(citas_unicas)
        citas_clasificadas = []
        descartadas_no_cumplen = 0

        for cita_id, info in citas_unicas.items():
            id_p = info["id_personal"]
            ups = info["id_ups"]
            
            # Exclusión de código 29
            if ids_personal_excluidos and id_p in ids_personal_excluidos:
                descartadas_no_cumplen += 1
                continue

            # Filtro restrictivo de profesión
            if ids_personal_permitidos is not None:
                if id_p not in ids_personal_permitidos:
                    descartadas_no_cumplen += 1
                    continue

            # Clasificación de Servicio (Solo Pediatría y Neonatología)
            if ups in self.UPS_PEDIATRIA:
                citas_clasificadas.append({
                    "servicio_key": "PEDIATRIA",
                    "periodo": info["periodo"],
                })
            elif ups in self.UPS_NEONATOLOGIA:
                citas_clasificadas.append({
                    "servicio_key": "NEONATOLOGIA",
                    "periodo": info["periodo"],
                })
            else:
                # Cualquier otra UPS queda descartada del reporte
                descartadas_no_cumplen += 1

        # 3. Detectar meses continuos (Alternativa B) y brechas
        meses_con_datos = {c["periodo"] for c in citas_clasificadas if c["periodo"] != "Sin fecha"}
        meses_continuos = self._generar_rango_meses_continuo(list(meses_con_datos))
        meses_faltantes = [m for m in meses_continuos if m not in meses_con_datos]

        meses_matriz = list(meses_continuos)
        if any(c["periodo"] == "Sin fecha" for c in citas_clasificadas):
            meses_matriz.append("Sin fecha")

        # 4. Agrupar atenciones por (Servicio, mes)
        conteo_servicio_mes = defaultdict(lambda: defaultdict(int))
        for c in citas_clasificadas:
            conteo_servicio_mes[c["servicio_key"]][c["periodo"]] += 1

        # 5. Generar exactamente las dos filas: Pediatría y Neonatología
        servicios_definidos = [
            {
                "servicio_key": "PEDIATRIA",
                "codigo_ups": "PEDIATRÍA",
                "nombre_servicio": "Pediatría",
            },
            {
                "servicio_key": "NEONATOLOGIA",
                "codigo_ups": "303707",
                "nombre_servicio": "Neonatología",
            },
        ]

        filas_ups = []
        totales_por_mes = {m: 0 for m in meses_matriz}
        gran_total = 0

        for serv in servicios_definidos:
            s_key = serv["servicio_key"]
            datos_meses = {}
            total_serv = 0

            for m in meses_matriz:
                cant = conteo_servicio_mes[s_key].get(m, 0)
                datos_meses[m] = cant
                total_serv += cant
                totales_por_mes[m] += cant

            gran_total += total_serv

            filas_ups.append({
                "codigo_ups": serv["codigo_ups"],
                "nombre_servicio": serv["nombre_servicio"],
                "mensual": datos_meses,
                "total_acumulado": total_serv,
            })

        return {
            "resumen_kpi": {
                "total_citas_evaluadas": total_evaluadas,
                "atenciones_validadas": len(citas_clasificadas),
                "atenciones_descartadas": descartadas_no_cumplen,
                "total_ups_activas": len([f for f in filas_ups if f["total_acumulado"] > 0]),
            },
            "meses": meses_matriz,
            "meses_faltantes": meses_faltantes,
            "filas": filas_ups,
            "totales_por_mes": totales_por_mes,
            "gran_total": gran_total,
        }

    def calcular_desde_resumen_db(
        self,
        resumen_db: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Procesa el resumen agregado directamente desde SQLite (Opción 1).
        Evita instanciar cientos de miles de entidades de dominio en memoria RAM.
        
        Args:
            resumen_db: Dict con 'total_evaluadas' y 'desglose' [{'id_ups': ..., 'mes': ..., 'total': ...}].
        """
        total_evaluadas = resumen_db.get("total_evaluadas", 0)
        desglose = resumen_db.get("desglose", [])

        # 1. Agrupar por Servicio (Pediatría / Neonatología) y Mes
        conteo_servicio_mes = defaultdict(lambda: defaultdict(int))
        meses_con_datos = set()
        atenciones_validadas = 0

        for item in desglose:
            ups = str(item["id_ups"]).strip()
            mes = str(item["mes"]).strip()
            cant = int(item["total"])

            if ups in self.UPS_PEDIATRIA:
                s_key = "PEDIATRIA"
            elif ups in self.UPS_NEONATOLOGIA:
                s_key = "NEONATOLOGIA"
            else:
                continue

            conteo_servicio_mes[s_key][mes] += cant
            atenciones_validadas += cant
            if mes and mes != "Sin fecha":
                meses_con_datos.add(mes)

        # 2. Generar rango continuo de meses (Alternativa B) y detectar brechas
        meses_continuos = self._generar_rango_meses_continuo(list(meses_con_datos))
        meses_faltantes = [m for m in meses_continuos if m not in meses_con_datos]
        meses_matriz = list(meses_continuos)

        # 3. Filas finales: Pediatría y Neonatología
        servicios_definidos = [
            {
                "servicio_key": "PEDIATRIA",
                "codigo_ups": "PEDIATRÍA",
                "nombre_servicio": "Pediatría",
            },
            {
                "servicio_key": "NEONATOLOGIA",
                "codigo_ups": "303707",
                "nombre_servicio": "Neonatología",
            },
        ]

        filas_ups = []
        totales_por_mes = {m: 0 for m in meses_matriz}
        gran_total = 0

        for serv in servicios_definidos:
            s_key = serv["servicio_key"]
            datos_meses = {}
            total_serv = 0

            for m in meses_matriz:
                cant = conteo_servicio_mes[s_key].get(m, 0)
                datos_meses[m] = cant
                total_serv += cant
                totales_por_mes[m] += cant

            gran_total += total_serv

            filas_ups.append({
                "codigo_ups": serv["codigo_ups"],
                "nombre_servicio": serv["nombre_servicio"],
                "mensual": datos_meses,
                "total_acumulado": total_serv,
            })

        descartadas = max(0, total_evaluadas - atenciones_validadas)

        return {
            "resumen_kpi": {
                "total_citas_evaluadas": total_evaluadas,
                "atenciones_validadas": atenciones_validadas,
                "atenciones_descartadas": descartadas,
                "total_ups_activas": len([f for f in filas_ups if f["total_acumulado"] > 0]),
            },
            "meses": meses_matriz,
            "meses_faltantes": meses_faltantes,
            "filas": filas_ups,
            "totales_por_mes": totales_por_mes,
            "gran_total": gran_total,
        }
