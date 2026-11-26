from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.domain.entities.variables_ppr import VariablesPPR


class DataMartRepositoryInterface(ABC):
    """
    Puerto de persistencia para el Data Mart de HIS MINSA.
    Gestiona el almacenamiento granular de atenciones (citas e items) y su acumulación mensual.
    """

    @abstractmethod
    def guardar_trama(
        self,
        nombre_archivo: str,
        tipo_formato: str,
        variables: List[VariablesPPR],
        usuario: str = "estadistica"
    ) -> Dict[str, Any]:
        """
        Inserta la trama de variables en el Data Mart.
        Realiza desduplicación de citas e items diagnósticos para permitir cargas incrementales.
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_variables_acumuladas(
        self,
        meses: Optional[List[str]] = None,
        anio: Optional[int] = None
    ) -> List[VariablesPPR]:
        """
        Recupera las variables clínicas acumuladas para los meses o año especificados.
        Si no se especifican filtros, recupera la totalidad de la historia almacenada.
        """
        raise NotImplementedError

    @abstractmethod
    def listar_meses_disponibles(self) -> List[str]:
        """
        Retorna la lista ordenada cronológicamente de meses disponibles en el Data Mart (ej: ['2026-01', '2026-02']).
        """
        raise NotImplementedError

    @abstractmethod
    def listar_archivos_cargados(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retorna el historial de archivos cargados para fines de trazabilidad y auditoría.
        """
        raise NotImplementedError

    @abstractmethod
    def guardar_personal_maestro(
        self,
        personal_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Inserta o actualiza el catálogo maestro de personal de salud (Médicos, Enfermeras, etc.).
        """
        raise NotImplementedError

    @abstractmethod
    def listar_personal(
        self,
        cod_profesion: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna el listado del personal de salud registrado, opcionalmente filtrado por código de profesión.
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_resumen_atenciones_ups(
        self,
        target_ups: List[str],
        cod_profesion: Optional[str] = None,
        anio: Optional[int] = None,
        excluir_cod_profesion: Optional[str] = "29",
    ) -> Dict[str, Any]:
        """
        Calcula de forma agregada y directa en la base de datos el conteo de citas únicas
        por UPS y mes, optimizada para alto rendimiento y cero sobrecarga de memoria.
        """
        raise NotImplementedError

    @abstractmethod
    def reiniciar_datamart(self) -> bool:
        """
        Limpia los datos del Data Mart (citas, items, personal y archivos cargados).
        """
        raise NotImplementedError
