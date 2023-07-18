import datetime
import os
import pathlib
import time
import urllib
from zipfile import ZipFile

from IP2Location import IP2Location

from .constants import console
from .enums import IP2LocDBStatus, IP2LocManagerUserAnswers
from .structs import CFG


class IP2L_Manager:
    def __init__(self, cfg: CFG) -> None:
        self.cfg = cfg

        self.ip2l_dbs: str = self.cfg.ip2location_dbs

        # Try to open the last updated date file
        opening_status: IP2LocDBStatus = self.open_last_updated_file()
        if opening_status == IP2LocDBStatus.DOESNT_EXIST:
            self.get_user_answers(
                "IP2Location Database doesn't exist. [U]pdate? [M]anually Update? [E]xit?: "
            )

        if opening_status == IP2LocDBStatus.INCORRECT_DATE:
            self.get_user_answers(
                "Can't determine last update of the IP2Location database. [U]pdate? [S]kip? [E]xit?: "
            )

        if opening_status == IP2LocDBStatus.EXISTS:
            if not self.is_up_to_date():
                self.get_user_answers(
                    "Your IP2Location database is outdated. [U]pdate? [M]anually update? [S]kip? [E]xit?: "
                )

        # Load DB
        console.print("Loading IP2Location database", style="cyan")
        try:
            if self.cfg.ip2location_cache:
                self.db: IP2Location = IP2Location(
                    f"{self.ip2l_dbs}/{self.cfg.ip2location_db_bin}", "SHARED_MEMORY"
                )
            else:
                self.db: IP2Location = IP2Location(
                    f"{self.ip2l_dbs}/{self.cfg.ip2location_db_bin}"
                )
        except ValueError:
            console.print("IP2Location database is broken or corrupted!", style="red")
            exit(1)

    def get_location(self, ip: str) -> dict:
        return self.db.get_all(ip).__dict__

    def open_last_updated_file(self) -> IP2LocDBStatus:
        last_updated_file_loc: str = f"{self.ip2l_dbs}/LAST_UPDATED"
        try:
            with open(last_updated_file_loc, "r") as f:
                self.last_updated: int = int(f.readline())
            # Also verify are the actual database files there
            if not os.path.isfile(
                f"{self.ip2l_dbs}/{self.cfg.ip2location_db_bin}"
            ) or not os.path.isfile(f"{self.ip2l_dbs}/{self.cfg.ip2location_db_csv}"):
                return IP2LocDBStatus.DOESNT_EXIST
            return IP2LocDBStatus.EXISTS
        except FileNotFoundError:
            # When the directory wasn't created yet
            os.makedirs(self.ip2l_dbs)
            pathlib.Path(last_updated_file_loc).touch()
            return IP2LocDBStatus.DOESNT_EXIST
        except ValueError:
            # When the directory exists, but the file is in incorrent format or doesn't exist
            if not os.path.isfile(self.cfg.ip2location_db_bin) or not os.path.isfile(
                self.cfg.ip2location_db_csv
            ):
                return IP2LocDBStatus.DOESNT_EXIST
            pathlib.Path(last_updated_file_loc).touch(exist_ok=True)
            return IP2LocDBStatus.INCORRECT_DATE

    def create_last_updated_file(self) -> None:
        last_updated_file_loc: str = f"{self.ip2l_dbs}/LAST_UPDATED"
        with open(last_updated_file_loc, "w") as f:
            # Write current time in Unix secs
            f.write(str(round(time.time())))

    def is_up_to_date(self) -> bool:
        YEAR_INDEX: int = 0
        MONTH_INDEX: int = 1

        current_time: list = (
            datetime.datetime.utcfromtimestamp(round(time.time()))
            .strftime("%Y %m")
            .split()
        )
        last_update_time: list = (
            datetime.datetime.utcfromtimestamp(self.last_updated)
            .strftime("%Y %m")
            .split()
        )

        if (
            last_update_time[YEAR_INDEX] < current_time[YEAR_INDEX]
            or last_update_time[MONTH_INDEX] < last_update_time[MONTH_INDEX]
        ):
            return False
        else:
            return True

    def download_db(self) -> None:
        if self.cfg.ip2location_token == "":
            console.print(
                "To automatically download IP2Location database, a IP2Location LITE token must be provided! Either provide it in the config, or use manual update.",
                style="red",
            )
            exit(1)

        # Download the dbs
        db_zips: tuple = (
            f"{self.ip2l_dbs}/{self.cfg.ip2location_db_bin}.zip",
            f"{self.ip2l_dbs}/{self.cfg.ip2location_db_csv}.zip",
        )
        
        urllib.request.urlretrieve(f"https://www.ip2location.com/download/?token={self.cfg.ip2location_token}&file={self.cfg.ip2location_bin_code}", db_zips[0])
        urllib.request.urlretrieve(f"https://www.ip2location.com/download/?token={self.cfg.ip2location_token}&file={self.cfg.ip2location_csv_code}", db_zips[1])

        for db_zip in db_zips:
            with ZipFile(db_zip, "r") as f:
                f.extractall(path=self.ip2l_dbs)

        self.create_last_updated_file()

    def get_user_answers(self, message: str) -> None:
        console.print(
            message,
            style="yellow",
            end="",
        )
        user_input: str = input().upper()
        if user_input == IP2LocManagerUserAnswers.UPDATE.value:
            self.download_db()
        elif user_input == IP2LocManagerUserAnswers.MANUAL_UPDATE.value:
            self.create_last_updated_file()
            exit(0)
        elif user_input == IP2LocManagerUserAnswers.SKIP.value:
            return
        elif user_input == IP2LocManagerUserAnswers.DISABLE.value:
            # Unused
            self.cfg.use_ip2location = False
        elif user_input == IP2LocManagerUserAnswers.EXIT.value:
            exit(1)
        else:
            console.print("Unknown answer", style="red")
            exit(1)
