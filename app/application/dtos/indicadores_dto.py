from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class IndicadorVacunasDTO:
    """Actividades Operativas de Inmunizaciones (Vacunas y CRED)."""
    act_operativa_3325401: str = "0"
    act_operativa_3325402: str = "0"
    act_operativa_3325403: str = "0"
    act_operativa_3325404: str = "0"
    act_operativa_3325405: str = "0"
    act_operativa_3325406: str = "0"
    act_operativa_3325407: str = "0"
    act_operativa_3325408: str = "0"
    act_operativa_3325508: str = "0"


@dataclass
class IndicadorPediatriaDTO:
    """Actividades Operativas de Pediatría (Atenciones Médicas / Morbilidad)."""
    act_operativa_3331501: str = "0"       # Anemia
    act_operativa_3341401: str = "0"       # Parasitosis Intestinal
    act_operativa_3331101: str = "0"       # IRA no complicada
    act_operativa_3331102: str = "0"       # FAPA
    act_operativa_3331103: str = "0"       # OMA
    act_operativa_3331104: str = "0"       # Sinusitis aguda
    act_operativa_3331105: str = "0"       # Neumonía sin complicaciones
    act_operativa_nuemonia: str = "0"      # Neumonía con complicaciones
    act_operativa_3331301: str = "0"       # Neumonía muy grave < 2 meses
    act_operativa_3331305: str = "0"       # Neumonía muy grave 2m a 4a
    act_operativa_3331502: str = "0"       # SOBA / ASMA
    act_operativa_3331201: str = "0"       # EDA no complicada
    act_operativa_3331203: str = "0"       # EDA disentérica
    act_operativa_3331204: str = "0"       # EDA persistente
    act_operativa_3331401: str = "0"       # EDA con deshidratación
    act_operativa_3331305_shock: str = "0" # EDA con deshidratación y shock


@dataclass
class IndicadorDTO:
    """
    Consolidado general PPR1001 que agrupa por separado:
    - Inmunizaciones (ppr1001_vacunas.py)
    - Pediatría (ppr1001_pediatria.py)
    """
    inmunizaciones: IndicadorVacunasDTO = field(default_factory=IndicadorVacunasDTO)
    pediatria: IndicadorPediatriaDTO = field(default_factory=IndicadorPediatriaDTO)

    # Delegación de accesos directos por compatibilidad
    @property
    def act_operativa_3325401(self) -> str:
        return self.inmunizaciones.act_operativa_3325401

    @property
    def act_operativa_3325402(self) -> str:
        return self.inmunizaciones.act_operativa_3325402

    @property
    def act_operativa_3325403(self) -> str:
        return self.inmunizaciones.act_operativa_3325403

    @property
    def act_operativa_3325404(self) -> str:
        return self.inmunizaciones.act_operativa_3325404

    @property
    def act_operativa_3325405(self) -> str:
        return self.inmunizaciones.act_operativa_3325405

    @property
    def act_operativa_3325406(self) -> str:
        return self.inmunizaciones.act_operativa_3325406

    @property
    def act_operativa_3325407(self) -> str:
        return self.inmunizaciones.act_operativa_3325407

    @property
    def act_operativa_3325408(self) -> str:
        return self.inmunizaciones.act_operativa_3325408

    @property
    def act_operativa_3325508(self) -> str:
        return self.inmunizaciones.act_operativa_3325508
