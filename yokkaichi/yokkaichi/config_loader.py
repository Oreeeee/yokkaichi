import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from .enums import Platforms
from .port_parser import parse_port_range
from .Printer import Printer
from .structs import CFG

CONFIG_VERSION = "4"
# TODO: Bring this back to a separate file
SAMPLE_CFG = """
# This is an example configuration file for Yokkaichi.
# Configure this for your preferences.
# Pass the location to this config file with -c as an argument.
# Example: python -m yokkaichi -c sample.toml
# You can pass this without the file location and it will look for yokkaichi.toml in your current location.
# Do not comment any of the config's options, it will currently cause a crash

version = "4" # Changed for every change breaking config compatibility

[platforms]
java = true
bedrock = false

[platforms.additional]
java_query = false # Use the Query protocol (more info, but a little bit broken and slow right now)

[scanner]
type = "ping_scan" # "masscan" type is faster, but less accurate and requires root/admin, and "ping_scan" is slower but more accurate and doesn't require escalated priviledges
countries = ["US", "DE"] # Countries to scan, standard TOML array, use ISO 3166-1 alpha-2 codes (the 2 letter ones), empty to disable
ip_list = "" # Location to the list of IP:Port combinations / CIDR blocks / IP addresses to scan, separated by newlines, empty to disable
ports = "25564-25566,25569" # Port list (not TOML's format! Similarly to nmap and masscan splits ports by commas and sets ranges with hyphens)
threads = 100 # Setting this to a higher value will make the scanning faster, but too much can crash the system or the network
timeout = 3.0 # Timeout in seconds before assuming the server is offline
offline_printing = "disabled" # Should the script output offline servers. "disabled" will print nothing, "offline" will print offline servers and "full_traceback" will print entire traceback
output = "out.json" # IMPORTANT! That's where the servers go!

[masscan]
args = "" # Additional arguments for masscan

[ip2location]
enabled = false # Enable getting the location of the server
databases_location = "ip2location_dbs/" # Where are the databases stored
bin_filename = "IP2LOCATION-LITE-DB11.BIN"
csv_filename = "IP2LOCATION-LITE-DB1.CSV"
bin_code = "DB11LITEBIN" # Avoid changing this
csv_code = "DB1LITECSV" # Avoid changing this
check_for_updates = true # Will Yokkaichi check for updates to the database every month. Highly recommended to leave it on!
cache = true # Enable for faster speed at the cost of RAM
""".strip()


def load_cfg(cfg_location):
    with open(cfg_location, "rb") as f:
        cfg_file = tomllib.load(f)
    return cfg_file


def parse_cfg(cfg_location):
    # Read the config file
    cfg_file = load_cfg(cfg_location)

    cfg = CFG()

    # TODO: Check if the file is a valid Yokkaichi config!
    cfg_file_ver = cfg_file["version"]
    if cfg_file_ver != CONFIG_VERSION:
        Printer.wrong_cfg_ver(cfg_file_ver=cfg_file_ver, cfg_ver=CONFIG_VERSION)
        exit(1)
        return True

    # [platforms]
    if cfg_file["platforms"]["java"]:
        cfg.platforms.append(Platforms.JAVA)
    if cfg_file["platforms"]["bedrock"]:
        cfg.platforms.append(Platforms.BEDROCK)

    # [platforms.additional]
    cfg.query_java = cfg_file["platforms"]["additional"]["java_query"]

    # [scanner]
    cfg.scan_type = cfg_file["scanner"]["type"]
    cfg.countries = cfg_file["scanner"]["countries"]
    cfg.ip_list = cfg_file["scanner"]["ip_list"]
    cfg.ports = parse_port_range(cfg_file["scanner"]["ports"])
    cfg.threads = cfg_file["scanner"]["threads"]
    cfg.timeout = cfg_file["scanner"]["timeout"]
    cfg.offline_printing = cfg_file["scanner"]["offline_printing"]
    cfg.output = cfg_file["scanner"]["output"]

    # [masscan]
    cfg.masscan_args = cfg_file["masscan"]["args"]

    # [ip2location]
    cfg.use_ip2location = cfg_file["ip2location"]["enabled"]
    cfg.ip2location_dbs = cfg_file["ip2location"]["databases_location"]
    cfg.ip2location_db_bin = cfg_file["ip2location"]["bin_filename"]
    cfg.ip2location_db_csv = cfg_file["ip2location"]["csv_filename"]
    cfg.ip2location_bin_code = cfg_file["ip2location"]["bin_code"]
    cfg.ip2location_csv_code = cfg_file["ip2location"]["csv_code"]
    cfg.ip2location_check_for_updates = cfg_file["ip2location"]["check_for_updates"]
    cfg.ip2location_cache = cfg_file["ip2location"]["cache"]

    return cfg


def write_cfg(cfg_location):
    # Write the sample config
    with open(cfg_location, "w") as f:
        f.write(SAMPLE_CFG)
