from lib.battery import BatteryInfo
from lib.console import ConsoleColor, Console, Alignment
from lib.tasks import Task
import sys
import os

def main(argc, argv):
    if argc == 2 and argv[0] == "tasks" and argv[1] == "insert":
        title: str = input("Enter title of the task: ")
        details: list[str] = []

        while (line := input("Enter next line of details (leave blank to exit): ")) != "":
           details.append(line)
        
        task: Task = Task(title, details)
        task.insert()
        
        Console.clear()
        main(0, [])
        
        exit()

    elif argc == 2 and argv[0] == "tasks" and argv[1] == "done":
        Task.mark_current_done()
        Console.clear()

        main(0, [])
        exit()

    battery: BatteryInfo = BatteryInfo.get_data()

    if battery.plugged_in:
        info_str: str = ConsoleColor.color("Battery on charge", ConsoleColor.YELLOW)
        Console.print_aligned(info_str, Alignment.Center)
    else:
        prct_str: str = ConsoleColor.color(f"{battery.percentage:.0f}%", ConsoleColor.YELLOW)
        time_str: str = ConsoleColor.color(f"{battery.time_left} hours", ConsoleColor.YELLOW)

        Console.print_aligned(f"Battery {prct_str}, {time_str} of usage left", Alignment.Center)

    print()

    Console.print_aligned(
        ConsoleColor.color(
            "Current task:",
            ConsoleColor.BOLD
        ),
        Alignment.Center
    )
    current_task: Task = Task.get_current()
    Console.print_aligned(
        current_task.title,
        Alignment.Center
    )
    for line in current_task.details:
        Console.print_aligned(
            line,
            Alignment.Center
        )

sys.argv.pop(0)
argv: list[str] = sys.argv
argc: int = len(sys.argv)

main(argc, argv)
