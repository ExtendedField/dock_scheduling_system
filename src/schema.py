import uuid
from datetime import date

from sqlmodel import Field, SQLModel


class BerthReservationHistory(SQLModel):
    dock_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    dock_name: str
    date: date = Field(primary_key=True)
    name: str
    size: int
    reserved_by: str | None = None
    reserved: bool = False
