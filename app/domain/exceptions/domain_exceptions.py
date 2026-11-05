class DomainException(Exception):
    """Excepción base para las reglas de negocio del dominio."""
    pass


class PatientNotFoundException(DomainException):
    """Lanzada cuando un paciente no se encuentra en el sistema."""
    def __init__(self, identifier: str | int):
        super().__init__(f"Paciente con identificador '{identifier}' no fue encontrado.")


class PatientAlreadyExistsException(DomainException):
    """Lanzada cuando ya existe un paciente con el mismo registro médico."""
    def __init__(self, medical_record_number: str):
        super().__init__(f"Ya existe un paciente con el número de historia clínica '{medical_record_number}'.")


class InvalidPatientAgeException(DomainException):
    """Lanzada cuando el paciente no cumple con el rango de edad pediátrico."""
    def __init__(self, age: int):
        super().__init__(f"La edad proporcionada ({age} años) supera el límite de atención pediátrica permitida.")
