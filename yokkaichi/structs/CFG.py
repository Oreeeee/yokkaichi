from dataclasses import dataclass, field


@dataclass
class CFG:
    platforms: list = field(default_factory=list)  # Possible values: "java", "bedrock"
    query_java: bool = field(default_factory=bool)
    masscan_scan: bool = field(default_factory=bool)
    ip_list_scan: bool = field(default_factory=bool)
    masscan_ip_source: str = field(
        default_factory=str
    )  # Possible values: "countries", "list"
    masscan_args: str = field(default_factory=str)
    masscan_output: bool = field(default_factory=bool)
    masscan_output_location: str = field(default_factory=str)
    masscan_country_list: list = field(default_factory=list)
    masscan_ip_list: str = field(default_factory=str)
    ip_list: str = field(default_factory=str)
    ports: list = field(default_factory=list)
    threads: int = field(default_factory=int)
    output: str = field(default_factory=str)
    use_ip2location: bool = field(default_factory=bool)
    ip2location_db: str = field(default_factory=str)
    ip2location_cache: bool = field(default_factory=bool)
