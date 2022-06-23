# Import modules
from threading import Thread, Lock
import colorama as clr
import IP2Location
import platform
import argparse
import csv

def load_file():
    ips = []
    # Load file
    try:
        with open(args.ip_list_file, "r") as f:
            ip_list = f.read()
            for line in ip_list:
                line.strip()
                ips.append(line)
    except FileNotFoundError:
        print(clr.Back.RED + clr.Fore.WHITE + "ERROR! FILE NOT FOUND!")
        exit(1)

    return ips

def scan_server(lock, ips):
    pass

def main():
    if platform.system() == "Windows":
        # Init colorama if on Windows
        clr.init()

    print(clr.Fore.CYAN + "Loading IPs")
    ips = load_file()

    print(clr.Fore.CYAN + f"Loading {args.thread_count} threads!")
    lock = Lock()
    thread_list = []

    for _ in range(args.thread_count):
        thread = Thread(target=scan_server, args=(lock, ips))

    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--java", dest="java", help="Scan for Java servers", action="store_true")
    parser.add_argument("-b", "--bedrock", dest="bedrock", help="Scan for Bedrock servers", action="store_true")
    parser.add_argument("-l", "--ip-list", dest="ip_list_file", help="Location to a file with IP addresses to scan", type=str)
    parser.add_argument("-p", "--ports", dest="ports", help="Ports to scan on", type=tuple, default=(25565))
    parser.add_argument("-t", "--threads", dest="thread_count", help="Number of threads (default: 100)", type=int, default=100)
    parser.set_defaults(java=False, bedrock=False)
    args = parser.parse_args()

    # if args.java and args.bedrock == False:
    #     print("You need to choose either Java or Bedrock")
    #     exit(1)

    main()