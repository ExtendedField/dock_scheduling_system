from datetime import date, timedelta

from sqlmodel import create_engine, Session, select, add

from schema import Size, Reservation, DockInfo, DockReservationHistory
from settings import settings


class SQLLiteDao:
    def __init__(self, session: Session):
        self.session = session


class ReservationDao(SQLLiteDao):
    def get_dates_booked(self, dock_id: str) -> list[date]:
        with self.session as session:
            query = select(DockReservationHistory).where(dock_id == dock_id)
            results = session.exec(query).all()
        return sorted([row.date for row in results])

    def add_reservation(self, reservation: Reservation):
        start_date = reservation.date_range.start_date
        end_date = reservation.date_range.end_date
        dates_to_add = [
            start_date + timedelta(days=x) for x in range((end_date - start_date).days)
        ]
        with self.session as session:
            # add DockReservationHistory for each date in daterange
            for day in dates_to_add:
                session.add(
                    DockReservationHistory(
                        dock_id=reservation.dock_id,
                        date=day,
                        reserved_by=reservation.reserved_by,
                    )
                )
            session.commit()


class DocksDao(SQLLiteDao):
    def get_dock_size(self, dock_id: str) -> Size:
        with self.session as session:
            query = select(DockInfo).where(DockInfo.dock_id == dock_id)
            results = session.exec(query).first()
        if results:
            return results.size
        raise FileNotFoundError(f"No dock found with passed id: {dock_id}")
