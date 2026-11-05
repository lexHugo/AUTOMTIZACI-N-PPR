from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class PatientCreateRequest(BaseModel):
    """Esquema de entrada para registrar un paciente."""
    first_name: str = Field(..., min_length=2, max_length=100, example="Mateo")
    last_name: str = Field(..., min_length=2, max_length=100, example="Gómez")
    birth_date: date = Field(..., example="2020-05-15")
    medical_record_number: str = Field(..., min_length=3, max_length=50, example="PED-2024-001")
    guardian_name: str = Field(..., min_length=3, max_length=150, example="Laura Gómez (Madre)")
    guardian_phone: str = Field(..., min_length=7, max_length=30, example="+57 300 1234567")


class PatientResponse(BaseModel):
    """Esquema de salida HTTP con los datos del paciente."""
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

    model_config = {
        "from_attributes": True
    }
