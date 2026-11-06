class DomainException(Exception):
    """Excepción base para las reglas de negocio del dominio."""
    pass


class InvalidPPRException(DomainException):
    """Excepción para errores de validación de datos en PPR."""
    pass
