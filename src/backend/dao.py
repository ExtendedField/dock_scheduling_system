from datetime import date, timedelta

from sqlmodel import Session, select

from schema import DockInfo, DockReservationHistory, Reservation


class SQLLiteDao:
    def __init__(self, session: Session):
        self.session = session


class ReservationDao(SQLLiteDao):
    def get_dates_booked(self, dock_id: str) -> list[date]:
        query = select(DockReservationHistory).where(
            DockReservationHistory.dock_id == dock_id
        )
        results = self.session.exec(query).all()
        return sorted([row.date for row in results])

    def add_reservation(self, reservation: Reservation):
        start_date = reservation.date_range.start_date
        end_date = reservation.date_range.end_date
        dates_to_add = [
            start_date + timedelta(days=x) for x in range((end_date - start_date).days)
        ]
        # add DockReservationHistory for each date in daterange
        for day in dates_to_add:
            self.session.add(
                DockReservationHistory(
                    dock_id=reservation.dock_id,
                    date=day,
                    reserved_by=reservation.reserved_by,
                )
            )
        self.session.commit()

    def get_all_reservations(self) -> list[DockReservationHistory]:
        query = select(DockReservationHistory)
        result = self.session.exec(query)
        return list(result)


class DocksDao(SQLLiteDao):
    def get_all_docks(self) -> list[DockInfo]:
        query = select(DockInfo)
        return list(self.session.exec(query))

    def get_dock_size(self, dock_id: str) -> int:
        query = select(DockInfo).where(DockInfo.dock_id == dock_id)
        results = self.session.exec(query).first()
        if results:
            return results.dock_size
        raise FileNotFoundError(f"No dock found with passed id: {dock_id}")
