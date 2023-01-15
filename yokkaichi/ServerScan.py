# Import modules
from mcstatus import BedrockServer, JavaServer
import colorama as clr
import IP2Location
import threading
import json
import ast


class ServerScan:
    def __init__(
        self,
        ports,
        platforms,
        query,
        ip2location_db_file,
        ip2location_cache,
        output_file,
        ip_list,
        masscan_list,
    ):
        self.ip_list = ip_list
        self.masscan_list = masscan_list
        self.ports = ports
        self.platforms = platforms
        self.query = query
        self.ip2location_db_file = ip2location_db_file
        self.ip2location_cache = ip2location_cache
        self.output_file = output_file

        self.results = {"server_list": []}
        self.lock = threading.Lock()

    def start_scan(self, thread_count):
        if self.ip2location_db_file != "":
            print(clr.Fore.CYAN + "Loading IP2Location database")
            if self.ip2location_cache:
                self.ip2location_db = IP2Location.IP2Location(
                    self.ip2location_db_file, "SHARED_MEMORY"
                )
            else:
                self.ip2location_db = IP2Location.IP2Location(self.ip2location_db_file)

        print(clr.Fore.CYAN + f"Loading {thread_count} threads!")

        thread_list = []

        for _ in range(thread_count):
            thread = threading.Thread(target=self.scan_server)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        # Show results
        server_count = len(self.results["server_list"])
        print(clr.Fore.MAGENTA + f"{server_count} servers found")

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
                        clr.Fore.WHITE
                        + f"No more IPs in masscan in thread {threading.current_thread().name}"
                    )
                    return
                ports = []
                for port_info in self.masscan_list["scan"][ip]:
                    ports.append(port_info["port"])
                self.masscan_list["scan"].pop(ip)

            for port in ports:
                for server_platform in self.platforms:
                    try:
                        self.check_server(ip, port, server_platform)
                    except Exception:
                        with self.lock:
                            print(
                                clr.Fore.RED
                                + f"[-] {ip}:{port} for {server_platform} is offline!"
                            )

    def scan_ip_list(self):
        while True:
            try:
                with self.lock:
                    ip = self.ip_list[0]
                    self.ip_list.pop(0)
            except IndexError:
                print(
                    clr.Fore.WHITE
                    + f"No more IPs in IP list in thread {threading.current_thread().name}"
                )
                return

            for port in self.ports:
                for server_platform in self.platforms:
                    try:
                        self.check_server(ip, port, server_platform)
                    except Exception as e:
                        with self.lock:
                            print(
                                clr.Fore.RED
                                + f"[-] {ip}:{port} for {server_platform} is offline!"
                            )

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
                print(clr.Fore.YELLOW + f"[!] Query failed for {ip}:{port}")
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
                clr.Fore.GREEN + f"[+] {server_platform} server found at {ip}:{port}!"
            )
            self.add_to_file(server_info)

    def get_location_data(self, ip):
        if self.ip2location_db_file == "":
            # Return None if the database doesn't exist
            return None

        # Make the data be a string
        ip2location_data_str = str(self.ip2location_db.get_all(ip))
        # Convert the data to dict
        ip2location_data_dict = ast.literal_eval(ip2location_data_str)

        return ip2location_data_dict

    def add_to_file(self, server_info):
        self.results["server_list"].append(server_info)
        with open(self.output_file, "w") as f:
            f.write(json.dumps(self.results, indent=4))
