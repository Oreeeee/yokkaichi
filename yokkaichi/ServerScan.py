# Import modules
import platform
import queue
import time
from queue import Queue
from threading import Lock

from pyScannerWrapper.scanners import Masscan
from pyScannerWrapper.structs import ServerResult

from .Checker import Checker
from .constants import console
from .IP2L_Manager import IP2L_Manager
from .Results import Results
from .structs import CFG


class ServerScan:
    def __init__(self, cfg, ip_list, masscan_country_file, ip2location) -> None:
        self.cfg: CFG = cfg
        self.ip_list: list = ip_list
        self.masscan_country_file: list = masscan_country_file
        self.queue: Queue = Queue()
        self.lock: Lock = Lock()
        self.results_obj: Results = Results(cfg)
        self.ip2location: IP2L_Manager = ip2location

    def start_scan(self) -> None:
        console.print(
            f"Loading [bold white]{self.cfg.threads}[/bold white] threads!",
            style="cyan",
        )

        checker_list: list = []

        for _ in range(self.cfg.threads):
            checker: Checker = Checker(
                self.cfg, self.ip2location, self.lock, self.results_obj, self.queue
            )
            checker_list.append(checker)

        for checker in checker_list:
            checker.start()

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

        # Stop the scanning
        stopping: bool = True
        while stopping:
            # Run until queue is empty
            if not self.queue.empty():
                time.sleep(0.001)  # 100% CPU usage hack
                continue

            try:
                checker: Checker = checker_list[0]  # Grab the checker
            except IndexError:
                stopping = False
                break

            if not checker.checking:
                # Stop the checker and join to its thread
                checker.running = False
                checker.thread.join()

                # Delete the checker from checker_list once the checker thread terminates
                checker_list.pop(0)
