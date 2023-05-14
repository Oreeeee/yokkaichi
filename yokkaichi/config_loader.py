from .constants.rich_console import console
from .port_parser import parse_port_range
from .structs.CFG import CFG
import tomli

CONFIG_VERSION = "1"
# TODO: Bring this back to a separate file
SAMPLE_CFG = """
# This is an example configuration file for Yokkaichi.
# Configure this for your preferences.
# Pass the location to this config file with -c as an argument.
# Example: python -m yokkaichi -c sample.toml
# You can pass this without the file location and it will look for yokkaichi.toml in your current location.

version = "1" # Changed for every change breaking config compatibility

[platforms]
java = true
bedrock = false

[platforms.additional]
java_query = false # Use the Query protocol (more info, but a little bit broken and slow right now)

[type]
masscan = true # Recommended, fast
ip_list = false # Not recommended, slow, outdated

[type.options_masscan]
ip_source = "countries" # Availible types: "countries", "list"
args = "" # Additional arguments for masscan
output = false
output_location = "masscan_out.json" # Where to output masscan's results (not required)

[type.options_masscan.countries]
countries = ["US", "DE"] # Standard TOML array, use ISO 3166-1 alpha-2 codes (the 2 letter ones)

[type.options_masscan.list]
list = "masscan_ips.txt" # Location to the list of IPs to scan with masscan, separated by newlines

[type.options_ip_list]
list = "ips.txt" # Location to the list of IPs to scan, separated by newlines

[scanner]
ports = "25564-25566,25569" # Port list (not TOML's format! Splits ports by commas, sets ranges with hyphens)
threads = 100 # Leave this at default unless you have a lot of servers
output = "out.json" # IMPORTANT! That's where the servers go!

[ip2location]
enabled = false # Enable getting the location of the server
db = "IP2LOCATION-LITE-DB11.BIN" # IP2Location .BIN database (get from lite.ip2location.com)
cache = true # Enable for faster speed at the cost of RAM (doesn't really matter with Lite database)
""".strip()


def parse_cfg(cfg_location):
    # Read the config file
    with open(cfg_location, "rb") as f:
        cfg_file = tomli.load(f)

    cfg = CFG()

    # TODO: Check if the file is a valid Yokkaichi config!
    cfg_file_ver = cfg_file["version"]
    if cfg_file_ver != CONFIG_VERSION:
        console.print(
            f"Wrong config version detected! Please update your config. Your config: {cfg_file_ver}. Expected: {CONFIG_VERSION}",
            style="bold red",
        )
        exit(1)

    if cfg_file["platforms"]["java"]:
        cfg.platforms.append("java")
    if cfg_file["platforms"]["bedrock"]:
        cfg.platforms.append("bedrock")

    cfg.query_java = cfg_file["platforms"]["additional"]["java_query"]

    cfg.masscan_scan = cfg_file["type"]["masscan"]
    cfg.ip_list_scan = cfg_file["type"]["ip_list"]

    cfg.masscan_ip_source = cfg_file["type"]["options_masscan"]["ip_source"]
    cfg.masscan_args = cfg_file["type"]["options_masscan"]["args"]
    cfg.masscan_output = cfg_file["type"]["options_masscan"]["output"]
    cfg.masscan_output_location = cfg_file["type"]["options_masscan"]["output_location"]

    cfg.masscan_country_list = cfg_file["type"]["options_masscan"]["countries"][
        "countries"
    ]

    cfg.masscan_ip_list = cfg_file["type"]["options_masscan"]["list"]["list"]

    cfg.ports = parse_port_range(cfg_file["scanner"]["ports"])
    cfg.threads = cfg_file["scanner"]["threads"]
    cfg.output = cfg_file["scanner"]["output"]

    cfg.use_ip2location = cfg_file["ip2location"]["enabled"]
    cfg.ip2location_db = cfg_file["ip2location"]["db"]
    cfg.ip2location_cache = cfg_file["ip2location"]["cache"]

    print(cfg)

    return cfg


def write_cfg(cfg_location):
    # Write the sample config
    with open(cfg_location, "w") as f:
        f.write(SAMPLE_CFG)
