from datetime import date as Date
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class DockReservationHistory(SQLModel, table=True):
    dock_id: str = Field(primary_key=True)
    date: Date = Field(primary_key=True)
    reserved_by: str | None = None


class SizeMetric(str, Enum):
    FEET = "ft"
    INCHES = "in"
    METERS = "m"


class DockInfo(SQLModel, table=True):
    dock_id: str = Field(primary_key=True)
    dock_name: str
    dock_size: int
    dock_size_metric: str = SizeMetric.FEET


class DateRange(BaseModel):
    start_date: Date
    end_date: Date


class Reservation(BaseModel):
    dock_id: str
    reserved_by: str
    vessel_size: int
    vessel_metric: SizeMetric = SizeMetric.FEET
    date_range: DateRange
