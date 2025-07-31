from typing import Annotated

from fastapi import APIRouter, Query
from geoalchemy2.functions import ST_AsGeoJSON
from sqlalchemy import select

from app.api.models import Period
from app.db.config import DbSession
from app.db.models import Link, SpeedRecord

router = APIRouter()


@router.get("/slow_links")
async def get_list(
    period: Annotated[str, Query()],
    threshold: Annotated[float, Query()],
    min_days: Annotated[int, Query()],
    session: DbSession,
):
    # TODO: need to complete. Do I need a window function or simple count?
    period = Period.from_display(period)
    statement = (
        select(
            Link.id,
            SpeedRecord.average_speed,
            SpeedRecord.period,
            ST_AsGeoJSON(Link.geo_json).label("geo_json"),
        )
        .join(Link.speeds)
        .where(SpeedRecord.period == period.number)
        .where(SpeedRecord.average_speed < threshold)
        .group_by(Link.id, SpeedRecord.period)
    )

    return [speed._asdict() for speed in await session.execute(statement)]
