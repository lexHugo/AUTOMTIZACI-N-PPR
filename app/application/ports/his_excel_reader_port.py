from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.variables_ppr import VariablesPPR


class HISExcelReaderPort(ABC):
    """
    Puerto de salida para la lectura y filtrado del archivo Excel en formato HIS.
    Desacopla la lógica de aplicación de la biblioteca Pandas/OpenPyXL.
    """

    @abstractmethod
    def read_his_excel(self, file_content: bytes) -> List[VariablesPPR]:
        """
        Lee el archivo binario del Excel HIS, filtra únicamente las columnas requeridas
        y las convierte en una lista de entidades VariablesPPR.
        """
        raise NotImplementedError
