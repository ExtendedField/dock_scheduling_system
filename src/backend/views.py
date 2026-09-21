from typing import Annotated

from fastapi import Depends, FastAPI, Response
from sqlmodel import Session

from backend import service
from backend.dependencies import get_session
from schema import Reservation

app = FastAPI()

# features:
# dont allow double bookings
# verify a boat will fit

app.post("create_reservation/{reservation}")


def create_reservation(
    reservation: Reservation,
    session: Annotated[Session, Depends(get_session)],
):
    try:
        service.add_reservation_to_database(reservation, session)
    except ValueError as e:
        return Response(content=e, status_code=400)
    return Response(
        content=f"Successfully added reservation {reservation}", status_code=200
    )
