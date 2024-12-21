from scriptlib.battery import BatteryInfo
from scriptlib.color import ConsoleColor
import psutil

battery: BatteryInfo = BatteryInfo.get_data()

if battery.plugged_in:
    info_str: str = ConsoleColor.color("Battery on charge", ConsoleColor.YELLOW)
    print(f"{info_str}.")
else:
    prct_str: str = ConsoleColor.color(f"{battery.percentage:.0f}%", ConsoleColor.YELLOW)
    time_str: str = ConsoleColor.color(f"{battery.time_left} hours", ConsoleColor.YELLOW)

    print(f"Battery {prct_str}, {time_str} of usage left.")
