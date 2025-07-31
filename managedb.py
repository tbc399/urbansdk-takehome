import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path

from sqlalchemy import URL, Engine, create_engine, insert
from sqlalchemy.orm import Session

_data_cache = "data"
_links_path = Path(_data_cache) / "links.parq"
_speeds_path = Path(_data_cache) / "speeds.parq"


def _make_engine() -> Engine:
    from app.config import settings

    url = URL.create(
        "postgresql+psycopg",
        username=settings().db_username,
        password=settings().db_pass,
        host=settings().db_host,
        database=settings().db_name,
    )
    return create_engine(url)


def create_tables():
    from app.db.models import Base

    print(f"Creating tables: {', '.join(Base.metadata.tables.keys())}")
    try:
        Base.metadata.create_all(_make_engine())
    except Exception as e:
        print(f"Failed to craete database tables: {e}")
        sys.exit(-1)

    print("Tables created successfully")


def drop_tables():
    from app.db.models import Base

    print(f"Dropping tables: {', '.join(Base.metadata.tables.keys())}")
    try:
        Base.metadata.drop_all(_make_engine())
    except Exception as e:
        print(f"Failed to drop database tables: {e}")
        sys.exit(-1)

    print("Tables dropped successfully")


def _fetch_data():
    import os
    import pathlib

    import requests

    #  hardcode for simplicity
    base = "https://cdn.urbansdk.com/data-engineering-interview"
    links_url = f"{base}/link_info.parquet.gz"
    speeds_url = f"{base}/duval_jan1_2024.parquet.gz"

    print("Fetching links file from cdn")
    links_response = requests.get(links_url)
    if links_response.status_code != 200:
        print(f"Failed to get file: status={links_response.status_code} - > {links_response.text}")
        sys.exit(-1)

    print("Fetching speeds file from cdn")
    speeds_response = requests.get(speeds_url)
    if speeds_response.status_code != 200:
        print(
            f"Failed to get file: status={speeds_response.status_code} - > {speeds_response.text}"
        )
        sys.exit(-1)

    os.makedirs(_data_cache, exist_ok=True)

    with open(_links_path, "wb") as f:
        f.write(links_response.content)

    with open(_speeds_path, "wb") as f:
        f.write(speeds_response.content)


def load_data():
    #  TODO: change this so that it downloads data from the cdn and caches it
    import os

    import pandas as pd

    from app.db.models import Link, SpeedRecord

    if not (os.path.exists(_links_path) and os.path.exists(_speeds_path)):
        _fetch_data()

    with Session(_make_engine()) as session:
        try:
            links_df = pd.read_parquet(_links_path, engine="fastparquet")
        except Exception as e:
            print(f"Failed to read the links file: {e}")
            sys.exit(-1)

        try:
            speeds_df = pd.read_parquet(_speeds_path, engine="fastparquet")
        except Exception as e:
            print(f"Failed to read the speeds file: {e}")
            sys.exit(-1)

        print("Loading links...")
        links = links_df.apply(
            lambda x: dict(
                id=x.link_id, length=x._length, road_name=x.road_name, geometry=x.geo_json
            ),
            axis=1,
        )
        session.execute(insert(Link), list(links.values))
        session.commit()

        print("Loading speeds...")
        speeds = speeds_df.apply(
            lambda x: dict(
                link_id=x.link_id,
                date_time=x.date_time,
                average_speed=x.average_speed,
                day_of_week=x.day_of_week,
                period=x.period,
            ),
            axis=1,
        )
        session.execute(insert(SpeedRecord), list(speeds.values))
        session.commit()

    print("Data loaded successfully!")


if __name__ == "__main__":

    parser = ArgumentParser(
        description="Database management CLI tool",
        formatter_class=RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands", metavar="COMMAND")

    # Create command
    create_parser = subparsers.add_parser("create-tables", help="Create all database tables")
    create_parser.set_defaults(func=create_tables)

    # Drop command
    drop_parser = subparsers.add_parser("drop-tables", help="Drop all database tables")
    drop_parser.set_defaults(func=drop_tables)

    # Ingest command
    load_parser = subparsers.add_parser("load-data", help="Load data into the database")
    load_parser.set_defaults(func=load_data)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "func"):
        args.func()
    else:
        parser.print_help()
        sys.exit(1)
