import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import yokkaichi.config_loader
from yokkaichi.enums import Platforms
from yokkaichi.structs import CFG

DEFAULT_CFG = """
version = "4"

[platforms]
java = true
bedrock = false

[platforms.additional]
java_query = false

[scanner]
type = "ping_scan"
countries = ["US", "DE"]
ip_list = ""
ports = "25564-25566,25569"
threads = 100
timeout = 3.0
offline_printing = "disabled"
output = "out.json"

[masscan]
args = "--rate 5000"

[ip2location]
enabled = false
databases_location = "ip2location_dbs/"
bin_filename = "IP2LOCATION-LITE-DB11.BIN"
csv_filename = "IP2LOCATION-LITE-DB1.CSV"
bin_code = "DB11LITEBIN"
csv_code = "DB1LITECSV"
check_for_updates = true
cache = true
"""


def test_parse_cfg(monkeypatch):
    def default_cfg(x):
        return tomllib.loads(DEFAULT_CFG)

    monkeypatch.setattr(yokkaichi.config_loader, "load_cfg", default_cfg)

    assert yokkaichi.config_loader.parse_cfg("") == CFG(
        platforms=[Platforms.JAVA],
        query_java=False,
        scan_type="ping_scan",
        countries=["US", "DE"],
        ip_list="",
        ports=[25564, 25565, 25566, 25569],
        threads=100,
        timeout=3.0,
        offline_printing="disabled",
        output="out.json",
        masscan_args="--rate 5000",
        use_ip2location=False,
        ip2location_dbs="ip2location_dbs/",
        ip2location_db_bin="IP2LOCATION-LITE-DB11.BIN",
        ip2location_db_csv="IP2LOCATION-LITE-DB1.CSV",
        ip2location_bin_code="DB11LITEBIN",
        ip2location_csv_code="DB1LITECSV",
        ip2location_check_for_updates=True,
        ip2location_cache=True,
    )


def test_parse_cfg_config_version_check(monkeypatch):
    def mockexit(x):
        pass

    def fake_cfg(x):
        cfg = DEFAULT_CFG
        cfg = cfg.replace('version = "4"', 'version = "0"')
        return tomllib.loads(cfg)

    monkeypatch.setattr("builtins.exit", mockexit)
    monkeypatch.setattr(yokkaichi.config_loader, "load_cfg", fake_cfg)
    assert yokkaichi.config_loader.parse_cfg("") == True
