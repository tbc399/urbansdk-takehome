import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from sqlalchemy import insert
from sqlalchemy.orm import Session


def create_tables(args):
    from config import get_engine
    from models import Base

    print(f"Creating tables: {', '.join(Base.metadata.tables.keys())}")
    try:
        Base.metadata.create_all(get_engine())
    except Exception as e:
        print(f"Failed to craete database tables: {e}")
        sys.exit(-1)

    print("Tables created successfully")


def drop_tables(args):
    from config import get_engine
    from models import Base

    print(f"Dropping tables: {', '.join(Base.metadata.tables.keys())}")
    try:
        Base.metadata.drop_all(get_engine())
    except Exception as e:
        print(f"Failed to drop database tables: {e}")
        sys.exit(-1)

    print("Tables dropped successfully")


def load_data(args):
    #  TODO: change this so that it downloads data from the cdn and caches it
    import os

    import pandas as pd
    from config import get_engine
    from models import Link, SpeedRecord

    # Session = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

    print("loading data...")

    if not os.path.exists(args.links_file):
        print(f"links file not found: {args.links_file}")
        sys.exit(-1)
    if not os.path.exists(args.speeds_file):
        print(f"speeds file not found: {args.speeds_file}")
        sys.exit(-1)

    with Session(get_engine()) as session:
        try:
            links_df = pd.read_parquet(args.links_file, engine="fastparquet")
        except Exception:
            print("Failed to read the links file")
            sys.exit(-1)

        try:
            speeds_df = pd.read_parquet(args.speeds_file, engine="fastparquet")
        except Exception:
            print("Failed to read the links file")
            sys.exit(-1)

        print("Loading links...")
        links = links_df.apply(lambda x: dict(id=x.link_id, geo_json=x.geo_json), axis=1)
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
    create_parser = subparsers.add_parser("create", help="Create all database tables")
    create_parser.set_defaults(func=create_tables)

    # Drop command
    drop_parser = subparsers.add_parser("drop", help="Drop all database tables")
    drop_parser.set_defaults(func=drop_tables)

    # Ingest command
    load_parser = subparsers.add_parser("load", help="Load data into the database")
    load_parser.add_argument("links_file", help="Path to the links parquet file")
    load_parser.add_argument("speeds_file", help="Path to the speeds parquet file")
    load_parser.set_defaults(func=load_data)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)
