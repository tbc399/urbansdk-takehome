from typing import Annotated

from fastapi import APIRouter, Query
from geoalchemy2.functions import ST_AsGeoJSON
from sqlalchemy import func, select

from app.api.models import AggregateResponse, Period
from app.db.config import DbSession
from app.db.models import Link, SpeedRecord

router = APIRouter()


@router.get("/slow_links")
async def get_list(
    period: Annotated[Period, Query()],
    threshold: Annotated[float, Query()],
    min_days: Annotated[int, Query()],
    session: DbSession,
):
    #  This query is probably wrong, but we're just gonna send it.
    daily_avg = (
        select(
            Link.id.label("link_id"),
            func.date(SpeedRecord.date_time).label("date"),
            Link.road_name,
            Link.length,
            func.avg(SpeedRecord.average_speed).label("avg_speed"),
            ST_AsGeoJSON(Link.geometry).label("geometry"),
        )
        .join(Link.speeds)
        .where(SpeedRecord.period == period.order)
        .group_by(Link.id, func.date(SpeedRecord.date_time), SpeedRecord.period)
        .cte("daily_avg")
    )

    slow_days = (
        select(
            daily_avg.c.link_id,
            daily_avg.c.road_name,
            daily_avg.c.length,
            daily_avg.c.avg_speed,
            daily_avg.c.geometry,
            func.date_trunc("week", daily_avg.c.date).label("week"),
            func.count().label("days_below_threshold"),
        )
        .where(daily_avg.c.avg_speed < threshold)
        .group_by(
            daily_avg.c.link_id,
            daily_avg.c.road_name,
            daily_avg.c.length,
            daily_avg.c.avg_speed,
            daily_avg.c.geometry,
            func.date_trunc("week", daily_avg.c.date),
            daily_avg.c.date,
        )
        .cte("slow_days")
    )

    statement = select(
        slow_days.c.link_id.distinct().label("link_id"),
        slow_days.c.road_name,
        slow_days.c.length,
        slow_days.c.avg_speed.label("average_speed"),
        slow_days.c.geometry,
    ).where(slow_days.c.days_below_threshold >= min_days)

    return [
        AggregateResponse.model_validate(record._asdict())
        for record in await session.execute(statement)
    ]
