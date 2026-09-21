# This is a script to load the legacy scheduling data into the sqllite database
import typing

import pandas as pd
from sqlmodel import Session, SQLModel, create_engine

from database.parse_legacy import parse_legacy_data
from schema import DockInfo, DockReservationHistory
from settings import settings

LEGACY_DATA_PATH = settings.path_to_legacy_docking_data
SQLLITE_ENGINE = create_engine(settings.sqllite_db_directory)


def main():
    dock_info_table, reservation_history_table = parse_legacy_data(
        path=LEGACY_DATA_PATH
    )
    dock_info_rows = [
        DockInfo(
            dock_id=str(row.dock_id),
            dock_name=str(row.dock_name),
            dock_size=int(typing.cast(str, row.dock_size)),
            dock_size_metric=str(row.dock_size_metric),
        )
        for row in dock_info_table.itertuples(index=False)
    ]
    reservation_history_rows = [
        DockReservationHistory(
            dock_id=str(row.dock_id),
            date=pd.Timestamp(typing.cast(str, row.date)).date(),
            reserved_by=None if pd.isna(row.reserved_by) else str(row.reserved_by),
        )
        for row in reservation_history_table.itertuples(index=False)
    ]

    SQLModel.metadata.drop_all(SQLLITE_ENGINE)
    SQLModel.metadata.create_all(SQLLITE_ENGINE)
    with Session(SQLLITE_ENGINE) as session:
        session.add_all(dock_info_rows)
        session.add_all(reservation_history_rows)
        session.commit()


if __name__ == "__main__":
    main()
