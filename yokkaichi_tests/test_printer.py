from dataclasses import dataclass, field

from yokkaichi.Printer import Printer


@dataclass
class PrinterTest:
    method: None
    expected_output: str = ""
    expected_style: str = ""
    expected_end: str = "\n"
    kwargs: dict = field(default_factory=dict)


@dataclass
class RichPrintCall:
    objects: str
    style: str
    end: str


class FakeConsole:
    def __init__(self, allow_abbrev: bool):
        self.last_print_call: RichPrintCall = RichPrintCall("", "", "")

    def print(self, objects: str, style: str = None, end: str = "\n"):
        self.last_print_call = RichPrintCall(objects=objects, style=style, end=end)


def test_printer():
    Printer.console: FakeConsole = FakeConsole(allow_abbrev=False)

    printer_tests: list = [
        PrinterTest(
            method=Printer.version,
            expected_output="yokkaichi [bold cyan]1.6.1[/bold cyan] on [bold cyan]CPython 3.12.0[/bold cyan]",
            expected_style="green",
            kwargs={
                "version": "1.6.1",
                "py_implementation": "CPython",
                "py_version": "3.12.0",
            },
        ),
        PrinterTest(
            method=Printer.ip_list_not_found,
            expected_output="ERROR! IP LIST/MASSCAN LIST NOT FOUND!",
            expected_style="red",
        ),
        PrinterTest(
            method=Printer.toml_parse_failed,
            expected_output="Config file is invalid! (Failed parsing TOML)",
            expected_style="bold red",
        ),
        PrinterTest(
            method=Printer.cfg_doesnt_exist,
            expected_output="[bold white]yokkaichi.toml[/bold white] doesn't exist. Create a sample config in this location? (y/n) ",
            expected_style="yellow",
            expected_end="",
            kwargs={"cfg_name": "yokkaichi.toml"},
        ),
        PrinterTest(
            method=Printer.created_cfg,
            expected_output="Created a new config file at [bold white]yokkaichi.toml[/bold white]. Adjust it to your preferences",
            expected_style="green",
            kwargs={"cfg_name": "yokkaichi.toml"},
        ),
        PrinterTest(
            method=Printer.output_exists,
            expected_output="Output file exists. Continuing will overwrite this file. Proceed? (y/n) ",
            expected_style="yellow",
            expected_end="",
        ),
        PrinterTest(
            method=Printer.loading_ips,
            expected_output="Loading IPs",
            expected_style="cyan",
        ),
        PrinterTest(
            method=Printer.loaded_ips,
            expected_output="Loaded 123456 IPs",
            expected_style="green",
            kwargs={"ip_count": "123456"},
        ),
        PrinterTest(
            method=Printer.scan_complete,
            expected_output="[bold white]12345[/bold white] servers found.\nStarted: [bold white]2023-01-01T13:30:00.380493[/bold white].\nEnded: [bold white]2023-01-01T23:30:00.380493[/bold white].\nTook [bold white]10:00:00[/bold white].",
            expected_style="magenta",
            kwargs={
                "server_count": "12345",
                "scan_start_time": "2023-01-01T13:30:00.380493",
                "scan_end_time": "2023-01-01T23:30:00.380493",
                "scan_time": "10:00:00",
            },
        ),
        PrinterTest(
            method=Printer.loading_db,
            expected_output="Loading IP2Location database",
            expected_style="cyan",
        ),
        PrinterTest(
            method=Printer.db_corrupted,
            expected_output="IP2Location database is broken or corrupted!",
            expected_style="red",
        ),
        PrinterTest(
            method=Printer.set_token,
            expected_output="To automatically download IP2Location database, a IP2Location LITE token must be provided! Either set the IP2LOCATION_LITE_TOKEN environment variable, or use manual update.",
            expected_style="red",
        ),
        PrinterTest(
            method=Printer.unknown_answer,
            expected_output="Unknown answer",
            expected_style="red",
        ),
        PrinterTest(
            method=Printer.server_offline,
            expected_output="[-] 127.0.0.1:25565 for Java is offline!",
            expected_style="red",
            kwargs={"ip": "127.0.0.1", "port": "25565", "platform": "Java"},
        ),
        PrinterTest(
            method=Printer.query_failed,
            expected_output="[!] Query failed for 127.0.0.1:25565",
            expected_style="yellow",
            kwargs={"ip": "127.0.0.1", "port": "25565"},
        ),
        PrinterTest(
            method=Printer.server_found,
            expected_output="[+] Java server found at 127.0.0.1:25565!",
            expected_style="green",
            kwargs={"platform": "Java", "ip": "127.0.0.1", "port": "25565"},
        ),
        PrinterTest(
            method=Printer.couldn_parse_port,
            expected_output="Couldn't parse: [bold white]25565+25566[/bold white]",
            expected_style="red",
            kwargs={"port": "25565+25566"},
        ),
        PrinterTest(
            method=Printer.wrong_cfg_ver,
            expected_output="Wrong config version detected! Please update your config. Your config: 1. Expected: 2",
            expected_style="bold red",
            kwargs={"cfg_file_ver": "1", "cfg_ver": "2"},
        ),
        PrinterTest(
            method=Printer.loading_threads,
            expected_output="Loading [bold white]100[/bold white] threads!",
            expected_style="cyan",
            kwargs={"thread_count": "100"},
        ),
        PrinterTest(
            method=Printer.no_input_list_specified,
            expected_output="No input list specified! Choose either scanning by countries or from IP list. Quitting...",
            expected_style="red",
        ),
    ]

    for printer_test in printer_tests:
        printer_test.method(**printer_test.kwargs)
        assert Printer.console.last_print_call.objects == printer_test.expected_output
        assert Printer.console.last_print_call.style == printer_test.expected_style
        assert Printer.console.last_print_call.end == printer_test.expected_end
