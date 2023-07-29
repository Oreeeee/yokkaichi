import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import yokkaichi.config_loader
from yokkaichi.enums import Platforms
from yokkaichi.structs import CFG

DEFAULT_CFG = """
version = "2"

[platforms]
java = true
bedrock = false

[platforms.additional]
java_query = false

[type]
masscan = true
ip_list = false

[type.options_masscan]
args = "--rate 5000"

[type.options_masscan.countries]
enabled = true
countries = ["US", "DE"]

[type.options_masscan.list]
enabled = true
list = "masscan_ips.txt"

[type.options_ip_list]
list = "ips.txt"

[scanner]
ports = "25564-25566,25569"
threads = 100
timeout = 3.0
offline_printing = "disabled"
output = "out.json"

[ip2location]
enabled = false
databases_location = "ip2location_dbs/"
bin_filename = "IP2LOCATION-LITE-DB11.BIN"
csv_filename = "IP2LOCATION-LITE-DB1.CSV"
bin_code = "DB11LITEBIN"
csv_code = "DB1LITECSV"
cache = true
"""


def test_parse_cfg(monkeypatch):
    def default_cfg(x):
        return tomllib.loads(DEFAULT_CFG)

    monkeypatch.setattr(yokkaichi.config_loader, "load_cfg", default_cfg)

    assert yokkaichi.config_loader.parse_cfg("") == CFG(
        platforms=[Platforms.JAVA],
        query_java=False,
        masscan_scan=True,
        ip_list_scan=False,
        masscan_args="--rate 5000",
        masscan_country_scan=True,
        masscan_country_list=["US", "DE"],
        masscan_ip_scan=True,
        masscan_ip_list="masscan_ips.txt",
        ip_list="ips.txt",
        ports=[25564, 25565, 25566, 25569],
        threads=100,
        timeout=3.0,
        offline_printing="disabled",
        output="out.json",
        use_ip2location=False,
        ip2location_dbs="ip2location_dbs/",
        ip2location_db_bin="IP2LOCATION-LITE-DB11.BIN",
        ip2location_db_csv="IP2LOCATION-LITE-DB1.CSV",
        ip2location_bin_code="DB11LITEBIN",
        ip2location_csv_code="DB1LITECSV",
        ip2location_cache=True,
    )


def test_parse_cfg_config_version_check(monkeypatch):
    def mockexit(x):
        pass

    def fake_cfg(x):
        cfg = DEFAULT_CFG
        cfg = cfg.replace('version = "2"', 'version = "0"')
        return tomllib.loads(cfg)

    monkeypatch.setattr("builtins.exit", mockexit)
    monkeypatch.setattr(yokkaichi.config_loader, "load_cfg", fake_cfg)
    assert yokkaichi.config_loader.parse_cfg("") == True
