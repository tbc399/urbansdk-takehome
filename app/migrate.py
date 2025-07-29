from models import Link, SpeedRecord
import sys


def init_db():
    pass

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Too many arguments")
        print("Usage: python app/init_db.py")
        exit(-1)
    else:
        links_path = sys.argv[1]
        speeds_path = sys.argv[2]

    code = init_db()
    exit(code)
