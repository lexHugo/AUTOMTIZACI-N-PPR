from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.variables_ppr import VariablesPPR


class HISExcelReaderPort(ABC):
    """
    Puerto de salida para la lectura y filtrado del archivo de tramas en formato HIS (Excel / CSV).
    Desacopla la lógica de aplicación de las bibliotecas de lectura de datos (Pandas, Calamine, etc.).
    """

    @abstractmethod
    def read_his_excel(self, file_content: bytes, filename: str = "") -> List[VariablesPPR]:
        """
        Lee el archivo binario del HIS (Excel .xlsx/.xls o texto .csv), filtra únicamente las columnas requeridas
        y las convierte en una lista de entidades VariablesPPR.
        """
        raise NotImplementedError
