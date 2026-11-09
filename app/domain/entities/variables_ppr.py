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
    Id_Correlativo: Optional[int] = None      # Posición correlativa del ítem/diagnóstico (1, 2, ..., 7...)
    Id_Correlativo_Lab: Optional[int] = None  # Posición correlativa del laboratorio (1, 2, 3...)

    def estandarizar_edad(self) -> int:
        """Alias para obtener la edad en meses."""
        return self.edad_en_meses()

    def edad_en_meses(self) -> int:
        """Retorna la edad calculada en meses completos."""
        tipo = self.Tipo_Edad.strip().upper() if self.Tipo_Edad else ""
        if tipo == "A":
            return self.Edad * 12
        elif tipo == "M":
            return self.Edad
        elif tipo == "D":
            return self.Edad // 30
        return self.Edad

    def edad_en_dias(self) -> int:
        """Retorna la edad calculada en días."""
        tipo = self.Tipo_Edad.strip().upper() if self.Tipo_Edad else ""
        if tipo == "D":
            return self.Edad
        elif tipo == "M":
            return self.Edad * 30
        elif tipo == "A":
            return self.Edad * 365
        return self.Edad

    def edad_en_anios(self) -> int:
        """Retorna la edad calculada en años completos."""
        tipo = self.Tipo_Edad.strip().upper() if self.Tipo_Edad else ""
        if tipo == "A":
            return self.Edad
        elif tipo == "M":
            return self.Edad // 12
        elif tipo == "D":
            return self.Edad // 365
        return self.Edad
