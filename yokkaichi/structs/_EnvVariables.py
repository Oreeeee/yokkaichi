from dataclasses import dataclass, field


@dataclass
class EnvVariables:
    ip2location_lite_token: str = field(default_factory=str)
