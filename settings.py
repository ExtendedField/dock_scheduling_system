from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqllite_password: str
    sqllite_db_directory: str = "sqlite:///dock_scheduling.db"
    path_to_legacy_docking_data: Path = Path("./src/database/legacy_dock_schedule.xlsx")


settings = Settings(_env_file=".env")
