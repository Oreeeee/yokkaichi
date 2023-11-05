# Import modules
import ipaddress
import platform
import queue
import time
import traceback
from queue import Queue
from threading import Lock

from pyScannerWrapper.scanners import Masscan
from pyScannerWrapper.structs import ServerResult

from .Checker import Checker
from .enums import ScanTypes
from .IP2L_Manager import IP2L_Manager
from .Printer import Printer
from .Results import Results
from .structs import CFG


class ServerScan:
    def __init__(self, cfg, ip_list, ip2location) -> None:
        self.cfg: CFG = cfg
        self.ip_list: list = ip_list
        self.queue: Queue = Queue()
        self.lock: Lock = Lock()
        self.results_obj: Results = Results(cfg)
        self.ip2location: IP2L_Manager = ip2location

    def start_scan(self) -> None:
        Printer.loading_threads(thread_count=self.cfg.threads)

        checker_list: list = []

        for _ in range(self.cfg.threads):
            checker: Checker = Checker(
                self.cfg, self.ip2location, self.lock, self.results_obj, self.queue
            )
            checker_list.append(checker)

        for checker in checker_list:
            checker.start()

        # masscan
        if self.cfg.scan_type == ScanTypes.MASSCAN.value:
            mas: Masscan = Masscan()
            mas.args = self.cfg.masscan_args
            mas.args = f"{mas.args} -iL {self.ip_list}"
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

        # ping scan
        if self.cfg.scan_type == ScanTypes.PING_SCAN.value:
            ip_list_p = open(self.ip_list, "r")
            reading_file: bool = True
            while reading_file:
                line = ip_list_p.readline().strip()
                if line == "":  # Stop reading file on EOF
                    reading_file = False

                if ":" in line:  # IP:Port format
                    ip, port = line.split(":")
                    self.queue.put(ServerResult(ip=ip, port=port))
                    continue

                # Check is the line a valid IP address or CIDR range
                try:
                    ipaddress.ip_network(line)
                except ValueError:
                    traceback.print_exc()
                    continue

                if "/" in line:  # CIDR format
                    for ip in ipaddress.ip_network(line).hosts():
                        for port in self.cfg.ports:
                            self.queue.put(ServerResult(ip=str(ip), port=port))
                else:  # IP list format
                    for port in self.cfg.ports:
                        self.queue.put(ServerResult(ip=line, port=port))

            ip_list_p.close()

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
