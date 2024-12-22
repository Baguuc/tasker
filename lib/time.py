from typing import Self
from dataclasses import dataclass

SECS_IN_MIN: int = 60
MINS_IN_HOUR: int = 60

@dataclass
class Time:
    seconds: int
    minutes: int
    hours: int

    def from_seconds(seconds: int) -> Self:
        minutes, seconds = divmod(seconds, SECS_IN_MIN)
        hours, minutes = divmod(minutes, MINS_IN_HOUR)

        return Time(seconds=seconds, minutes=minutes, hours=hours)
    
    def from_minutes(minutes: int) -> Self:
        seconds: int = minutes * SECS_IN_HOUR

        return Self.from_seconds(seconds)
    
    def from_hours(hours: int) -> Self:
        seconds: int = hours * SECS_IN_HOUR
        return Self.from_seconds(seconds)
    
    def __str__(self) -> str:
        return f"{self.hours}:{self.minutes}:{self.seconds}"

