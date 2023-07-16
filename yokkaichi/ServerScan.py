# Import modules
import ast
import json
import platform
import queue
import threading
import time
from datetime import datetime
from queue import Queue

import IP2Location
import pyScannerWrapper
from mcstatus import BedrockServer, JavaServer
from pyScannerWrapper.structs import ServerResult

from .constants import console
from .enums import Platforms
from .structs import CFG


class ServerScan:
    def __init__(self, cfg, ip_list, masscan_list) -> None:
        self.cfg: CFG = cfg

        self.results: list = []
        self.ip_list: list = ip_list
        self.masscan_list: list = masscan_list
        self.lock: threading.Lock = threading.Lock()
        self.queue: Queue = Queue()
        self.running: bool = False

        if self.cfg.use_ip2location:
            console.print("Loading IP2Location database", style="cyan")
            if self.cfg.ip2location_cache:
                self.ip2location_db = IP2Location.IP2Location(
                    self.cfg.ip2location_db, "SHARED_MEMORY"
                )
            else:
                self.ip2location_db = IP2Location.IP2Location(self.cfg.ip2location_db)

    def start_scan(self) -> None:
        console.print(
            f"Loading [bold white]{self.cfg.threads}[/bold white] threads!",
            style="cyan",
        )

        self.running = True

        thread_list: list = []

        for _ in range(self.cfg.threads):
            thread: threading.Thread = threading.Thread(target=self.scan_queue)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        # masscan
        if self.cfg.masscan_scan:
            mas: pyScannerWrapper.scanners.Masscan = pyScannerWrapper.scanners.Masscan()
            mas.args = self.cfg.masscan_args
            mas.input_ip_list = self.masscan_list
            mas.input_port_list = self.cfg.ports
            if platform.system() == "Linux":
                mas.sudo = True
            mas_yielder = mas.scan_yielder()
            for server in mas_yielder:
                self.queue.put(server)

        # Servers from the IP List
        if self.cfg.ip_list_scan:
            for ip in self.ip_list:
                for port in self.cfg.ports:
                    self.queue.put(ServerResult(ip=ip, port=port))

        # Stop the scanning and wait for all threads to stop
        self.running = False
        for thread in thread_list:
            thread.join()

    def scan_queue(self) -> None:
        while self.running:
            try:
                mas_result: ServerResult = self.queue.get(timeout=1)
            except queue.Empty:
                continue

            for server_platform in self.cfg.platforms:
                try:
                    self.check_server(mas_result.ip, mas_result.port, server_platform)
                except Exception as e:
                    with self.lock:
                        console.print(
                            f"[-] {mas_result.ip}:{mas_result.port} for {server_platform.value} is offline!",
                            style="red",
                        )

    def check_server(self, ip, port, server_platform) -> None:
        if server_platform == Platforms.JAVA:
            server_lookup = JavaServer.lookup(f"{ip}:{port}")
        if server_platform == Platforms.BEDROCK:
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
            "platform": server_platform.value,
            "motd": "",
            "version": "",
            "online_players": 0,
            "max_players": 0,
            "player_list": player_list,
            "time_discovered": datetime.now().isoformat(),
        }
        if server_platform == Platforms.JAVA:
            server_info["motd"] = server_lookup.status().description
            server_info["version"] = server_lookup.status().version.name
            server_info["online_players"] = server_lookup.status().players.online
            server_info["max_players"] = server_lookup.status().players.max
        if server_platform == Platforms.BEDROCK:
            server_info["motd"] = server_lookup.status().motd
            server_info["version"] = ""
            server_info["online_players"] = server_lookup.status().players_online
            server_info["max_players"] = server_lookup.status().players_max

        with self.lock:
            console.print(
                f"[+] {server_platform.value} server found at {ip}:{port}!",
                style="green",
            )
            self.add_to_file(server_info)

    def get_location_data(self, ip) -> dict:
        if not self.cfg.use_ip2location:
            return None
        # Make the data be a string
        ip2location_data_str: str = str(self.ip2location_db.get_all(ip))
        # Convert the data to dict
        ip2location_data_dict: dict = ast.literal_eval(ip2location_data_str)

        return ip2location_data_dict

    def add_to_file(self, server_info) -> None:
        self.results.append(server_info)
        with open(self.cfg.output, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
