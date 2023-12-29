from enum import Enum


class IP2LocManagerUserAnswers(Enum):
    UPDATE = "U"
    MANUAL_UPDATE = "M"
    SKIP = "S"
    DISABLE = "D"
    EXIT = "E"
