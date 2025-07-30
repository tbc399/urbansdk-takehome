from datetime import datetime
from typing import Annotated

from config import DbSession
from fastapi import APIRouter, Query
from models import DayOfWeek, Link, Period, SpeedRecord
from sqlalchemy import func, select

router = APIRouter()


@router.get("/")
async def get_list(
    day: Annotated[DayOfWeek, Query()], period: Annotated[str, Query()], session: DbSession
):
    period = Period.from_display(period)
    statement = (
        select(
            SpeedRecord.link_id,
            func.avg(SpeedRecord.average_speed).label("average_speed"),
            SpeedRecord.day_of_week,
            SpeedRecord.period,
        )
        .where(SpeedRecord.day_of_week == day.number)
        .where(SpeedRecord.period == period.number)
        .group_by(SpeedRecord.link_id, SpeedRecord.day_of_week, SpeedRecord.period)
    )
    return [speed._asdict() for speed in session.execute(statement)]


@router.get("/{link_id}")
async def get_detail():
    return
