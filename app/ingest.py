import sys

import pandas as pd


def ingest(links_file, speeds_file):
    try:
        links_df = pd.read_parquet(links_path, engine="fastparquet")
    except FileNotFoundError:
        print("Could not find the given links file")
        return -1
    except Exception:
        print("Found links file, but failed to read")
        return -1

    try:
        speeds_df = pd.read_parquet(speeds_file, engine="fastparquet")
    except FileNotFoundError:
        print("Could not find the given speeds file")
        return -1
    except Exception:
        print("Found speeds file, but failed to read")
        return -1

    print(links_df.head())
    links_df.
    #print(speeds_df.head())


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Too many arguments")
        print("Usage: python app/ingest.py [LINKS_FILE] [SPEEDS_FILE]")
        exit(-1)
    elif len(sys.argv) < 3:
        print("Too few arguments")
        print("Usage: python app/ingest.py [LINKS_FILE] [SPEEDS_FILE]")
        exit(-1)
    else:
        links_path = sys.argv[1]
        speeds_path = sys.argv[2]

    code = ingest(links_path, speeds_path)
    exit(code)
