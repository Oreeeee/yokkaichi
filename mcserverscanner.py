# Import modules
from threading import Thread, Lock
from mcstatus import BedrockServer
from mcstatus import JavaServer
import colorama as clr
import IP2Location
import threading
import platform
import argparse
import csv


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


def scan_server(lock, ips):
    try:
        ip = ips[0]
        ips.pop(0)
    except IndexError:
        print(clr.Fore.WHITE +
              f"No more IPs, exiting thread {threading.current_thread().name}")
        return True

    if args.java == True:
        for port in args.ports:
            try:
                server = JavaServer.lookup(f"{ip}:{port}")
                motd = server.status().description
                players_online = server.status().players.online
                players_max = server.status().players.max
                ping = round(server.status().latency)
                version = server.status().version.name
                with lock:
                    print(
                        clr.Fore.GREEN + f"[+] Java server found at {ip}:{port}! Motd: {motd}, players online: {players_online}/{players_max}, ping {ping}ms, version {version}.")
            except Exception:
                with lock:
                    print(clr.Fore.RED + f"[-] {ip}:{port} is offline!")
    if args.bedrock == True:
        for port in args.ports:
            try:
                server = BedrockServer.lookup(f"{ip}:{port}")
                motd = server.status().description
                players_online = server.status().players.online
                players_max = server.status().players.max
                ping = round(server.status().latency)
                version = server.status().version.name
                with lock:
                    print(
                        clr.Fore.GREEN + f"[+] Bedrock server found at {ip}:{port}! Motd: {motd}, players online: {players_online}/{players_max}, ping {ping}ms, version {version}.")
            except Exception:
                with lock:
                    print(clr.Fore.RED + f"[-] {ip}:{port} is offline!")


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
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()
        thread.join()


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
    parser.add_argument("-t", "--threads", dest="thread_count",
                        help="Number of threads (default: 100)", type=int, default=100)
    parser.set_defaults(java=False, bedrock=False)
    args = parser.parse_args()

    # if args.java and args.bedrock == False:
    #     print("You need to choose either Java or Bedrock")
    #     exit(1)

    main()
