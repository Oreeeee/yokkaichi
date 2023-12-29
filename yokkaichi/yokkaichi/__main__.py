# Import modules
import argparse
import pathlib
import platform
import sys
import time
from datetime import datetime

from .Printer import Printer

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from yokkaichi import __version__

from . import config_loader, env_loader
from .IP2L_Manager import IP2L_Manager
from .port_parser import parse_port_range
from .ServerScan import ServerScan
from .structs import EnvVariables


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="Configuration file (example one will be created if it doesn't exist)",
        default=None,
        const="yokkaichi.toml",
        nargs="?",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="show_version",
        help="Show version and quit",
        action="store_true",
    )
    parser.set_defaults(config_file="yokkaichi.toml")
    args = parser.parse_args()

    if args.show_version:
        Printer.version(
            version=__version__,
            py_implementation=platform.python_implementation(),
            py_version=platform.python_version(),
        )
        exit()

    # Load the config file
    if args.config_file != None:
        try:
            cfg = config_loader.parse_cfg(args.config_file)
        except tomllib.TOMLDecodeError:
            Printer.toml_parse_failed()
        except FileNotFoundError:
            Printer.cfg_doesnt_exist(cfg_name=args.config_file)
            if input().lower() == "y":
                config_loader.write_cfg(args.config_file)
                Printer.created_cfg(cfg_name=args.config_file)
                exit(0)

    # Load environment variables
    env_variables: EnvVariables = env_loader.load_env()

    # Check does output file exists
    if pathlib.Path(cfg.output).is_file():
        Printer.output_exists()
        if input().lower() == "n":
            exit(0)
    else:
        # Touch the file
        pathlib.Path(cfg.output).touch()

    if cfg.use_ip2location:
        # Initialize IP2Location
        ip2location: IP2L_Manager = IP2L_Manager(cfg, env_variables)
    else:
        ip2location: None = None

    if cfg.use_ip2location and cfg.countries != []:
        ip_list: str = ip2location.get_country_cidr_file()
    elif cfg.ip_list != "":
        ip_list: str = cfg.ip_list
    else:
        Printer.no_input_list_specified()
        exit(1)

    scan_start = time.time()

    scanner = ServerScan(
        cfg=cfg,
        ip_list=ip_list,
        ip2location=ip2location,
    )
    scanner.start_scan()

    scan_end = time.time()

    # Show results
    scan_start_time = datetime.fromtimestamp(scan_start).isoformat()
    scan_end_time = datetime.fromtimestamp(scan_end).isoformat()
    scan_time = time.strftime("%H:%M:%S", time.gmtime(scan_end - scan_start))
    Printer.scan_complete(
        server_count=len(scanner.results_obj.results),
        scan_start_time=scan_start_time,
        scan_end_time=scan_end_time,
        scan_time=scan_time,
    )


if __name__ == "__main__":
    main()
