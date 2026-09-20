import uuid
from datetime import date
from enum import Enum

from sqlmodel import Field, SQLModel


class BerthReservationHistory(SQLModel, Table=True):
    dock_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    date: date = Field(primary_key=True)
    reserved_by: str | None = None


class SizeMetric(Enum, str):
    FEET = "ft"
    INCHES = "in"
    METERS = "m"


class DockInfo(SQLModel, Table=True):
    dock_id: uuid.UUID = Field(primary_key=True)
    dock_name: str
    size: int
    size_metric: SizeMetric
