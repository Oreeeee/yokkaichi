from yokkaichi.structs.CFG import CFG
import yokkaichi.config_loader
import tomli

DEFAULT_CFG = """
version = "1"

[platforms]
java = true
bedrock = false

[platforms.additional]
java_query = false

[type]
masscan = true
ip_list = false

[type.options_masscan]
ip_source = "countries"
args = ""
output = false
output_location = "masscan_out.json"

[type.options_masscan.countries]
countries = ["US", "DE"]

[type.options_masscan.list]
list = "masscan_ips.txt"

[type.options_ip_list]
list = "ips.txt"

[scanner]
ports = "25564-25566,25569"
threads = 100
output = "out.json"

[ip2location]
enabled = false
db = "IP2LOCATION-LITE-DB11.BIN"
cache = true
"""


def test_parse_cfg(monkeypatch):
    def default_cfg(x):
        return tomli.loads(DEFAULT_CFG)

    monkeypatch.setattr(yokkaichi.config_loader, "load_cfg", default_cfg)

    assert yokkaichi.config_loader.parse_cfg("") == CFG(
        platforms=["Java"],
        query_java=False,
        masscan_scan=True,
        ip_list_scan=False,
        masscan_ip_source="countries",
        masscan_args="",
        masscan_output=False,
        masscan_output_location="masscan_out.json",
        masscan_country_list=["US", "DE"],
        masscan_ip_list="masscan_ips.txt",
        ip_list="ips.txt",
        ports=[25564, 25565, 25566, 25569],
        threads=100,
        output="out.json",
        use_ip2location=False,
        ip2location_db="IP2LOCATION-LITE-DB11.BIN",
        ip2location_cache=True,
    )
