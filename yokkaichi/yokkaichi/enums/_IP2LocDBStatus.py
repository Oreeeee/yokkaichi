from enum import Enum, auto


class IP2LocDBStatus(Enum):
    UP_TO_DATE = auto()
    EXISTS = auto()
    OUTDATED = auto()
    DOESNT_EXIST = auto()
    INCORRECT_DATE = auto()
