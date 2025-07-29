from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from geoalchemy2 import Geometry
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[float]
    road_name: Mapped[str] = mapped_column(String(50))
    usdk_speed_category: Mapped[int]
    funclass_id: Mapped[int]
    speed_cat: Mapped[int]
    volume_value: Mapped[int]
    volume_bin_id: Mapped[int]
    volume_year: Mapped[int]
    volumes_bin_description: Mapped[str] = mapped_column(String(50))
    geo_json: Mapped[Geometry] = mapped_column(Geometry('MULTILINESTRING'))

    speeds: Mapped[List["SpeedRecord"]] = relationship(back_populates="link")


class Period(Base):
    __tablename__ = "periods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    start: Mapped[datetime]
    end: Mapped[datetime]


class SpeedRecord(Base):
    __tablename__ = "speeds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"))
    date_time: Mapped[datetime]
    freeflow: Mapped[float]
    count: Mapped[int]
    std_dev: Mapped[float]
    min_: Mapped[float] = mapped_column(name="min")
    max_: Mapped[float] = mapped_column(name="max")
    confidence: Mapped[float]
    average_speed: Mapped[float]
    average_pct_85: Mapped[float]
    average_pct_95: Mapped[float]
    day_of_week: Mapped[int]
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id"))
    
    period: Mapped[Period] = relationship()
    link: Mapped[Link] = relationship(back_populates="speeds")
