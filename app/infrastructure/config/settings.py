import os
import urllib.parse
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        DB_TYPE: str = "sqlite"  # "sqlite" o "mssql"
        DATABASE_URL: Optional[str] = None
        SQLITE_DB_PATH: str = "./pediatria_ppr.db"

        DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
        DB_SERVER: str = "localhost"
        DB_PORT: int = 1433
        DB_NAME: str = "PediatriaDB"
        DB_USER: str = "sa"
        DB_PASSWORD: str = "TuPasswordSeguro123!"
        DB_TRUST_SERVER_CERTIFICATE: str = "yes"
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
            if self.DATABASE_URL:
                return self.DATABASE_URL
            if self.DB_TYPE.lower() == "sqlite":
                return f"sqlite:///{self.SQLITE_DB_PATH}"
            odbc_str = (
                f"DRIVER={{{self.DB_DRIVER}}};"
                f"SERVER={self.DB_SERVER},{self.DB_PORT};"
                f"DATABASE={self.DB_NAME};"
                f"UID={self.DB_USER};"
                f"PWD={self.DB_PASSWORD};"
                f"TrustServerCertificate={self.DB_TRUST_SERVER_CERTIFICATE};"
            )
            return f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"

    settings = Settings()

except ImportError:
    class Settings:  # type: ignore
        DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")
        DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)
        SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "./pediatria_ppr.db")

        DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
        DB_PORT: int = int(os.getenv("DB_PORT", "1433"))
        DB_NAME: str = os.getenv("DB_NAME", "PediatriaDB")
        DB_USER: str = os.getenv("DB_USER", "sa")
        DB_PASSWORD: str = os.getenv("DB_PASSWORD", "TuPasswordSeguro123!")
        DB_TRUST_SERVER_CERTIFICATE: str = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")
        API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
        API_PORT: int = int(os.getenv("API_PORT", "8000"))
        API_DEBUG: bool = os.getenv("API_DEBUG", "True").lower() in ("true", "1")

        @property
        def database_url(self) -> str:
            if self.DATABASE_URL:
                return self.DATABASE_URL
            if self.DB_TYPE.lower() == "sqlite":
                return f"sqlite:///{self.SQLITE_DB_PATH}"
            odbc_str = (
                f"DRIVER={{{self.DB_DRIVER}}};"
                f"SERVER={self.DB_SERVER},{self.DB_PORT};"
                f"DATABASE={self.DB_NAME};"
                f"UID={self.DB_USER};"
                f"PWD={self.DB_PASSWORD};"
                f"TrustServerCertificate={self.DB_TRUST_SERVER_CERTIFICATE};"
            )
            return f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"

    settings = Settings()
