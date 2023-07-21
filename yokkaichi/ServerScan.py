# Import modules
import dataclasses
import json
import platform
import queue
import threading
import time
import traceback
from datetime import datetime
from queue import Queue

from mcstatus import BedrockServer, JavaServer
from pyScannerWrapper.scanners import Masscan
from pyScannerWrapper.structs import ServerResult

from .constants import console
from .enums import OfflinePrintingModes, Platforms
from .IP2L_Manager import IP2L_Manager
from .structs import CFG, MinecraftServer


class ServerScan:
    def __init__(self, cfg, ip_list, masscan_country_file, ip2location) -> None:
        self.cfg: CFG = cfg

        self.results: list = []
        self.ip_list: list = ip_list
        self.masscan_country_file: list = masscan_country_file
        self.lock: threading.Lock = threading.Lock()
        self.queue: Queue = Queue()
        self.running: bool = False
        self.ip2location: IP2L_Manager = ip2location

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
            mas: Masscan = Masscan()
            mas.args = self.cfg.masscan_args
            if self.cfg.masscan_ip_scan:
                mas.args = f"{mas.args} -iL {self.cfg.masscan_ip_list}"
            if self.cfg.masscan_country_scan:
                mas.args = f"{mas.args} -iL {self.masscan_country_file}"
            # Convert ports to str
            str_ports: list = []
            for p in self.cfg.ports:
                str_ports.append(str(p))
            mas.input_port_list = str_ports
            if platform.system() == "Linux":
                mas.sudo = True
            mas_yielder = mas.scan_yielder()
            for server in mas_yielder:
                self.queue.put(server)

        # Servers from the IP List
        if self.cfg.ip_list_scan:
            for ip in self.ip_list:
                split_ip_and_port: list = ip.split(":")
                if len(split_ip_and_port) == 2:
                    self.queue.put(
                        ServerResult(ip=split_ip_and_port[0], port=split_ip_and_port[1])
                    )
                else:
                    for port in self.cfg.ports:
                        self.queue.put(ServerResult(ip=ip, port=port))

        # Stop the scanning and wait for all threads to stop
        self.running = False
        for thread in thread_list:
            thread.join()

    def scan_queue(self) -> None:
        while self.running:
            try:
                mas_result: ServerResult = self.queue.get(timeout=0.01)
            except queue.Empty:
                continue

            for server_platform in self.cfg.platforms:
                try:
                    self.check_server(mas_result.ip, mas_result.port, server_platform)
                except Exception as e:
                    with self.lock:
                        if (
                            self.cfg.offline_printing
                            == OfflinePrintingModes.OFFLINE.value
                        ):
                            console.print(
                                f"[-] {mas_result.ip}:{mas_result.port} for {server_platform.value} is offline!",
                                style="red",
                            )
                        if (
                            self.cfg.offline_printing
                            == OfflinePrintingModes.FULL_TRACEBACK.value
                        ):
                            console.print(
                                f"[-] {mas_result.ip}:{mas_result.port} for {server_platform.value} is offline!",
                                style="red",
                            )
                            traceback.print_exc()

    def check_server(self, ip: str, port: int, server_platform: Platforms) -> None:
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

        server_info: MinecraftServer = MinecraftServer(
            ip=ip,
            port=port,
            location_info=self.ip2location.get_location(ip)
            if self.ip2location != None
            else dict(),
            ping=round(server_lookup.status().latency),
            platform=server_platform.value,
            motd="",
            version="",
            online_players=0,
            max_players=0,
            player_list=player_list,
            time_discovered=datetime.now().isoformat(),
        )

        if server_platform == Platforms.JAVA:
            server_info.motd = server_lookup.status().description
            server_info.version = server_lookup.status().version.name
            server_info.online_players = server_lookup.status().players.online
            server_info.max_players = server_lookup.status().players.max
        if server_platform == Platforms.BEDROCK:
            server_info.motd = server_lookup.status().motd
            server_info.version = ""
            server_info.online_players = server_lookup.status().players_online
            server_info.max_players = server_lookup.status().players_max

        with self.lock:
            console.print(
                f"[+] {server_platform.value} server found at {ip}:{port}!",
                style="green",
            )
            self.add_to_file(server_info)

    def add_to_file(self, server_info: MinecraftServer) -> None:
        self.results.append(dataclasses.asdict(server_info))
        with open(self.cfg.output, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
