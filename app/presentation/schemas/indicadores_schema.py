from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IndicadoresVacunasResponse(BaseModel):
    """Resultados de Actividades Operativas de Inmunizaciones (ppr1001_vacunas.py)."""
    act_operativa_3325401: str = "0"
    act_operativa_3325402: str = "0"
    act_operativa_3325403: str = "0"
    act_operativa_3325404: str = "0"
    act_operativa_3325405: str = "0"
    act_operativa_3325406: str = "0"
    act_operativa_3325407: str = "0"
    act_operativa_3325408: str = "0"
    act_operativa_3325508: str = "0"

    model_config = {
        "from_attributes": True
    }


class IndicadoresPediatriaResponse(BaseModel):
    """Resultados de Actividades Operativas de Pediatría (ppr1001_pediatria.py)."""
    act_operativa_3331501: str = "0"        # Anemia
    act_operativa_3341401: str = "0"        # Parasitosis Intestinal
    act_operativa_3331101: str = "0"        # IRA no complicada
    act_operativa_3331102: str = "0"        # FAPA
    act_operativa_3331103: str = "0"        # OMA
    act_operativa_3331104: str = "0"        # Sinusitis aguda
    act_operativa_3331105: str = "0"        # Neumonía sin complicaciones
    act_operativa_nuemonia: str = "0"       # Neumonía con complicaciones
    act_operativa_3331301: str = "0"        # Neumonía muy grave < 2 meses
    act_operativa_3331305: str = "0"        # Neumonía muy grave 2m a 4a
    act_operativa_3331502: str = "0"        # SOBA / ASMA
    act_operativa_3331201: str = "0"        # EDA no complicada
    act_operativa_3331203: str = "0"        # EDA disentérica
    act_operativa_3331204: str = "0"        # EDA persistente
    act_operativa_3331401: str = "0"        # EDA con deshidratación
    act_operativa_3331305_shock: str = "0"  # EDA con deshidratación y shock

    model_config = {
        "from_attributes": True
    }


class IndicadoresResponse(BaseModel):
    """Respuesta HTTP consolidada para el frontend, separando Inmunizaciones y Pediatría."""
    inmunizaciones: IndicadoresVacunasResponse
    pediatria: IndicadoresPediatriaResponse

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
