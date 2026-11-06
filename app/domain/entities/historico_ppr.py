from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HistoricoPPR:
    """
    Entidad pura del Dominio: Almacena el histórico de indicadores calculados para el PPR1001.
    """
    fecha_procesamiento: datetime
    nombre_archivo: str
    act_operativa_3325401: str
    act_operativa_3325402: str
    act_operativa_3325403: str
    act_operativa_3325404: str
    act_operativa_3325405: str
    act_operativa_3325406: str
    act_operativa_3325407: str
    act_operativa_3325408: str
    act_operativa_3325508: str
    id: Optional[int] = None
