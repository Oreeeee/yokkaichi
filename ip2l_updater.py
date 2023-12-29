import sys
import time
from zipfile import ZipFile

import requests


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: {} IP2LOCATION_TOKEN".format(sys.argv[0]))
        sys.exit(1)

    # Download the dbs
    db_zips: tuple = (
        "data/ip2location_dbs/IP2LOCATION-LITE-DB11.BIN.zip",
        "data/ip2location_dbs/IP2LOCATION-LITE-DB1.CSV.zip",
    )

    with open(db_zips[0], "wb") as f:
        f.write(
            requests.get(
                f"https://www.ip2location.com/download/?token={sys.argv[1]}&file=DB11LITEBIN"
            ).content
        )

    with open(db_zips[1], "wb") as f:
        f.write(
            requests.get(
                f"https://www.ip2location.com/download/?token={sys.argv[1]}&file=DB1LITECSV"
            ).content
        )

    for db_zip in db_zips:
        with ZipFile(db_zip, "r") as f:
            f.extractall(path="data/ip2location_dbs/")

    with open("data/ip2location_dbs/LAST_UPDATED", "w") as f:
        # Write current time in Unix secs
        f.write(str(round(time.time())))


if __name__ == "__main__":
    sys.exit(main())
