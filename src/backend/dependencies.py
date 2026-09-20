from backend.dao import DocksDao, ReservationDao


def get_docks_dao() -> DocksDao:
    return DocksDao()


def get_reservation_dao() -> ReservationDao:
    return ReservationDao()
