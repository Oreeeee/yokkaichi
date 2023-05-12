from .constants.rich_console import console
from pathlib import Path
import platform
import masscan
import json


class MasscanScan:
    def __init__(self, cfg, ip_list):
        # Declare variables
        self.cfg = cfg
        self.ip_list = ip_list

        # Create masscan object
        self.mas = masscan.PortScanner()

        # Convert IP and port list to masscan friendly format
        self.mas_ip_list = self.convert_ip_list()
        self.mas_port_list = self.convert_port_list()

    def convert_ip_list(self):
        mas_ip_list = ""
        for ip in self.ip_list:
            # Add a space every IP in the list
            mas_ip_list += f" {ip}"

        # Remove the first space
        mas_ip_list = mas_ip_list[1:]

        return mas_ip_list

    def convert_port_list(self):
        mas_port_list = ""
        for port in self.cfg.ports:
            # Add a comma every port in the list
            mas_port_list += f",{port}"

        # Remove the first comma
        mas_port_list = mas_port_list[1:]

        return mas_port_list

    def save_output(self, masscan_results):
        Path(self.cfg.masscan_output_location).touch()
        with open(self.cfg.masscan_output_location, "w") as f:
            f.write(json.dumps(masscan_results, indent=4))
        console.print(
            f"Saved masscan results to [bold cyan]{self.cfg.masscan_output_location}[/bold cyan]",
            style="green",
        )

    def start_scan(self):
        console.print(
            f"Starting masscan with [bold white]{len(self.ip_list)}[/bold white] entries and [bold white]{len(self.cfg.ports)}[/bold white] ports",
            style="cyan",
        )
        if platform.system() == "Windows":
            console.print(
                "If the scanning doesn't work, start this script as admin!",
                style="bold yellow",
            )
            self.mas.scan(
                self.mas_ip_list,
                ports=self.mas_port_list,
                arguments=self.cfg.masscan_args,
            )
        else:
            self.mas.scan(
                self.mas_ip_list,
                ports=self.mas_port_list,
                arguments=self.cfg.masscan_args,
                sudo=True,
            )

        # Dict-ify masscan results
        masscan_results = json.loads(self.mas.scan_result)

        online_ip_amount = len(masscan_results["scan"])
        # Calculate open port amount
        open_port_amount = 0
        for online_ip in masscan_results["scan"]:
            open_port_amount += len(masscan_results["scan"][online_ip])

        console.print(
            f"[bold white]{open_port_amount}[/bold white] ports open on [bold white]{online_ip_amount}[/bold white] IPs",
            style="green",
        )

        # Save the results if provided
        if self.cfg.masscan_output:
            self.save_output(masscan_results)

        return masscan_results
