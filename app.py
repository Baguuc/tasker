from lib.console import ConsoleColor, Console, Alignment, Screen
from lib.database import get_database_connection
from lib.migrations import migrate
from lib.tasks import Task
from time import sleep
import sys
import os

def insert():
    title: str = input("Enter title of the task: ")
    details: list[str] = []

    while (line := input("Enter next line of details (leave blank to exit): ")) != "":
        details.append(line)
   
    current: str = input("Mark this task as done? (y/N)")
    if current.lower() == "y":
        current = True
    else:
        current = False

    Task.insert(title, details, current)


def done():
    tasks: list[Task] = Task.select_all_uncompleted()
    lines: list[str] = list(map(lambda task: task.title, tasks))
    callbacks: list[callable] = list(map(lambda task: lambda: Task.mark_done(task), tasks))
    state: dict = {
        "current_line": 0
    }

    if len(tasks) == 0:
        print("No tasks to mark done.")
        return
    

    def get_current_line_idx():
        return state["current_line"]
    
    
    def set_current_line_idx(idx: int):
        state["current_line"] = idx

    
    def set_current_line(new_idx: int):
        current_line = get_current_line_idx()

        lines[current_line] = ConsoleColor.strip(lines[current_line])
        lines[new_idx] = ConsoleColor.color(lines[new_idx], [ConsoleColor.BG_YELLOW, ConsoleColor.BOLD])

        set_current_line_idx(new_idx)
    

    set_current_line(0)
    
    
    def move_down():
        current_line_idx = get_current_line_idx()

        if current_line_idx < len(lines) - 1:
            set_current_line(current_line_idx + 1)
    
    
    def move_up():
        current_line_idx = get_current_line_idx()
        
        if current_line_idx > 0:
            set_current_line(current_line_idx - 1)


    def handle_keypress(_input, lines):
        if _input == "arrow up": move_up()
        if _input == "arrow down": move_down()
        if _input == "enter":
            Console.clear()
            task = tasks[get_current_line_idx()]
            Task.mark_done(task._id)
            
            print(f"Marked task {task.title} (id: {task._id}) as done.")
            sleep(2)

            return False, [] 
        return True, lines

    Screen.render(lines, handle_keypress)


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

