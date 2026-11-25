from collections import defaultdict
from typing import Dict, List, Optional, Set, Any
from app.domain.entities.variables_ppr import VariablesPPR

# Catálogo oficial de Unidades Productoras de Servicios (UPS) de MINSA
CATALOGO_UPS: Dict[str, str] = {
    "303712": "Pediatría",
    "301204": "Inmunizaciones (Vacunas)",
    "301202": "Control de Crecimiento y Desarrollo (CRED)",
    "301203": "Estimulación Temprana",
    "303701": "Medicina General",
    "303702": "Medicina Interna",
    "301301": "Nutrición",
    "301302": "Psicología",
    "301303": "Odontología",
    "301304": "Servicio Social",
    "304101": "Emergencia Pediátrica",
    "304102": "Emergencia General",
    "304201": "Hospitalización Pediatría",
    "304202": "Neonatología / UCI Neonatal",
}


class PPR1001SeguimientoService:
    """
    Servicio de Cálculo de Seguimiento y Producción de Atenciones por Servicio (UPS).
    
    Regla Técnica:
    - Se cuenta una sola vez cada cita médica (Id_cita único) para evitar inflar atenciones
      por diagnósticos o procedimientos múltiples.
    - Se clasifica y desglosa mes a mes para cada UPS.
    - Aplica la Alternativa B: Relleno continuo de meses entre el inicio y fin del período.
    - Soporta filtro estricto por profesional (médicos / enfermeras).
    """

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
    ) -> Dict[str, Any]:
        """
        Calcula el número de atenciones (citas únicas) agrupadas por UPS y mes.
        
        Args:
            variables: Lista de registros del HIS.
            ids_personal_permitidos: Conjunto opcional de Id_Personal válidos (ej: solo médicos).
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
                    "id_personal": v.Id_Personal or "",
                }

        # 2. Si se especificó un filtro de personal (ej: solo médicos), aplicar filtro
        total_evaluadas = len(citas_unicas)
        citas_filtradas = []
        descartadas_no_cumplen = 0

        for cita_id, info in citas_unicas.items():
            if ids_personal_permitidos is not None:
                if info["id_personal"] not in ids_personal_permitidos:
                    descartadas_no_cumplen += 1
                    continue
            citas_filtradas.append(info)

        # 3. Detectar meses continuos (Alternativa B) y lista de UPS presentes
        meses_con_datos = {c["periodo"] for c in citas_filtradas if c["periodo"] != "Sin fecha"}
        meses_continuos = self._generar_rango_meses_continuo(list(meses_con_datos))
        meses_faltantes = [m for m in meses_continuos if m not in meses_con_datos]

        meses_matriz = list(meses_continuos)
        if any(c["periodo"] == "Sin fecha" for c in citas_filtradas):
            meses_matriz.append("Sin fecha")

        # 4. Agrupar atenciones por (UPS, mes)
        conteo_ups_mes = defaultdict(lambda: defaultdict(int))
        for c in citas_filtradas:
            conteo_ups_mes[c["id_ups"]][c["periodo"]] += 1

        # 5. Armar matriz de resultados por UPS ordenada por volumen
        todas_las_ups = sorted(
            conteo_ups_mes.keys(),
            key=lambda u: sum(conteo_ups_mes[u].values()),
            reverse=True,
        )

        filas_ups = []
        totales_por_mes = {m: 0 for m in meses_matriz}
        gran_total = 0

        for ups_cod in todas_las_ups:
            nombre_servicio = CATALOGO_UPS.get(ups_cod, f"Servicio {ups_cod}")
            datos_meses = {}
            total_ups = 0

            for m in meses_matriz:
                cant = conteo_ups_mes[ups_cod].get(m, 0)
                datos_meses[m] = cant
                total_ups += cant
                totales_por_mes[m] += cant

            gran_total += total_ups

            filas_ups.append({
                "codigo_ups": ups_cod,
                "nombre_servicio": nombre_servicio,
                "mensual": datos_meses,
                "total_acumulado": total_ups,
            })

        return {
            "resumen_kpi": {
                "total_citas_evaluadas": total_evaluadas,
                "atenciones_validadas": len(citas_filtradas),
                "atenciones_descartadas": descartadas_no_cumplen,
                "total_ups_activas": len(filas_ups),
            },
            "meses": meses_matriz,
            "meses_faltantes": meses_faltantes,
            "filas": filas_ups,
            "totales_por_mes": totales_por_mes,
            "gran_total": gran_total,
        }
