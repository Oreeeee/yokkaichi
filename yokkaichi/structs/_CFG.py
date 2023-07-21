from dataclasses import dataclass, field


@dataclass
class CFG:
    platforms: list = field(default_factory=list)
    query_java: bool = field(default_factory=bool)
    masscan_scan: bool = field(default_factory=bool)
    ip_list_scan: bool = field(default_factory=bool)
    masscan_args: str = field(default_factory=str)
    masscan_country_list: list = field(default_factory=list)
    masscan_country_scan: bool = field(default_factory=bool)
    masscan_ip_list: str = field(default_factory=str)
    masscan_ip_scan: bool = field(default_factory=bool)
    ip_list: str = field(default_factory=str)
    ports: list = field(default_factory=list)
    threads: int = field(default_factory=int)
    timeout: float = field(default_factory=float)
    offline_printing: str = field(default_factory=str)
    output: str = field(default_factory=str)
    use_ip2location: bool = field(default_factory=bool)
    ip2location_dbs: str = field(default_factory=str)
    ip2location_db_bin: str = field(default_factory=str)
    ip2location_db_csv: str = field(default_factory=str)
    ip2location_bin_code: str = field(default_factory=str)
    ip2location_csv_code: str = field(default_factory=str)
    ip2location_cache: bool = field(default_factory=bool)
