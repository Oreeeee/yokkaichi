# Import modules
import argparse
import pathlib
import platform
import time
from datetime import datetime

import tomli

from yokkaichi import __version__

from . import config_loader, env_loader
from .constants import console
from .IP2L_Manager import IP2L_Manager
from .port_parser import parse_port_range
from .ServerScan import ServerScan
from .structs import EnvVariables


def display_version() -> None:
    console.print(
        f"yokkaichi [bold cyan]{__version__}[/bold cyan] on [bold cyan]{platform.python_implementation()} {platform.python_version()}[/bold cyan]",
        style="green",
    )
    exit()


def load_ip_list(ip_list_location) -> list:
    ips = []
    # Load file
    try:
        with open(ip_list_location, "r") as f:
            ip_list = f.readlines()
            for ip in ip_list:
                ips.append(ip.strip())
    except FileNotFoundError:
        console.print("ERROR! IP LIST/MASSCAN LIST NOT FOUND!", style="red")
        exit(1)

    return ips


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="Configuration file (example one will be created if it doesn't exist)",
        default=None,
        const="yokkaichi.toml",
        nargs="?",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="show_version",
        help="Show version and quit",
        action="store_true",
    )
    parser.set_defaults(config_file="yokkaichi.toml")
    args = parser.parse_args()

    if args.show_version:
        # Show the version and exit
        display_version()

    # Load the config file
    if args.config_file != None:
        try:
            cfg = config_loader.parse_cfg(args.config_file)
        except tomli.TOMLDecodeError:
            console.print(
                "Config file is invalid! (Failed parsing TOML)", style="bold red"
            )
        except FileNotFoundError:
            console.print(
                f"[bold white]{args.config_file}[/bold white] doesn't exist. Create a sample config in this location? (y/n) ",
                style="yellow",
                end="",
            )
            if input().lower() == "y":
                config_loader.write_cfg(args.config_file)
                console.print(
                    f"Created a new config file at [bold white]{args.config_file}[/bold white]. Adjust it to your preferences",
                    style="green",
                )
                exit(0)

    # Load environment variables
    env_variables: EnvVariables = env_loader.load_env()

    # Check does output file exists
    if pathlib.Path(cfg.output).is_file():
        console.print(
            "Output file exists. Continuing will overwrite this file. Proceed? (y/n) ",
            style="yellow",
            end="",
        )
        if input().lower() == "n":
            exit(0)
    else:
        # Touch the file
        pathlib.Path(cfg.output).touch()

    if cfg.use_ip2location:
        # Initialize IP2Location
        ip2location: IP2L_Manager = IP2L_Manager(cfg, env_variables)
    else:
        ip2location: None = None

    if cfg.use_ip2location and cfg.masscan_scan and cfg.masscan_country_scan:
        masscan_country_file: str = ip2location.get_country_cidr()
    else:
        masscan_country_file: str = ""

    if cfg.ip_list_scan:
        console.print("Loading IPs", style="cyan")
        ip_list: list = load_ip_list(cfg.ip_list)
        console.print(f"Loaded {len(ip_list)} IPs", style="green")
    else:
        ip_list: list = None

    scan_start = time.time()

    scanner = ServerScan(
        cfg=cfg,
        ip_list=ip_list,
        masscan_country_file=masscan_country_file,
        ip2location=ip2location,
    )
    scanner.start_scan()

    scan_end = time.time()

    # Show results
    scan_start_time = datetime.fromtimestamp(scan_start).isoformat()
    scan_end_time = datetime.fromtimestamp(scan_end).isoformat()
    scan_time = time.strftime("%H:%M:%S", time.gmtime(scan_end - scan_start))
    console.print(
        f"[bold white]{len(scanner.results_obj.results)}[/bold white] servers found.\nStarted: [bold white]{scan_start_time}[/bold white].\nEnded: [bold white]{scan_end_time}[/bold white].\nTook [bold white]{scan_time}[/bold white].",
        style="magenta",
    )


if __name__ == "__main__":
    main()
