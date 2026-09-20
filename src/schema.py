from datetime import date

from sqlmodel import Field, SQLModel


class BerthReservationHistory(SQLModel):
    id: int = Field(primary_key=True)
    date: date = Field(primary_key=True)
    name: str
    size: int
    reserved_by: str | None = None
    reserved: bool = False
