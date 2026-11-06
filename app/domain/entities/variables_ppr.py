from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class VariablesPPR:

    Id_cita: str
    Fecha_Atencion: date
    Lote: str
    Id_ups: str
    Edad: int
    Tipo_Edad: str
    Codigo_Item: str
    Tipo_Diagnostico: str
    Valor_Lab: str | None = None
    Correlativo1: int | None = None
    Correlativo2: int | None = None
    Correlativo3: int | None = None
    Lab1: int | None = None
    Lab2: int | None = None
    Lab3: int | None = None
    
    
    def estandarizar_edad(self) -> int:
        if self.Tipo_Edad == "A":
            return self.Edad * 12
        elif self.Tipo_Edad == "M":
            return self.Edad
        elif self.Tipo_Edad == "D":
            return self.Edad // 30