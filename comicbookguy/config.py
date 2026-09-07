from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    comicbooks_library: Path
    comicbooks_inbox: Path

    model_config = SettingsConfigDict(
        env_file="paths.env",
        env_file_encoding="utf-8",
    )


settings = Settings()
