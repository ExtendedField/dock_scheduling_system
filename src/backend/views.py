from typing import Annotated

from fastapi import Depends, FastAPI, Response

from backend import service
from backend.dao import DocksDao, ReservationDao
from backend.dependencies import get_docks_dao, get_reservation_dao
from schema import Reservation

app = FastAPI()

# features:
# dont allow double bookings
# verify a boat will fit

app.post("create_reservation/{reservation}")


def create_reservation(
    reservation: Reservation,
    reservation_dao: Annotated[ReservationDao, Depends(get_reservation_dao)],
    docks_dao: Annotated[DocksDao, Depends(get_docks_dao)],
):
    try:
        service.add_reservation_to_database(reservation, reservation_dao, docks_dao)
    except ValueError as e:
        return Response(content=e, status_code=400)
    return Response(
        content=f"Successfully added reservation {reservation}", status_code=200
    )
