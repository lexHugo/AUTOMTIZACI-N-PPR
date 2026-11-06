from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IndicadoresResponse(BaseModel):
    """Respuesta HTTP para el frontend con los 9 indicadores calculados."""
    act_operativa_3325401: str
    act_operativa_3325402: str
    act_operativa_3325403: str
    act_operativa_3325404: str
    act_operativa_3325405: str
    act_operativa_3325406: str
    act_operativa_3325407: str
    act_operativa_3325408: str
    act_operativa_3325508: str

    model_config = {
        "from_attributes": True
    }


class HistoricoPPRResponse(BaseModel):
    """Respuesta para listar ejecuciones históricas guardadas en SQL Server."""
    id: Optional[int] = None
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

    model_config = {
        "from_attributes": True
    }
