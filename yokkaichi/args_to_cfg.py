from .constants.rich_console import console
from .port_parser import parse_port_range
from .structs.CFG import CFG


def args_to_cfg(args):
    cfg = CFG()

    if args.java:
        cfg.platforms.append("java")
    if args.bedrock:
        cfg.platforms.append("bedrock")

    cfg.query_java = args.query
    cfg.masscan_scan = args.masscan
    cfg.ip_list_scan = args.ip_list_scan

    if args.masscan_method not in ("countries", "list"):
        console.print(
            "Proper values for --masscan-method are: countries, list", style="bold red"
        )
        exit(1)

    cfg.masscan_ip_source = args.masscan_method
    cfg.masscan_args = args.masscan_args

    if args.masscan_json_output == "":
        cfg.masscan_output = False

    cfg.masscan_output_location = args.masscan_json_output
    cfg.masscan_ip_list = args.masscan_ip_list
    cfg.ip_list = args.ip_list
    cfg.ports = parse_port_range(args.ports)
    cfg.threads = args.thread_count
    cfg.output = args.output_file

    if args.ip2location_db != "":
        cfg.use_ip2location = True
        cfg.ip2location_db = args.ip2location_db
    else:
        cfg.use_ip2location = False
        cfg.ip2location_db = ""

    cfg.ip2location_cache = args.ip2location_cache

    return cfg
