from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from backend import service
from backend.dependencies import get_session
from schema import DockInfo, Reservation

router = APIRouter()


@router.post("/create_reservation")
def create_reservation(
    reservation: Reservation,
    session: Annotated[Session, Depends(get_session)],
):
    try:
        service.add_reservation_to_database(reservation, session)
    except ValueError as e:
        return Response(content=str(e), status_code=400)
    return Response(
        content=f"Successfully added reservation {reservation}", status_code=200
    )


@router.get("/current_reservations")
def get_current_reservations(session: Annotated[Session, Depends(get_session)]):
    return service.get_all_existing_reservations(session=session)


@router.get("/docks", response_model=list[DockInfo])
def get_docks(session: Annotated[Session, Depends(get_session)]):
    return service.get_all_docks(session=session)
