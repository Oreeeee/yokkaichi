# Import modules
from .MasscanScan import MasscanScan
from .ServerScan import ServerScan
import colorama as clr
import platform
import argparse
import requests
import pathlib


def get_country_ips(countries):
    country_ip_list = []
    for country in countries:
        # Download CIDRs for country
        cidr_list = requests.get(
            f"https://raw.githubusercontent.com/herrbischoff/country-ip-blocks/master/ipv4/{country.lower()}.cidr"
        )
        # Check is the country valid
        if cidr_list.text == "404: Not Found":
            print(clr.Fore.RED + f"{country} is not a proper 2-letter code!")
            continue
        # Add IPs to IP list
        for ip in cidr_list.text.splitlines():
            country_ip_list.append(ip)

    return country_ip_list


def load_ip_list(ip_list_location):
    ips = []
    # Load file
    try:
        with open(ip_list_location, "r") as f:
            ip_list = f.readlines()
            for ip in ip_list:
                ips.append(ip.strip())
    except FileNotFoundError:
        print(clr.Back.RED + clr.Fore.WHITE + "ERROR! IP LIST/MASSCAN LIST NOT FOUND!")
        exit(1)

    return ips


def parse_port_range(arg: str) -> list:
    def verify_ints(port: any) -> None:
        try:
            int(port)
        except TypeError:
            print(clr.Fore.RED + f"Couldn't parse: {port}" + clr.Fore.RESET)
            exit(1)

    ports: list[int] = []
    # Parse all separate port/ranges, separated by commas
    separate_values: list[str] = arg.split(",")
    # Parse all ranges
    for value in separate_values:
        # Check if it's a range
        if "-" in value:
            # Parse the range
            port_range: list[str] = value.split("-")
            range_start: str = port_range[0]
            range_end: str = port_range[1]
            for port in (range_start, range_end):
                verify_ints(port)
            for port in range(
                int(range_start), int(range_end) + 1
            ):  # Range end needs to be offset by 1 to make the range inclusive
                ports.append(port)
        else:
            verify_ints(value)
            ports.append(int(value))

    return list(set(ports))


def main():
    if platform.system() == "Windows":
        # Init colorama if on Windows
        clr.init()

    # Check does output file exists
    if pathlib.Path(args.output_file).is_file():
        if (
            input(
                clr.Fore.YELLOW
                + "Output file exists. Continuing will overwrite this file. Proceed? (y/n) "
            )
            == "n"
        ):
            exit(0)
    else:
        # Touch the file
        pathlib.Path(args.output_file).touch()

    # Check does IP2Location db exist
    if args.ip2location_db != "" and not pathlib.Path(args.ip2location_db).is_file():
        print(clr.Fore.RED + "This IP2Location DB doesn't exist")
        exit(1)

    ports = parse_port_range(args.ports)

    # Add platforms to a list
    platforms = []
    if args.java:
        platforms.append("Java")
    if args.bedrock:
        platforms.append("Bedrock")

    if args.ip_list != "":
        print(clr.Fore.CYAN + "Loading IPs")
        ip_list = load_ip_list(args.ip_list)
        print(clr.Fore.GREEN + f"Loaded {len(ip_list)} IPs")
    else:
        ip_list = None

    if args.masscan:
        masscan_ips_from_file = []
        masscan_ips_for_countries = []
        if args.masscan_ip_list != "":
            # Load masscan IP list
            masscan_ips_from_file = load_ip_list(args.masscan_ip_list)
        if args.masscan_countries != None:
            # Get CIDR ranges for countries
            masscan_ips_for_countries = get_country_ips(args.masscan_countries)

        # Combine two sources of masscan IPs together
        masscan_ips = masscan_ips_from_file + masscan_ips_for_countries

        # Start masscan
        masscan_scanner = MasscanScan(
            masscan_ips, ports, args.masscan_args, args.masscan_json_output
        )
        masscan_results = masscan_scanner.start_scan()
    else:
        masscan_results = None

    # print(clr.Fore.CYAN + "Loading IPs")
    # ips = load_file()

    ServerScan(
        ip_list=None,
        masscan_list=masscan_results,
        ports=ports,
        platforms=platforms,
        query=args.query,
        ip2location_db_file=args.ip2location_db,
        ip2location_cache=args.ip2location_cache,
        output_file=args.output_file,
    ).start_scan(args.thread_count)


if __name__ == "__main__":
    # Parse arguments
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
        "--ip-list", dest="ip_list", help="Location to IP List", type=str, default=""
    )
    parser.add_argument(
        "--masscan",
        dest="masscan",
        help="Enable scanning with masscan",
        action="store_true",
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
        default=None,
        required=True,
    )
    parser.set_defaults(java=False, bedrock=False, query=False)
    args = parser.parse_args()

    # if args.java and args.bedrock == False:
    #     print("You need to choose either Java or Bedrock")
    #     exit(1)

    main()
