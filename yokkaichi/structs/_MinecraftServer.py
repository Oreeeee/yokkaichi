from dataclasses import dataclass


@dataclass
class MinecraftServer:
    ip: str
    port: int
    location_info: dict
    ping: int
    platform: str
    motd: str
    version: str
    online_players: int
    max_players: int
    player_list: list
    time_discovered: str
