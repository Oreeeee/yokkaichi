import dataclasses
import json
from threading import Lock

from .structs import CFG, MinecraftServer


class Results:
    results: list = []

    def __init__(self, cfg: CFG) -> None:
        self.file_lock: Lock = Lock()
        self.cfg: CFG = cfg

    def add_to_file(self, server_info: MinecraftServer) -> None:
        """
        This method saves results to a file with a lock, and additionally adds
        the server to self.results
        """
        self.results.append(dataclasses.asdict(server_info))
        with self.file_lock:
            with open(self.cfg.output, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=4, ensure_ascii=False)
