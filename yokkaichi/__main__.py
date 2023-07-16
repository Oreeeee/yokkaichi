# Import modules
import argparse
import pathlib
import platform
import time
from datetime import datetime

import IP2Location
import requests
import tomli

from yokkaichi import __version__

from . import config_loader
from .args_to_cfg import args_to_cfg
from .constants import console
from .enums import MasscanMethods
from .port_parser import parse_port_range
from .ServerScan import ServerScan


def display_version() -> None:
    console.print(
        f"yokkaichi [bold cyan]{__version__}[/bold cyan] on [bold cyan]{platform.python_implementation()} {platform.python_version()}[/bold cyan]",
        style="green",
    )
    exit()


def get_country_ips(countries) -> list:
    console.print(
        "Note: IP Ranges provided by the tool might be inaccurate or incomplete. This will be fixed in the future releases. Sorry about that.",
        style="yellow",
    )
    country_ip_list = []
    for country in countries:
        # Download CIDRs for country
        cidr_list = requests.get(
            f"https://raw.githubusercontent.com/herrbischoff/country-ip-blocks/master/ipv4/{country.lower()}.cidr"
        )
        # Check is the country valid
        if cidr_list.text == "404: Not Found":
            console.print(
                f"[bold white]{country}[/bold white] is not a proper 2-letter code!",
                style="red",
            )
            continue
        # Add IPs to IP list
        for ip in cidr_list.text.splitlines():
            country_ip_list.append(ip)

    return country_ip_list


def verify_ip2location(db) -> None:
    if not pathlib.Path(db).is_file():
        console.print("IP2Location database doesn't exist", style="bold red")
        exit(1)

    try:
        IP2Location.IP2Location(db)
    except ValueError:
        # IP2Location's default exception messages are okay
        console.print("The IP2Location database is corrupted", style="bold red")
        exit(1)


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


def main(cfg):
    if args.show_version:
        # Show the version and exit
        display_version()

    # Load the config file
    if args.config_file != None:
        try:
            cfg = config_loader.parse_cfg(args.config_file)
            # TODO: Make use of it
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
        verify_ip2location(cfg.ip2location_db)

    scan_start = time.time()

    if cfg.ip_list_scan:
        console.print("Loading IPs", style="cyan")
        ip_list: list = load_ip_list(cfg.ip_list)
        console.print(f"Loaded {len(ip_list)} IPs", style="green")
    else:
        ip_list: list = None

    if cfg.masscan_scan:
        masscan_ips_file: list = []
        masscan_ips_countries: list = []
        if cfg.masscan_ip_source == MasscanMethods.COUNTRIES:
            # Get CIDR ranges for countries
            masscan_ips_file = get_country_ips(cfg.masscan_country_list)
        if cfg.masscan_ip_source == MasscanMethods.LIST:
            # Load masscan IP list
            masscan_ips_countries = load_ip_list(cfg.masscan_ip_list)

        # Combine two sources of masscan IPs together
        masscan_ips: list = masscan_ips_file + masscan_ips_countries
    else:
        masscan_ips: list = None

    # print(clr.Fore.CYAN + "Loading IPs")
    # ips = load_file()

    scanner = ServerScan(cfg=cfg, ip_list=ip_list, masscan_list=masscan_ips)
    scanner.start_scan()

    scan_end = time.time()

    # Show results
    scan_start_time = datetime.fromtimestamp(scan_start).isoformat()
    scan_end_time = datetime.fromtimestamp(scan_end).isoformat()
    scan_time = time.strftime("%H:%M:%S", time.gmtime(scan_end - scan_start))
    console.print(
        f"[bold white]{len(scanner.results)}[/bold white] servers found.\nStarted: [bold white]{scan_start_time}[/bold white].\nEnded: [bold white]{scan_end_time}[/bold white].\nTook [bold white]{scan_time}[/bold white].",
        style="magenta",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "-j", "--java", dest="java", help="Scan for Java servers", action="store_true"
    )
    parser.add_argument(
        "-b",
        "--bedrock",
        dest="bedrock",
        help="Scan for Bedrock servers",
        action="store_true",
    )
    parser.add_argument(
        "--ip-list-scan",
        dest="ip_list_scan",
        help="Scan from IP list (slow and outdated, use masscan instead)",
        action="store_true",
    )
    parser.add_argument(
        "--ip-list", dest="ip_list", help="Location to IP List", type=str, default=""
    )
    parser.add_argument(
        "--masscan",
        dest="masscan",
        help="Enable scanning with masscan",
        action="store_true",
    )
    parser.add_argument(
        "--masscan-method",
        dest="masscan_method",
        help="Where to look for IPs for masscan? Possible values: countries, list",
        type=str,
        default="countries",
    )
    parser.add_argument(
        "--masscan-ip-list",
        dest="masscan_ip_list",
        help="Location to IP (or CIDR) list to scan by masscan before scanning with mcserver scanner",
        type=str,
        default="",
    )
    parser.add_argument(
        "--masscan-countries",
        dest="masscan_countries",
        help="Countries to scan in 2-letter format",
        nargs="+",
    )
    parser.add_argument(
        "--masscan-args",
        dest="masscan_args",
        help="Arguments for masscan (example: --max-rate 1000)",
        type=str,
        default="",
    )
    parser.add_argument(
        "--masscan-output",
        dest="masscan_json_output",
        help="Output results to a file. To be used for debugging purposes.",
        type=str,
        default="",
    )
    parser.add_argument(
        "-p",
        "--ports",
        dest="ports",
        help="Ports to scan on. Example format: 25560-25569,42069. Uses 25565 by default",
        type=str,
        default="25565",
    )
    parser.add_argument(
        "--query",
        dest="query",
        help="Query servers, required for player list but slows down the script (Note: might be broken at the moment)",
        action="store_true",
    )
    parser.add_argument(
        "--ip2location-db",
        dest="ip2location_db",
        help="IP2Location BIN database location, required for providing geolocation info",
        type=str,
        default="",
    )
    parser.add_argument(
        "--ip2location-cache",
        dest="ip2location_cache",
        help="Cache IP2Location database to RAM. Make sure you have enough RAM to use this feature",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--threads",
        dest="thread_count",
        help="Number of threads (default: 100)",
        type=int,
        default=100,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Output JSON file",
        default="out.json",
    )
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
    parser.set_defaults(java=False, bedrock=False, query=False)
    args = parser.parse_args()

    cfg = args_to_cfg(args)

    # if args.java and args.bedrock == False:
    #     print("You need to choose either Java or Bedrock")
    #     exit(1)

    main(cfg)
