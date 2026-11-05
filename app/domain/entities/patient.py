from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Patient:
    """
    Entidad pura del Dominio: Paciente Pediátrico.
    No depende de ningún framework, ORM ni base de datos.
    """
    first_name: str
    last_name: str
    birth_date: date
    medical_record_number: str
    guardian_name: str
    guardian_phone: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def calculate_age_in_years(self) -> int:
        """Calcula la edad en años del paciente."""
        today = date.today()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    def is_pediatric(self) -> bool:
        """Regla de negocio: Un paciente pediátrico suele tener menos de 18 años."""
        return self.calculate_age_in_years() < 18
