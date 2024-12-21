from scriptlib.battery import BatteryInfo
from scriptlib.console import ConsoleColor
from scriptlib.tasks import Task
import sys

sys.argv.pop(0)
argv: list[str] = sys.argv
argc: int = len(sys.argv)

if argc >= 4 and argv[0] == "tasks" and argv[1] == "insert":
    task: Task = Task(argv[2], argv[3:])
    task.insert()

    exit()

battery: BatteryInfo = BatteryInfo.get_data()

if battery.plugged_in:
    info_str: str = ConsoleColor.color("Battery on charge", ConsoleColor.YELLOW)
    print(f"{info_str}.")
else:
    prct_str: str = ConsoleColor.color(f"{battery.percentage:.0f}%", ConsoleColor.YELLOW)
    time_str: str = ConsoleColor.color(f"{battery.time_left} hours", ConsoleColor.YELLOW)

    print(f"Battery {prct_str}, {time_str} of usage left.")
