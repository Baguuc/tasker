from lib.console import ConsoleColor, Console, Alignment
from lib.tasks import Task
import sys
import os


def insert(argc, argv):
    title: str = input("Enter title of the task: ")
    details: list[str] = []

    while (line := input("Enter next line of details (leave blank to exit): ")) != "":
        details.append(line)
        
    Task.insert(title, details)


def done(argc, argv):
    Task.mark_current_done()


def update(argc, argv):
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


def main(argc, argv):
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


def run(argc, argv):
    commands_map: dict[tuple, callable] = {
        ("tasks", "insert"): insert,
        ("tasks", "done"): done,
        ("tasks", "update"): update
    }
    command: callable = commands_map.get(tuple(argv), main)
    command(argc, argv)

if __name__ == "__main__":
    sys.argv.pop(0)
    argv: list[str] = sys.argv
    argc: int = len(sys.argv)

    run(argc, argv)

