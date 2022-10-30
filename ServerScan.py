# Import modules
from http import server
from mcstatus import BedrockServer, JavaServer
import colorama as clr
import threading
import json


class ServerScan:
    def __init__(self, ips, ports, platforms, query, output_file):
        self.ips = ips
        self.ports = ports
        self.platforms = platforms
        self.query = query
        self.output_file = output_file

        self.results = {"server_list": []}
        self.lock = threading.Lock()

    def start_scan(self, thread_count):
        print(clr.Fore.CYAN + f"Loading {thread_count} threads!")

        thread_list = []

        for _ in range(thread_count):
            thread = threading.Thread(target=self.scan_server)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

    def scan_server(self):
        while True:
            try:
                with self.lock:
                    ip = self.ips[0]
                    self.ips.pop(0)
            except IndexError:
                print(clr.Fore.WHITE +
                      f"No more IPs, exiting thread {threading.current_thread().name}")
                return True

            for port in self.ports:
                for server_platform in self.platforms:
                    try:
                        self.check_server(ip, port, server_platform)
                    except Exception as e:
                        with self.lock:
                            print(
                                clr.Fore.RED + f"[-] {ip}:{port} for {server_platform} is offline!")

    def check_server(self, ip, port, server_platform):
        if server_platform == "Java":
            server_lookup = JavaServer.lookup(f"{ip}:{port}")
        if server_platform == "Bedrock":
            server_lookup = BedrockServer.lookup(f"{ip}:{port}")

        # Get player list
        if self.query:
            try:
                player_list = server_lookup.query().players.names
            except Exception as e:
                print(clr.Fore.YELLOW +
                      f"[!] Query failed for {ip}:{port}")
                player_list = None
        else:
            player_list = None

        server_info = {
            "ip": ip,
            "port": port,
            "ping": round(server_lookup.status().latency),
            "platform": server_platform,
            "motd": "",
            "version": "",
            "online_players": 0,
            "max_players": 0,
            "player_list": player_list,
            "whitelist": "TODO",
            "cracked": "TODO"
        }
        if server_platform == "Java":
            server_info["motd"] = server_lookup.status().description
            server_info["version"] = server_lookup.status().version.name
            server_info["online_players"] = server_lookup.status().players.online
            server_info["max_players"] = server_lookup.status().players.max
        if server_platform == "Bedrock":
            server_info["motd"] = server_lookup.status().motd
            server_info["version"] = ""
            server_info["online_players"] = server_lookup.status().players_online
            server_info["max_players"] = server_lookup.status().players_max

        with self.lock:
            print(
                clr.Fore.GREEN + f"[+] {server_platform} server found at {ip}:{port}!")
            self.add_to_file(server_info)

    def add_to_file(self, server_info):
        self.results["server_list"].append(server_info)
        with open(self.output_file, "w") as f:
            f.write(json.dumps(self.results, indent=4))
