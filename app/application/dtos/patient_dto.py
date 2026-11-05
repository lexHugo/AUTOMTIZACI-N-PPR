from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional
from app.domain.entities.patient import Patient


@dataclass
class PatientCreateDTO:
    """Datos necesarios para registrar un nuevo paciente."""
    first_name: str
    last_name: str
    birth_date: date
    medical_record_number: str
    guardian_name: str
    guardian_phone: str

    def to_entity(self) -> Patient:
        return Patient(
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            medical_record_number=self.medical_record_number,
            guardian_name=self.guardian_name,
            guardian_phone=self.guardian_phone,
        )


@dataclass
class PatientUpdateDTO:
    """Datos modificables para un paciente existente."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None


@dataclass
class PatientResponseDTO:
    """Datos que la capa de aplicación expone hacia el exterior."""
    id: int
    first_name: str
    last_name: str
    birth_date: date
    medical_record_number: str
    guardian_name: str
    guardian_phone: str
    age_in_years: int
    is_pediatric: bool
    created_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, patient: Patient) -> "PatientResponseDTO":
        return cls(
            id=patient.id,  # type: ignore
            first_name=patient.first_name,
            last_name=patient.last_name,
            birth_date=patient.birth_date,
            medical_record_number=patient.medical_record_number,
            guardian_name=patient.guardian_name,
            guardian_phone=patient.guardian_phone,
            age_in_years=patient.calculate_age_in_years(),
            is_pediatric=patient.is_pediatric(),
            created_at=patient.created_at,
        )


@dataclass
class PatientImportResultDTO:
    """Resultado del proceso de importación masiva desde Excel."""
    total_rows: int
    imported_count: int
    failed_count: int
    errors: List[str] = field(default_factory=list)
