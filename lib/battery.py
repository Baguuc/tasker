import psutil
from typing import Self
from dataclasses import dataclass
from lib.time import Time


@dataclass
class BatteryInfo:
    percentage: float
    plugged_in: bool
    time_left: Time

    def get_data() -> Self:
        data = psutil.sensors_battery()
        time_left: Time = Time.from_seconds(data.secsleft)

        return BatteryInfo(data.percent, data.power_plugged, time_left)


