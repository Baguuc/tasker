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
        
        Task.insert(title, details)

        Console.clear()
        main(0, [])
        
        exit()

    elif argc == 2 and argv[0] == "tasks" and argv[1] == "done":
        Task.mark_current_done()
        Console.clear()

        main(0, [])
        exit()
    
    elif argc == 3 and argv[0] == "tasks" and argv[1] == "update":
        try:
            _id: int = int(argv[2])
        except:
            print("The id has to be numeric")
            exit()
        
        current_data: Task = Task.select_one(_id)
        print(ConsoleColor.color(current_data.title, ConsoleColor.YELLOW))
        title: str = input("Enter new title of the task: ")
        details: list[str] = []
        
        linei: int = 0
        try:
            print(ConsoleColor.color(current_data.details[linei], ConsoleColor.YELLOW))
        except:
            pass

        line = input("Enter next line of new details (leave blank to exit): ")
        
        while line != "":
            linei += 1
            details.append(line)

        
            try:
                print(ConsoleColor.color(current_data.details[linei], ConsoleColor.YELLOW))
            except:
                pass

            line = input("Enter next line of new details (leave blank to exit): ")
        Task.update(_id, title, details)
        Console.clear()
        main(0, [])
        exit()

    battery: BatteryInfo = BatteryInfo.get_data()

    if battery.plugged_in:
        info_str: str = ConsoleColor.color("Battery on charge", ConsoleColor.YELLOW)
        Console.print_aligned(info_str, Alignment.Center)
    else:
        prct_str: str = ConsoleColor.color(f"{battery.percentage:.0f}%", ConsoleColor.YELLOW)
        time_str: str = ConsoleColor.color(f"~{battery.time_left} hours", ConsoleColor.YELLOW)

        Console.print_aligned(f"Battery {prct_str}, {time_str} of usage left", Alignment.Center)

    print()

    current_task: Task = Task.get_current()
    Console.print_aligned(
        ConsoleColor.color(
            current_task.title,
            [ConsoleColor.BOLD, ConsoleColor.YELLOW]
        ),
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
