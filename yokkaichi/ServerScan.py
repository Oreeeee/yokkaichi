# Import modules
import ast
import json
import threading
from datetime import datetime

import IP2Location
from mcstatus import BedrockServer, JavaServer

from .constants.rich_console import console


class ServerScan:
    def __init__(self, cfg, masscan_list, ip_list):
        self.cfg = cfg
        self.masscan_list = masscan_list
        self.ip_list = ip_list

        self.results = []
        self.lock = threading.Lock()

    def start_scan(self):
        if self.cfg.use_ip2location:
            console.print("Loading IP2Location database", style="cyan")
            if self.cfg.ip2location_cache:
                self.ip2location_db = IP2Location.IP2Location(
                    self.cfg.ip2location_db, "SHARED_MEMORY"
                )
            else:
                self.ip2location_db = IP2Location.IP2Location(self.cfg.ip2location_db)

        console.print(
            f"Loading [bold white]{self.cfg.threads}[/bold white] threads!",
            style="cyan",
        )

        thread_list = []

        for _ in range(self.cfg.threads):
            thread = threading.Thread(target=self.scan_server)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    def scan_server(self):
        # Scan servers from masscan list
        if self.masscan_list != None:
            self.scan_masscan()
        if self.ip_list != None:
            self.scan_ip_list()

    def scan_masscan(self):
        while True:
            # Select the first IP from the list and get the port list
            with self.lock:
                try:
                    ip = list(self.masscan_list["scan"].keys())[0]
                except IndexError:
                    print(
                        f"No more IPs in masscan in thread {threading.current_thread().name}"
                    )
                    return
                ports = []
                for port_info in self.masscan_list["scan"][ip]:
                    ports.append(port_info["port"])
                self.masscan_list["scan"].pop(ip)

            for port in ports:
                for server_platform in self.cfg.platforms:
                    try:
                        self.check_server(ip, port, server_platform)
                    except Exception:
                        with self.lock:
                            console.print(
                                f"[-] {ip}:{port} for {server_platform} is offline!",
                                style="red",
                            )

    def scan_ip_list(self):
        while True:
            with self.lock:
                try:
                    ip = self.ip_list[0]
                    self.ip_list.pop(0)
                except IndexError:
                    print(
                        f"No more IPs in IP list in thread {threading.current_thread().name}"
                    )
                    return

            for port in self.cfg.ports:
                for server_platform in self.cfg.platforms:
                    try:
                        self.check_server(ip, port, server_platform)
                    except Exception as e:
                        with self.lock:
                            console.print(
                                f"[-] {ip}:{port} for {server_platform} is offline!",
                                style="red",
                            )

    def check_server(self, ip, port, server_platform):
        if server_platform == "Java":
            server_lookup = JavaServer.lookup(f"{ip}:{port}")
        if server_platform == "Bedrock":
            server_lookup = BedrockServer.lookup(f"{ip}:{port}")

        # Get player list
        if self.cfg.query_java:
            try:
                player_list = server_lookup.query().players.names
            except Exception as e:
                console.print(f"[!] Query failed for {ip}:{port}", style="yellow")
                player_list = None
        else:
            player_list = None

        server_info = {
            "ip": ip,
            "port": port,
            "info": self.get_location_data(ip),
            "ping": round(server_lookup.status().latency),
            "platform": server_platform,
            "motd": "",
            "version": "",
            "online_players": 0,
            "max_players": 0,
            "player_list": player_list,
            "time_discovered": datetime.now().isoformat(),
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
            console.print(
                f"[+] {server_platform} server found at {ip}:{port}!", style="green"
            )
            self.add_to_file(server_info)

    def get_location_data(self, ip):
        # Make the data be a string
        ip2location_data_str = str(self.ip2location_db.get_all(ip))
        # Convert the data to dict
        ip2location_data_dict = ast.literal_eval(ip2location_data_str)

        return ip2location_data_dict

    def add_to_file(self, server_info):
        self.results.append(server_info)
        with open(self.cfg.output, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
