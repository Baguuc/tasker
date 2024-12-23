import json
import sqlite3 as sqlite
from glob import glob
from typing import Self
from pathlib import Path
from lib.console import ConsoleColor
from dataclasses import dataclass

home_path: str = str(Path.home())
db_conn_str: str = f"{home_path}/todo_tasks.db"
db_conn = sqlite.connect(db_conn_str)

cursor = db_conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
	id INTEGER PRIMARY KEY,
	title TEXT,
	details TEXT,
    completed INTEGER(1)
);
""")
db_conn.commit()

@dataclass
class Task:
    _id: int
    title: str
    details: list[str]
    
    def get_current() -> Self:
        sql: str = "SELECT id, title, details FROM tasks WHERE completed = 0 ORDER BY id LIMIT 1;"
        res = cursor.execute(sql)
        row: tuple = res.fetchone()
        
        if row == None:
            return Task(-1, "Chill out", [])

        task: Task = Task(row[0], row[1], row[2].split("\n"))
        
        return task    
    
    def select_one(_id: int) -> Self:
        sql: str = "SELECT id, title, details FROM tasks WHERE id = ?;"
        res = cursor.execute(sql, (_id,))
        row: tuple = res.fetchone()

        if row == None:
            raise ValueException("A task with this id do not exist.")

        return Task(
            row[0],
            row[1],
            row[2].split("\n")
        )
    
    def insert(title: str, details: list[str]):
        details: str = "\n".join(details)
        
        sql: str = "INSERT INTO tasks (title, details, completed) VALUES (?, ?, 0);"
        cursor.execute(sql, (title, details))

        db_conn.commit()
    
    def update(_id: int, title: str, details: list[str]):
        details: str = "\n".join(details)
        
        try:
            current_data: str = Task.select_one(_id)
        except ValueError:
            raise ValueError("This details do not exist")

        sql: str = "UPDATE tasks SET title = ?, details = ? WHERE id = ?;"

        new_title: str = title or current_data.title
        new_details: str = details or current_data.details

        cursor.execute(sql, (new_title, new_details, _id))
        db_conn.commit()
    
    def mark_current_done():
        sql: str = "UPDATE tasks SET completed = 1 WHERE id = ?;"
        current_task: Task = Task.get_current()
        cursor.execute(sql, (current_task._id,))
        
        db_conn.commit()

