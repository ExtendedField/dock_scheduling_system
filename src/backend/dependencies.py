from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from backend.dao import DocksDao, ReservationDao
from settings import settings

connect_args = {"check_same_thread": False}
ENGINE = create_engine(settings.sqllite_db_directory, connect_args=connect_args)


def get_session() -> Generator[Session]:
    with Session(ENGINE) as session:
        yield session


def get_docks_dao(session: Annotated[Session, Depends(get_session)]) -> DocksDao:
    return DocksDao(session)


def get_reservation_dao(
    session: Annotated[Session, Depends(get_session)],
) -> ReservationDao:
    return ReservationDao(session)
