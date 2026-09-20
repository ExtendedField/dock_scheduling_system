from datetime import date

from sqlmodel import create_engine

from schema import Size, Reservation
from settings import settings

ENGINE = create_engine(sqllite_db_directory)


class SQLLiteDao:
    pass


class ReservationDao(SQLLiteDao):
    def get_dates_booked(self, dock_id: str) -> list[date]:
        return dates
    
    def add_reservation(self, reservation: Reservation):



class DocksDao(SQLLiteDao):
    def get_dock_size(self, dock_id: str) -> Size:
        return Size()
