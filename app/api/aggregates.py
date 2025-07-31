from typing import Annotated

import shapely
from fastapi import APIRouter, Path, Query
from geoalchemy2 import functions
from sqlalchemy import Numeric, func, select

from app.api.models import (
    AggregateResponse,
    DayOfWeek,
    LinkResponse,
    Period,
    SpatialFilterRequest,
)
from app.db.config import DbSession
from app.db.models import Link, SpeedRecord

router = APIRouter()


@router.get("/")
async def get_list(
    day: Annotated[DayOfWeek, Query()], period: Annotated[Period, Query()], session: DbSession
):
    statement = (
        select(
            Link.id.label("link_id"),
            Link.road_name,
            Link.length,
            func.round(func.avg(SpeedRecord.average_speed).cast(Numeric), 2).label("average_speed"),
            functions.ST_AsGeoJSON(Link.geometry).label("geometry"),
        )
        .join(Link.speeds)
        .where(SpeedRecord.day_of_week == day.order)
        .where(SpeedRecord.period == period.order)
        .group_by(Link.id, SpeedRecord.day_of_week, SpeedRecord.period)
    )
    return [
        AggregateResponse.model_validate(record._asdict())
        for record in await session.execute(statement)
    ]


@router.get("/{link_id}")
async def get_detail(
    link_id: Annotated[int, Path()],
    day: Annotated[DayOfWeek, Query()],
    period: Annotated[Period, Query()],
    session: DbSession,
):
    statement = (
        select(
            Link.id.label("link_id"),
            Link.road_name,
            Link.length,
            func.round(func.avg(SpeedRecord.average_speed).cast(Numeric), 2).label("average_speed"),
            functions.ST_AsGeoJSON(Link.geometry).label("geometry"),
        )
        .join(Link.speeds)
        .where(SpeedRecord.link_id == link_id)
        .where(SpeedRecord.day_of_week == day.order)
        .where(SpeedRecord.period == period.order)
        .group_by(Link.id, SpeedRecord.day_of_week, SpeedRecord.period)
    )
    records = [
        AggregateResponse.model_validate(record._asdict())
        for record in await session.execute(statement)
    ]
    return records[0]


@router.post("/spatial_filter")
async def spatial_filter(filter: SpatialFilterRequest, session: DbSession):
    polygon = shapely.box(*filter.bbox)
    statement = (
        select(Link.id.label("link_id"), Link.road_name, Link.length)
        .join(Link.speeds)
        .where(SpeedRecord.day_of_week == filter.day.order)
        .where(SpeedRecord.period == filter.period.order)
        .where(Link.geometry.intersects(functions.ST_GeomFromText(polygon.wkt, 4326)))
    )

    return [
        LinkResponse.model_validate(record._asdict()) for record in await session.execute(statement)
    ]
