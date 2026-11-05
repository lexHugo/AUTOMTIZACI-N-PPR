from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from app.domain.entities.patient import Patient
from app.infrastructure.database.session import Base


class PatientModel(Base):
    """
    Modelo ORM de SQLAlchemy mapeado a la tabla de SQL Server 'pacientes'.
    Pertenece exclusivamente a la capa de Infraestructura.
    """
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    medical_record_number = Column(String(50), unique=True, index=True, nullable=False)
    guardian_name = Column(String(150), nullable=False)
    guardian_phone = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_domain(self) -> Patient:
        """Convierte el modelo ORM de persistencia en una entidad pura del dominio."""
        return Patient(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            medical_record_number=self.medical_record_number,
            guardian_name=self.guardian_name,
            guardian_phone=self.guardian_phone,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, patient: Patient) -> "PatientModel":
        """Convierte una entidad pura del dominio en un modelo ORM para persistencia."""
        return cls(
            id=patient.id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            birth_date=patient.birth_date,
            medical_record_number=patient.medical_record_number,
            guardian_name=patient.guardian_name,
            guardian_phone=patient.guardian_phone,
            created_at=patient.created_at or datetime.utcnow(),
        )
