from dataclasses import dataclass, field


@dataclass
class CFG:
    # [platforms]
    platforms: list = field(default_factory=list)

    # [platforms.additional]
    query_java: bool = field(default_factory=bool)

    # [scanner]
    scan_type: str = field(default_factory=str)
    countries: list = field(default_factory=list)
    ip_list: str = field(default_factory=str)
    ports: list = field(default_factory=list)
    threads: int = field(default_factory=int)
    timeout: float = field(default_factory=float)
    offline_printing: str = field(default_factory=str)
    output: str = field(default_factory=str)

    # [masscan]
    masscan_args: str = field(default_factory=str)

    # [ip2location]
    use_ip2location: bool = field(default_factory=bool)
    ip2location_dbs: str = field(default_factory=str)
    ip2location_db_bin: str = field(default_factory=str)
    ip2location_db_csv: str = field(default_factory=str)
    ip2location_bin_code: str = field(default_factory=str)
    ip2location_csv_code: str = field(default_factory=str)
    ip2location_check_for_updates: bool = field(default_factory=bool)
    ip2location_cache: bool = field(default_factory=bool)
