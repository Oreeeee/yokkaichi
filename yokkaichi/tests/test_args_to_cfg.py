from dataclasses import dataclass

import yokkaichi.args_to_cfg
from yokkaichi.enums import MasscanMethods, Platforms
from yokkaichi.structs import CFG


@dataclass
class FakeArgs:
    java: bool
    bedrock: bool
    query: bool
    masscan: bool
    ip_list_scan: bool
    masscan_method: str
    masscan_args: str
    masscan_json_output: str
    masscan_ip_list: str
    masscan_countries: list
    ip_list: str
    ports: str
    thread_count: int
    output_file: str
    ip2location_db: str
    ip2location_cache: bool


example_args = FakeArgs(
    java=True,
    bedrock=False,
    query=False,
    masscan=True,
    ip_list_scan=False,
    masscan_method="countries",
    masscan_args="",
    masscan_json_output="masscan_out.json",
    masscan_ip_list="masscan_ips.txt",
    masscan_countries=["US", "DE"],
    ip_list="ips.txt",
    ports="25564-25566,25569",
    thread_count=100,
    output_file="out.json",
    ip2location_db="IP2LOCATION-LITE-DB11.BIN",
    ip2location_cache=True,
)


def test_args_to_cfg():
    assert yokkaichi.args_to_cfg.args_to_cfg(example_args) == CFG(
        platforms=[Platforms.JAVA],
        query_java=False,
        masscan_scan=True,
        ip_list_scan=False,
        masscan_ip_source=MasscanMethods.COUNTRIES,
        masscan_args="",
        masscan_output=False,
        masscan_output_location="masscan_out.json",
        masscan_country_list=["US", "DE"],
        masscan_ip_list="masscan_ips.txt",
        ip_list="ips.txt",
        ports=[25564, 25565, 25566, 25569],
        threads=100,
        output="out.json",
        use_ip2location=True,
        ip2location_db="IP2LOCATION-LITE-DB11.BIN",
        ip2location_cache=True,
    )


def test_args_to_cfg_improper_method(monkeypatch):
    def mockexit(x):
        pass

    monkeypatch.setattr("builtins.exit", mockexit)
    args = example_args
    args.masscan_method = "notarealvalue"
    assert yokkaichi.args_to_cfg.args_to_cfg(args) == True


def test_args_to_cfg_proper_method():
    args = example_args
    for method in MasscanMethods:
        args.masscan_method = method.value
        assert type(yokkaichi.args_to_cfg.args_to_cfg(args)) == CFG