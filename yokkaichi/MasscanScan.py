from pathlib import Path
import colorama as clr
import platform
import masscan
import json


class MasscanScan:
    def __init__(self, ip_list, port_list, masscan_args, masscan_output):
        # Declare variables
        self.ip_list = ip_list
        self.port_list = port_list
        self.masscan_args = masscan_args
        self.masscan_output = masscan_output

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
        for port in self.port_list:
            # Add a comma every port in the list
            mas_port_list += f",{port}"

        # Remove the first comma
        mas_port_list = mas_port_list[1:]

        return mas_port_list

    def save_output(self, masscan_results):
        Path(self.masscan_output).touch()
        with open(self.masscan_output, "w") as f:
            f.write(json.dumps(masscan_results, indent=4))
        print(
            clr.Fore.GREEN
            + f"Saved masscan results to {self.masscan_output}"
            + clr.Fore.RESET
        )

    def start_scan(self):
        print(
            clr.Fore.BLUE
            + f"Starting masscan with {len(self.ip_list)} entries and {len(self.port_list)} ports"
            + clr.Fore.RESET
        )
        if platform.system() == "Windows":
            print("If the scanning doesn't work, start this script as admin!")
            self.mas.scan(
                self.mas_ip_list, ports=self.mas_port_list, arguments=self.masscan_args
            )
        else:
            self.mas.scan(
                self.mas_ip_list,
                ports=self.mas_port_list,
                arguments=self.masscan_args,
                sudo=True,
            )

        # Dict-ify masscan results
        masscan_results = json.loads(self.mas.scan_result)

        online_ip_amount = len(masscan_results["scan"])
        # Calculate open port amount
        open_port_amount = 0
        for online_ip in masscan_results["scan"]:
            open_port_amount += len(masscan_results["scan"][online_ip])

        print(
            clr.Fore.GREEN + f"{open_port_amount} ports open on {online_ip_amount} IPs"
        )

        # Save the results if provided
        if self.masscan_output != "":
            self.save_output(masscan_results)

        return masscan_results
