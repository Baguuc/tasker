import json
from typing import Self
from pathlib import Path
from lib.console import ConsoleColor
from dataclasses import dataclass

TASKS_FILE_PATH: Path = Path("/home/baguuc/.todo_tasks")

@dataclass
class Task:
    title: str
    details: list[str]
    
    def get_current() -> Self:
        all_tasks: list[Task] = Task.get_all()

        if len(all_tasks) == 0:
            return Task("Chill out", [])

        current_task: Task = all_tasks[0]

        return current_task
    def get_all() -> list[Self]:
        tasks: list[Self] = []

        # create file, pass if already exist
        if not TASKS_FILE_PATH.exists():
            TASKS_FILE_PATH.touch()
        
        with open(TASKS_FILE_PATH, "r") as f:
            loaded: dict = {}

            try:
                loaded = json.load(f)
            except:
                print(ConsoleColor.color(ConsoleColor.RED, "Cannot load the JSON data."))
                exit()

            tasks = list(
                map(
                    lambda item: Task(
                        item["title"], 
                        item["details"]
                    ),
                    loaded
                )
            )

        return tasks

    def insert(self):
        all_tasks: list[Self] = Task.get_all()
        all_tasks.append(self)
        as_dict: list[dict] = list(map(lambda item: item.__dict__, all_tasks))               
        
        with open(TASKS_FILE_PATH, "w") as f:
            dumped: str = json.dumps(as_dict)
            f.write(dumped)


