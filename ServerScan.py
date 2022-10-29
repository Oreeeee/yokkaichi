# Import modules
from mcstatus import BedrockServer, JavaServer
import colorama as clr
import threading
import json


class ServerScan:
    def __init__(self, ips, ports, platforms, output_file):
        self.ips = ips
        self.ports = ports
        self.platforms = platforms
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
                if "Java" in self.platforms:
                    self.connect_java(ip, port)

                if "Bedrock" in self.platforms:
                    self.connect_bedrock(ip, port)

    def connect_java(self, ip, port):
        try:
            server_lookup = JavaServer.lookup(f"{ip}:{port}")
        except Exception as e:
            with self.lock:
                print(clr.Fore.RED + f"[-] {ip}:{port} is offline!")

        # Get player list
        try:
            player_list = server_lookup.query().players.names
        except Exception as e:
            player_list = None
            print(clr.Fore.YELLOW + f"[!] Query failed for {ip}:{port} - {e}")

        server_info = {
            "ip": ip,
            "port": port,
            "ping": round(server_lookup.status().latency),
            "platform": "Java",
            "motd": server_lookup.status().description,
            "version": server_lookup.status().version.name,
            "online_players": server_lookup.status().players.online,
            "max_players": server_lookup.status().players.max,
            "player_list": player_list,
            "whitelist": "TODO",
            "cracked": "TODO"
        }

        with self.lock:
            print(
                clr.Fore.GREEN + f"[+] Java server found at {ip}:{port}!")
            self.add_to_file(server_info)

    def connect_bedrock(self, ip, port):
        try:
            server_lookup = BedrockServer.lookup(f"{ip}:{port}")
        except Exception as e:
            with self.lock:
                print(clr.Fore.RED + f"[-] {ip}:{port} is offline!")

        # Get player list
        try:
            player_list = server_lookup.query().players.names
        except Exception as e:
            player_list = None
            print(clr.Fore.YELLOW + f"[!] Query failed for {ip}:{port} - {e}")

        server_info = {
            "ip": ip,
            "port": port,
            "ping": round(server_lookup.status().latency),
            "platform": "Java",
            "motd": server_lookup.status().description,
            "version": server_lookup.status().version.name,
            "online_players": server_lookup.status().players.online,
            "max_players": server_lookup.status().players.max,
            "player_list": player_list,
            "whitelist": "TODO",
            "cracked": "TODO"
        }

        with self.lock:
            print(
                clr.Fore.GREEN + f"[+] Bedrock server found at {ip}:{port}!")
            self.add_to_file(server_info)

    def add_to_file(self, server_info):
        self.results["server_list"].append(server_info)
        print(self.results)
        with open(self.output_file, "w") as f:
            f.write(json.dumps(self.results, indent=4))
