from rich.console import Console

from yokkaichi import __version__


class Printer:
    console: Console = Console(highlight=False)

    @classmethod
    def version(cls, **kwargs) -> None:
        cls.console.print(
            "yokkaichi [bold cyan]{version}[/bold cyan] on [bold cyan]{py_implementation} {py_version}[/bold cyan]".format(
                **kwargs
            ),
            style="green",
        )

    @classmethod
    def ip_list_not_found(cls) -> None:
        cls.console.print("ERROR! IP LIST/MASSCAN LIST NOT FOUND!", style="red")

    @classmethod
    def toml_parse_failed(cls) -> None:
        cls.console.print(
            "Config file is invalid! (Failed parsing TOML)", style="bold red"
        )

    @classmethod
    def cfg_doesnt_exist(cls, **kwargs) -> None:
        cls.console.print(
            "[bold white]{cfg_name}[/bold white] doesn't exist. Create a sample config in this location? (y/n) ".format(
                **kwargs
            ),
            style="yellow",
            end="",
        )

    @classmethod
    def created_cfg(cls, **kwargs) -> None:
        cls.console.print(
            "Created a new config file at [bold white]{cfg_name}[/bold white]. Adjust it to your preferences".format(
                **kwargs
            ),
            style="green",
        )

    @classmethod
    def output_exists(cls) -> None:
        cls.console.print(
            "Output file exists. Continuing will overwrite this file. Proceed? (y/n) ",
            style="yellow",
            end="",
        )

    @classmethod
    def loading_ips(cls) -> None:
        cls.console.print("Loading IPs", style="cyan")

    @classmethod
    def loaded_ips(cls, **kwargs) -> None:
        cls.console.print("Loaded {ip_count} IPs".format(**kwargs), style="green")

    @classmethod
    def scan_complete(cls, **kwargs) -> None:
        cls.console.print(
            "[bold white]{server_count}[/bold white] servers found.\nStarted: [bold white]{scan_start_time}[/bold white].\nEnded: [bold white]{scan_end_time}[/bold white].\nTook [bold white]{scan_time}[/bold white].".format(
                **kwargs
            ),
            style="magenta",
        )

    @classmethod
    def loading_db(cls) -> None:
        cls.console.print("Loading IP2Location database", style="cyan")

    @classmethod
    def db_corrupted(cls) -> None:
        cls.console.print("IP2Location database is broken or corrupted!", style="red")

    @classmethod
    def set_token(cls) -> None:
        cls.console.print(
            "To automatically download IP2Location database, a IP2Location LITE token must be provided! Either set the IP2LOCATION_LITE_TOKEN environment variable, or use manual update.",
            style="red",
        )

    @classmethod
    def unknown_answer(cls) -> None:
        cls.console.print("Unknown answer", style="red")

    @classmethod
    def server_offline(cls, **kwargs) -> None:
        cls.console.print(
            "[-] {ip}:{port} for {platform} is offline!".format(**kwargs),
            style="red",
        )

    @classmethod
    def query_failed(cls, **kwargs) -> None:
        cls.console.print(
            "[!] Query failed for {ip}:{port}".format(**kwargs), style="yellow"
        )

    @classmethod
    def server_found(cls, **kwargs) -> None:
        cls.console.print(
            "[+] {platform} server found at {ip}:{port}!".format(**kwargs),
            style="green",
        )

    @classmethod
    def couldn_parse_port(cls, **kwargs) -> None:
        cls.console.print(
            "Couldn't parse: [bold white]{port}[/bold white]".format(**kwargs),
            style="red",
        )

    @classmethod
    def wrong_cfg_ver(cls, **kwargs) -> None:
        cls.console.print(
            "Wrong config version detected! Please update your config. Your config: {cfg_file_ver}. Expected: {cfg_ver}".format(
                **kwargs
            ),
            style="bold red",
        )

    @classmethod
    def loading_threads(cls, **kwargs) -> None:
        cls.console.print(
            "Loading [bold white]{thread_count}[/bold white] threads!".format(**kwargs),
            style="cyan",
        )

    @classmethod
    def no_input_list_specified(cls) -> None:
        cls.console.print(
            "No input list specified! Choose either scanning by countries or from IP list. Quitting...",
            style="red",
        )
