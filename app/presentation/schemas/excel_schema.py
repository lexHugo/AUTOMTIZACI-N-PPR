from typing import List
from pydantic import BaseModel, Field


class ImportResultResponse(BaseModel):
    """Respuesta HTTP para el proceso de importación masiva de Excel."""
    total_rows: int = Field(..., description="Total de filas leídas en el archivo Excel")
    imported_count: int = Field(..., description="Cantidad de pacientes registrados exitosamente")
    failed_count: int = Field(..., description="Cantidad de registros que no pudieron ser importados")
    errors: List[str] = Field(default_factory=list, description="Detalle de errores por fila")
