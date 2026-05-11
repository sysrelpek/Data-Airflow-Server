from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

# Hitta projektets rotmapp (3 steg upp från denna fil)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    # Miljö-identitet
    ENV: str = "dev"  # Hämtas från .env, defaultar till 'dev'
    PROJECT_NAME: str = "NextGen_MLOps"

    # Databas/Infrastruktur
    DATABASE_URL: str = "sqlite:///./dev_storage.db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Sökvägar (Gör det enkelt att flytta mellan servrar)
    CONFIG_DIR: Path = BASE_DIR / "config"
    MANIFEST_DIR: Path = BASE_DIR / "dags" / "manifests"
    DATA_DIR: Path = BASE_DIR / "data"

    # Pydantic-magi: Läser automatiskt från .env filen om den finns
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding='utf-8',
        extra='ignore'  # Ignorera variabler i .env som vi inte definierat här
    )


# Instansiera settings som en singleton
settings = Settings()
