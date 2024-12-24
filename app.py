from lib.console import ConsoleColor, Console, Alignment
from lib.database import get_database_connection
from lib.migrations import migrate
from lib.tasks import Task
import sys
import os

def insert():
    title: str = input("Enter title of the task: ")
    details: list[str] = []

    while (line := input("Enter next line of details (leave blank to exit): ")) != "":
        details.append(line)
        
    Task.insert(title, details)


def done():
    Task.mark_current_done()


def update(_id: str):
    try:
        _id: int = int(_id)
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


def change_current(_id: str):
    try:
        _id: int = int(_id)
    except:
        print("The id has to be numeric")
        exit()

    try:
        Task.change_current(_id)
    except:
        print("This task do not exist")
        exit()


def main():
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
    db_conn: sqlite.Connection = get_database_connection()
    migrate(".", db_conn)

    match tuple(argv):
        case ("insert",): insert()
        case ("done",): done()
        case ("update", _id): update(_id)
        case ("set-current", _id): change_current(_id)
        case _: main()

if __name__ == "__main__":
    _ = sys.argv.pop(0)
    argv: list[str] = sys.argv
    argc: int = len(sys.argv)

    run(argc, argv)

