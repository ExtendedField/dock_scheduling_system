import uuid
from datetime import date
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class BerthReservationHistory(SQLModel, Table=True):
    dock_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    date: date = Field(primary_key=True)
    reserved_by: str | None = None


class SizeMetric(Enum, str):
    FEET = "ft"
    INCHES = "in"
    METERS = "m"


class Size(BaseModel):
    size: int
    metric: SizeMetric = SizeMetric.FEET


class DockInfo(SQLModel, Table=True):
    dock_id: uuid.UUID = Field(primary_key=True)
    dock_name: str
    size: Size


class DateRange(BaseModel):
    start_date: date
    end_date: date


class Reservation(BaseModel):
    dock_id: str
    reserved_by: str
    vessel_size: Size
    date_range: DateRange
