from sqlmodel import Session

from backend.dao import DocksDao, ReservationDao
from backend.helper import is_already_booked
from schema import DockInfo, DockReservationHistory, Reservation


def add_reservation_to_database(reservation: Reservation, session: Session):
    if not _vessel_fits(reservation, DocksDao(session)):
        raise ValueError(
            f"Vessel of size {reservation.vessel_size} does not fit in requested dock."
        )
    reservation_dao = ReservationDao(session)
    if _dock_booked(reservation, ReservationDao(session)):
        raise ValueError(
            f"Requested Dock is booked during date range {reservation.date_range}"
        )

    reservation_dao.add_reservation(reservation)


def _vessel_fits(reservation: Reservation, docks_dao: DocksDao) -> bool:
    dock_size = docks_dao.get_dock_size(reservation.dock_id)
    # TODO: coerce to unified metric for apples to apples comparison
    return dock_size > reservation.vessel_size


def _dock_booked(reservation: Reservation, reservations_dao: ReservationDao) -> bool:
    dates_booked = reservations_dao.get_dates_booked(reservation.dock_id)
    return is_already_booked(dates_booked, reservation.date_range)


def get_all_existing_reservations(session: Session) -> list[DockReservationHistory]:
    reservation_dao = ReservationDao(session)
    return reservation_dao.get_all_reservations()


def get_all_docks(session: Session) -> list[DockInfo]:
    return DocksDao(session).get_all_docks()
