import csv
import datetime
import ipaddress
import os
import pathlib
import platform
import time
from uuid import uuid4

from IP2Location import IP2Location

from .enums import IP2LocDBStatus
from .Printer import Printer
from .structs import CFG


class IP2L_Manager:
    def __init__(self, cfg: CFG) -> None:
        self.cfg = cfg
        self.ip2l_dbs: str = self.cfg.ip2location_dbs

        # Try to open the last updated date file
        opening_status: IP2LocDBStatus = self.open_last_updated_file()
        if opening_status == IP2LocDBStatus.DOESNT_EXIST:
            Printer.ip2l_db_doesnt_exist()
            self.cfg.use_ip2location = False

        if opening_status == IP2LocDBStatus.INCORRECT_DATE:
            Printer.cant_get_ip2l_last_update_date()

        if opening_status == IP2LocDBStatus.EXISTS:
            if not self.is_up_to_date():
                Printer.ip2l_db_outdated()

        # Load DB
        Printer.loading_db()
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
            Printer.db_corrupted()
            self.cfg.use_ip2location = False

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
        if not self.cfg.ip2location_check_for_updates:
            return True

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
            or last_update_time[MONTH_INDEX] < current_time[MONTH_INDEX]
        ):
            return False
        else:
            return True

    def get_country_cidr_file(self) -> str:
        IP_START_INDEX: int = 0
        IP_END_INDEX: int = 1
        COUNTRY_CODE_INDEX: int = 2

        ip_list: list = []
        with open(
            f"{self.ip2l_dbs}/{self.cfg.ip2location_db_csv}", "r", newline=""
        ) as f:
            ip2l_reader: csv.reader = csv.reader(f)
            for row in ip2l_reader:
                if row[COUNTRY_CODE_INDEX] in self.cfg.countries:
                    ip_list.append(
                        [
                            str(ipaddr)
                            for ipaddr in ipaddress.summarize_address_range(
                                ipaddress.IPv4Address(int(row[IP_START_INDEX])),
                                ipaddress.IPv4Address(int(row[IP_END_INDEX])),
                            )
                        ][0]
                    )

        # Write the list into a temp file
        if platform.system() == "Windows":
            temp_dir: str = "%temp%"
        else:
            temp_dir: str = "/tmp"
        ip_list_loc: str = f"{temp_dir}/{uuid4()}"
        with open(ip_list_loc, "w") as f:
            for ip in ip_list:
                f.write(ip + "\n")

        return ip_list_loc
