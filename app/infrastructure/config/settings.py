import urllib.parse
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base de Datos SQL Server
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
    DB_SERVER: str = "localhost"
    DB_PORT: int = 1433
    DB_NAME: str = "PediatriaDB"
    DB_USER: str = "sa"
    DB_PASSWORD: str = "TuPasswordSeguro123!"
    DB_TRUST_SERVER_CERTIFICATE: str = "yes"

    # API FastAPI
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """
        Genera la URL de conexión SQLAlchemy con mssql+pyodbc usando connection string ODBC.
        Este formato es el más confiable y compatible para SQL Server en Windows y Linux.
        """
        odbc_str = (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_SERVER},{self.DB_PORT};"
            f"DATABASE={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASSWORD};"
            f"TrustServerCertificate={self.DB_TRUST_SERVER_CERTIFICATE};"
        )
        encoded_odbc = urllib.parse.quote_plus(odbc_str)
        return f"mssql+pyodbc:///?odbc_connect={encoded_odbc}"


settings = Settings()
