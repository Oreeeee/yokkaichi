# Import modules
from ServerScan import ServerScan
import colorama as clr
import platform
import argparse


def load_file():
    ips = []
    # Load file
    try:
        with open(args.ip_list_file, "r") as f:
            ip_list = f.readlines()
            for ip in ip_list:
                ips.append(ip.strip())
    except FileNotFoundError:
        print(clr.Back.RED + clr.Fore.WHITE + "ERROR! FILE NOT FOUND!")
        exit(1)

    return ips


def main():
    if platform.system() == "Windows":
        # Init colorama if on Windows
        clr.init()

    # Check does output file exists
    if args.output_file != None:
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

    print(clr.Fore.CYAN + "Loading IPs")
    ips = load_file()

    ServerScan(ips, args.ports, platforms, args.query,
               args.output_file).start_scan(args.thread_count)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--java", dest="java",
                        help="Scan for Java servers", action="store_true")
    parser.add_argument("-b", "--bedrock", dest="bedrock",
                        help="Scan for Bedrock servers", action="store_true")
    parser.add_argument("-l", "--ip-list", dest="ip_list_file",
                        help="Location to a file with IP addresses to scan", type=str)
    parser.add_argument("-p", "--ports", dest="ports", action="append",
                        help="Ports to scan on")
    parser.add_argument("-q", "--query", dest="query",
                        help="Query servers, required for player list but slows down the script", action="store_true")
    parser.add_argument("-t", "--threads", dest="thread_count",
                        help="Number of threads (default: 100)", type=int, default=100)
    parser.add_argument("-o", "--output", dest="output_file",
                        help="Output JSON file", default=None)
    parser.set_defaults(java=False, bedrock=False, query=False)
    args = parser.parse_args()

    # if args.java and args.bedrock == False:
    #     print("You need to choose either Java or Bedrock")
    #     exit(1)

    main()
