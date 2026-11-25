from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class VariablesPPR:
    """
    Entidad pura del dominio que representa una fila procesada de la trama HIS.
    Cada instancia corresponde a un ítem/diagnóstico registrado en una atención médica.
    """
    Id_cita: str
    Fecha_Atencion: date
    Lote: str
    Id_ups: str
    Edad: int
    Tipo_Edad: str  # "A" = Años, "M" = Meses, "D" = Días
    Codigo_Item: str
    Tipo_Diagnostico: str
    Valor_Lab: Optional[str] = None
    Id_Correlativo: Optional[int] = None  
    Id_Correlativo_Lab: Optional[int] = None 
    Id_Personal: Optional[str] = None 

    def estandarizar_edad(self) -> int:
        """Alias para obtener la edad en meses."""
        return self.edad_en_meses()

    def edad_en_meses(self) -> int:
        """Retorna la edad calculada en meses completos."""
        try:
            edad_num = int(self.Edad)
        except (ValueError, TypeError):
            return 0
        tipo = self.Tipo_Edad.strip().upper() if self.Tipo_Edad else ""
        if tipo == "A":
            return edad_num * 12
        elif tipo == "M":
            return edad_num
        elif tipo == "D":
            return edad_num // 30
        return edad_num

    def edad_en_dias(self) -> int:
        """Retorna la edad calculada en días."""
        try:
            edad_num = int(self.Edad)
        except (ValueError, TypeError):
            return 0
        tipo = self.Tipo_Edad.strip().upper() if self.Tipo_Edad else ""
        if tipo == "D":
            return edad_num
        elif tipo == "M":
            return edad_num * 30
        elif tipo == "A":
            return edad_num * 365
        return edad_num

    def edad_en_anios(self) -> int:
        """Retorna la edad calculada en años completos."""
        try:
            edad_num = int(self.Edad)
        except (ValueError, TypeError):
            return 0
        tipo = self.Tipo_Edad.strip().upper() if self.Tipo_Edad else ""
        if tipo == "A":
            return edad_num
        elif tipo == "M":
            return edad_num // 12
        elif tipo == "D":
            return edad_num // 365
        return edad_num
