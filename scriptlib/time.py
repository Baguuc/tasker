from typing import Self
from dataclasses import dataclass

SECS_IN_MINUTE: int = 60
SECS_IN_HOUR: int = 3600

@dataclass
class Time:
    seconds: int
    minutes: int
    hours: int

    def from_seconds(seconds: int) -> Self:
        hours: int = seconds // SECS_IN_HOUR
        seconds -= hours * SECS_IN_HOUR

        minutes: int = seconds // SECS_IN_MINUTE
        seconds -= minutes * SECS_IN_MINUTE

        return Time(seconds, minutes, hours)


