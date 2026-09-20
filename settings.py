from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_password: str
    path_to_legacy_docking_data: Path = Path("./src/database/legacy_dock_schedule.xlsx")


settings = Settings(_env_file=".env")
