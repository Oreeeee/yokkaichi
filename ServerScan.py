from mcstatus import BedrockServer
from mcstatus import JavaServer
import colorama as clr
import threading


class ServerScan:
    def __init__(self, ips, ports, platforms, output_file):
        self.ips = ips
        self.ports = ports
        self.platforms = platforms
        self.output_file = output_file

        self.lock = threading.Lock()

    def start_scan(self, thread_count, ips):
        print(clr.Fore.CYAN + f"Loading {self.thread_count} threads!")

        thread_list = []

        for _ in range(thread_count):
            thread = threading.Thread(target=self.scan_server, args=(self.lock, ips))
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

    def scan_server(self, lock):
        while True:
            try:
                with lock:
                    ip = self.ips[0]
                    self.ips.pop(0)
            except IndexError:
                print(clr.Fore.WHITE +
                    f"No more IPs, exiting thread {threading.current_thread().name}")
                return True

            if "Java" in self.platforms:
                for port in self.ports:
                    self.scan_java(ip, port)

            if "Bedrock" in self.platforms:
                for port in self.ports:
                    self.connect_bedrock(ip, port)

    def connect_java(self, ip, port):
        try:
            server = JavaServer.lookup(f"{ip}:{port}")

            server_info = []
            server_info.append(f"{ip}:{port}")
            server_info.append(server.status().description)
            server_info.append(
                f"{server.status().players.online}/{server.status().players.max}")
            server_info.append(f"{round(server.status().latency)}ms")
            server_info.append(server.status().version.name)
            server_info.append("Java")

            file = open(args.output_file, "a")
            with self.lock:
                print(
                    clr.Fore.GREEN + f"[+] Java server found at {server_info[0]}! Motd: {server_info[1]}, players online: {server_info[2]}, ping {server_info[3]}, version {server_info[4]}.")
                with file as f:
                    write = csv.writer(file)
                    write.writerow(server_info)
        except Exception as e:
            with self.lock:
                print(clr.Fore.RED + f"[-] {ip}:{port} is offline!")
                print(e)

    def connect_bedrock(self, ip, port):
        try:
            server = BedrockServer.lookup(f"{ip}:{port}")

            server_info = []
            server_info.append(f"{ip}:{port}")
            server_info.append(server.status().description)
            server_info.append(
                f"{server.status().players.online}/{server.status().players.max}")
            server_info.append(f"{round(server.status().latency)}ms")
            server_info.append(server.status().version.name)
            server_info.append("Bedrock")

            file = open(args.output_file, "a")
            with lock:
                print(
                    clr.Fore.GREEN + f"[+] Bedrock server found at {server_info[0]}! Motd: {server_info[1]}, players online: {server_info[2]}, ping {server_info[3]}, version {server_info[4]}.")
                with file as f:
                    write = csv.writer(file)
                    write.writerow(server_info)
        except Exception as e:
            with lock:
                print(clr.Fore.RED + f"[-] {ip}:{port} is offline!")
                print(e)

    def save_to_file(self, ip, port):
        pass