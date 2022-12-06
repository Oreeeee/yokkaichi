# Import modules
from MasscanScan import MasscanScan
from ServerScan import ServerScan
import colorama as clr
import platform
import argparse


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


def main():
    if platform.system() == "Windows":
        # Init colorama if on Windows
        clr.init()

    # Check does output file exists
    try:
        open(args.output_file, "r").close()
    except FileNotFoundError:
        print(clr.Fore.RED + "Given output file doesn't exist!")
        exit(1)

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
        # Load masscan IP list
        masscan_ips = load_ip_list(args.masscan_ip_list)
        # Start masscan
        masscan_scanner = MasscanScan(masscan_ips, args.ports, args.masscan_args)
        masscan_results = masscan_scanner.start_scan()
    else:
        masscan_results = None

    # print(clr.Fore.CYAN + "Loading IPs")
    # ips = load_file()

    ServerScan(
        ip_list=None,
        masscan_list=masscan_results,
        ports=args.ports,
        platforms=platforms,
        query=args.query,
        check_country=args.check_country,
        output_file=args.output_file,
    ).start_scan(args.thread_count)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
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
        "--masscan-country",
        dest="masscan_country",
        help="Country to scan in 2-letter format",
        type=str,
    )
    parser.add_argument(
        "--masscan-args",
        dest="masscan_args",
        help="Arguments for masscan (example: --max-rate 1000)",
        type=str,
        default="",
    )
    parser.add_argument(
        "-p", "--ports", dest="ports", help="Ports to scan on", nargs="+"
    )
    parser.add_argument(
        "-q",
        "--query",
        dest="query",
        help="Query servers, required for player list but slows down the script",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--check-country",
        dest="check_country",
        help="Check server location, provide IP2Location BIN database location",
        type=str,
        default="",
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
