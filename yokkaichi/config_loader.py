from .constants.rich_console import console
from .port_parser import parse_port_range
from .structs.CFG import CFG
import pkgutil

try:
    import tomllib
except ModuleNotFoundError:
    # Use tomli instead (Python versions before 3.11)
    import tomli as tomllib

CONFIG_VERSION = "1"
SAMPLE_CFG = pkgutil.get_data(__name__, "assets/example_config.toml").decode("utf-8")

def parse_cfg(cfg_location):
    # Read the config file
    with open(cfg_location, "rb") as f:
        cfg_file = tomllib.load(f)

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
