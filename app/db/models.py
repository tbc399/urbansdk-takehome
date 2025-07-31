from datetime import datetime
from typing import List

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[float]
    road_name: Mapped[str] = mapped_column(String(50), nullable=True)
    geometry: Mapped[Geometry] = mapped_column(
        Geometry("MULTILINESTRING", from_text="ST_GeomFromGeoJSON")
    )

    speeds: Mapped[List["SpeedRecord"]] = relationship(back_populates="link")


class SpeedRecord(Base):
    __tablename__ = "speeds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"))
    date_time: Mapped[datetime]
    average_speed: Mapped[float]
    day_of_week: Mapped[int]
    period: Mapped[int]

    link: Mapped[Link] = relationship(back_populates="speeds")
