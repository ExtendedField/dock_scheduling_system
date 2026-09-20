from backend.dao import DocksDao, ReservationDao
from schema import Reservation
from src.backend.helper import is_already_booked


def add_reservation_to_database(
    reservation: Reservation, reservation_dao: ReservationDao, docks_dao: DocksDao
):
    if not _vessel_fits(reservation, docks_dao):
        raise ValueError(
            f"Vessel of size {reservation.vessel_size} does not fit in requested dock."
        )

    if _dock_booked(reservation, reservation_dao):
        raise ValueError(
            f"Requested Dock is booked during date range {reservation.date_range}"
        )

    reservation_dao.add_reservation(reservation)


def _vessel_fits(reservation: Reservation, docks_dao: DocksDao) -> bool:
    dock_size = docks_dao.get_dock_size(reservation.dock_id)
    # TODO: coerce to unified metric for apples to apples comparison
    return dock_size.size > reservation.vessel_size.size


def _dock_booked(reservation: Reservation, reservations_dao: ReservationDao) -> bool:
    dates_booked = reservations_dao.get_dates_booked(reservation.dock_id)
    return is_already_booked(dates_booked, reservation.date_range)
