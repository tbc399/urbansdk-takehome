from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Period(Enum):
    OVERNIGHT = "Overnight"
    MORNING = "Early Morning"
    AM_PEAK = "AM Peak"
    MIDDAY = "Midday"
    AFTERNOON = "Afternoon"
    PM_PEAK = "PM Peak"
    EVENING = "Evening"

    @classmethod
    def from_order(cls, order):
        for i, x in enumerate(cls, 1):
            if i == order:
                return x
        raise ValueError(f"No value corresponding to {order} exists in {cls.__name__}")

    @property
    def order(self):
        for i, x in enumerate(Period, 1):
            if x == self:
                return i


class DayOfWeek(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Sunday"

    @property
    def order(self):
        for i, x in enumerate(DayOfWeek, 1):
            if x == self:
                return i

    @classmethod
    def from_order(cls, order):
        for i, x in enumerate(cls, 1):
            if i == order:
                return x
        raise ValueError(f"No value corresponding to {order} exists in {cls.__name__}")


class SpatialFilterRequest(BaseModel):
    day: DayOfWeek
    period: Period
    bbox: List[float] = Field(min_length=4, max_length=4)


class AggregateResponse(BaseModel):
    link_id: int = Field(serialization_alias="id")
    road_name: Optional[str] = Field(default=None)
    length: float
    average_speed: float
    geometry: str


class LinkResponse(BaseModel):
    link_id: int
    road_name: Optional[str] = Field(default=None)
    length: float
