import dataclasses
import json
import queue
import socket
import time
import traceback
from datetime import datetime
from queue import Queue
from threading import Lock, Thread

from mcstatus import BedrockServer, JavaServer
from pyScannerWrapper.structs import ServerResult

from .enums import OfflinePrintingModes, Platforms
from .IP2L_Manager import IP2L_Manager
from .Printer import Printer
from .structs import CFG, MinecraftServer


class Checker:
    checking: bool = True
    running: bool = True
    thread: Thread = None

    def __init__(
        self,
        cfg: CFG,
        ip2location: IP2L_Manager,
        print_lock: Lock,
        queue: Queue,
        results_collection
    ):
        self.cfg: CFG = cfg
        self.ip2location: IP2L_Manager = ip2location
        self.queue = queue
        self.print_lock: Lock = Lock()
        self.results_collection = results_collection

    def start(self) -> None:
        """
        This method starts the scanning thread for the current instance of Checker
        """
        self.thread = Thread(target=self.scan_queue)
        self.thread.start()

    def scan_queue(self) -> None:
        while self.running:
            self.checking = False  # Set checking status to False every iteration
            try:
                mas_result: ServerResult = self.queue.get(timeout=0.01)
                self.checking = True  # We got a server, that means we are checking
            except queue.Empty:
                continue

            for server_platform in self.cfg.platforms:
                try:
                    self.check_server(mas_result.ip, mas_result.port, server_platform)
                except socket.error as e:
                    with self.print_lock:
                        if (
                            self.cfg.offline_printing
                            == OfflinePrintingModes.OFFLINE.value
                        ):
                            Printer.server_offline(
                                ip=mas_result.ip,
                                port=mas_result.port,
                                platform=server_platform.value,
                            )
                except Exception as e:
                    if (
                            self.cfg.offline_printing
                            == OfflinePrintingModes.OFFLINE.value
                        ):
                            Printer.connection_exception(
                                ip=mas_result.ip,
                                port=mas_result.port,
                                platform=server_platform.value,
                                exception=e,
                            )

    def check_server(self, ip: str, port: int, server_platform: Platforms) -> None:
        if server_platform == Platforms.JAVA:
            server_lookup = JavaServer.lookup(f"{ip}:{port}", timeout=self.cfg.timeout)
        if server_platform == Platforms.BEDROCK:
            server_lookup = BedrockServer.lookup(
                f"{ip}:{port}", timeout=self.cfg.timeout
            )

        # Get player list
        if self.cfg.query_java:
            try:
                player_list = server_lookup.query().players.names
            except Exception as e:
                Printer.query_failed(ip=ip, port=port)
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

        self.results_obj.add_to_file(server_info)
        with self.print_lock:
            self.results_collection.insert_one(dataclasses.as_dict(server_info))

