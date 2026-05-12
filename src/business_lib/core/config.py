import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    # 1. Identify which environment we are in
    ENV: str = os.getenv("ENV", "dev")

    # 2. Define the settings that will be filled
    PROJECT_NAME: str = "NextGen_MLOps"
    DATABASE_URL: str = ""
    ADAPTER_TYPE: str = ""

    # Pydantic loads files in the order provided.
    # We dynamically select the file based on the ENV variable.
    model_config = SettingsConfigDict(
        env_file=[
            str(BASE_DIR / ".env"),  # Load general defaults
            str(BASE_DIR / f".env.{os.getenv('ENV', 'dev')}")  # Load env-specific overrides
        ],
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()
