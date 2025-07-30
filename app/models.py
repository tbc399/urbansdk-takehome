from datetime import datetime
from enum import Enum, IntEnum
from typing import List

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    # length: Mapped[float]
    # road_name: Mapped[str] = mapped_column(String(50))
    # usdk_speed_category: Mapped[int]
    # funclass_id: Mapped[int]
    # speed_cat: Mapped[int]
    # volume_value: Mapped[int]
    # volume_bin_id: Mapped[int]
    # volume_year: Mapped[int]
    # volumes_bin_description: Mapped[str] = mapped_column(String(50))
    geo_json: Mapped[Geometry] = mapped_column(
        Geometry("MULTILINESTRING", from_text="ST_GeomFromGeoJSON")
    )

    speeds: Mapped[List["SpeedRecord"]] = relationship(back_populates="link")


class Period(Enum):
    OVERNIGHT = (1, "Overnight")
    MORNING = (2, "Early Morning")
    AM_PEAK = (3, "AM Peak")
    MIDDAY = (4, "Midday")
    AFTERNOON = (5, "Afternoon")
    PM_PEAK = (6, "PM Peak")
    EVENING = (7, "Evening")

    def __init__(self, id_value, display):
        self.number = id_value
        self.display = display

    @classmethod
    def from_display(cls, display):
        for x in cls:
            if display.lower() == x.display.lower():
                return x
        raise ValueError(f"No Period with display name {display} exists")

    @classmethod
    def from_number(cls, number):
        for x in cls:
            if number == x.number:
                return x
        raise ValueError(f"No Period with number {number} exists")

    def __str__(self):
        return self.display


class DayOfWeek(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Sunday"

    @property
    def number(self):
        for i, x in enumerate(DayOfWeek, 1):
            if x == self:
                return i


class SpeedRecord(Base):
    __tablename__ = "speeds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"))
    date_time: Mapped[datetime]
    # freeflow: Mapped[float]
    # count: Mapped[int]
    # std_dev: Mapped[float]
    # min_: Mapped[float] = mapped_column(name="min")
    # max_: Mapped[float] = mapped_column(name="max")
    # confidence: Mapped[float]
    average_speed: Mapped[float]
    # average_pct_85: Mapped[float]
    # average_pct_95: Mapped[float]
    day_of_week: Mapped[int]
    period: Mapped[int]

    link: Mapped[Link] = relationship(back_populates="speeds")
