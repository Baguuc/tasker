import json
from typing import Self
from pathlib import Path
from scriptlib.color import ConsoleColor
from dataclasses import dataclass

TASKS_FILE_PATH: Path = Path("/home/baguuc/.todo_tasks")

@dataclass
class Task:
    title: str
    details: list[str]
    
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
