# This is a script to load the legacy scheduling data into the sqllite database
from sqlmodel import create_engine

from database.parse_legacy import parse_legacy_data
from settings import settings

LEGACY_DATA_PATH = settings.path_to_legacy_docking_data
SQLLITE_ENGINE = create_engine(settings.sqllite_db_directory)


def main():
    dock_info_table, reservation_history_table = parse_legacy_data(
        path=LEGACY_DATA_PATH
    )
    dock_info_table.to_sql(
        name="dock_info", con=SQLLITE_ENGINE, if_exists="replace", index=False
    )
    reservation_history_table.to_sql(
        name="reservation_history", con=SQLLITE_ENGINE, if_exists="replace", index=False
    )


if __name__ == "__main__":
    main()
