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
    # usdk_speed_category: Mapped[int]
    # funclass_id: Mapped[int]
    # speed_cat: Mapped[int]
    # volume_value: Mapped[int]
    # volume_bin_id: Mapped[int]
    # volume_year: Mapped[int]
    # volumes_bin_description: Mapped[str] = mapped_column(String(50))
    geometry: Mapped[Geometry] = mapped_column(  # TODO: change this "geometry"
        Geometry("MULTILINESTRING", from_text="ST_GeomFromGeoJSON")
    )

    speeds: Mapped[List["SpeedRecord"]] = relationship(back_populates="link")


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
