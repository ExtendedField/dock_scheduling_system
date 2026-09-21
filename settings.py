from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent


class Settings(BaseSettings):
    sqllite_password: str
    sqllite_db_directory: str = f"sqlite:///{PROJECT_ROOT / 'dock_scheduling.db'}"
    path_to_legacy_docking_data: Path = (
        PROJECT_ROOT / "src/database/legacy_dock_schedule.xlsx"
    )


settings = Settings(_env_file=PROJECT_ROOT / ".env")
