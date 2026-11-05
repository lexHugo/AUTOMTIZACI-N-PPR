from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepositoryInterface
from app.infrastructure.models.patient_model import PatientModel


class SqlAlchemyPatientRepository(PatientRepositoryInterface):
    """
    Implementación concreta de persistencia para SQL Server utilizando SQLAlchemy.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, patient: Patient) -> Patient:
        model = PatientModel.from_domain(patient)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_domain()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        model = (
            self.db.query(PatientModel)
            .filter(PatientModel.id == patient_id)
            .first()
        )
        return model.to_domain() if model else None

    def get_by_medical_record_number(self, medical_record_number: str) -> Optional[Patient]:
        model = (
            self.db.query(PatientModel)
            .filter(PatientModel.medical_record_number == medical_record_number)
            .first()
        )
        return model.to_domain() if model else None

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        models = (
            self.db.query(PatientModel)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [m.to_domain() for m in models]

    def update(self, patient: Patient) -> Patient:
        model = (
            self.db.query(PatientModel)
            .filter(PatientModel.id == patient.id)
            .first()
        )
        if not model:
            raise ValueError(f"No existe el modelo para el paciente con ID {patient.id}")

        model.first_name = patient.first_name
        model.last_name = patient.last_name
        model.birth_date = patient.birth_date
        model.guardian_name = patient.guardian_name
        model.guardian_phone = patient.guardian_phone

        self.db.commit()
        self.db.refresh(model)
        return model.to_domain()

    def delete(self, patient_id: int) -> bool:
        model = (
            self.db.query(PatientModel)
            .filter(PatientModel.id == patient_id)
            .first()
        )
        if not model:
            return False

        self.db.delete(model)
        self.db.commit()
        return True
