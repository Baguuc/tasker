import json
from glob import glob
from typing import Self
import sqlite3 as sqlite
from dataclasses import dataclass
from lib.console import ConsoleColor
from lib.database import get_database_connection

db_conn: sqlite.Connection = get_database_connection()

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
    current: bool
    
    def get_current() -> Self:
        sql: str = "SELECT id, title, details, current FROM tasks WHERE completed = 0 AND current = 1;"
        res = cursor.execute(sql)
        row: tuple = res.fetchone()
        
        if row == None:
            return Task(
                0,
                "Chill out",
                [],
                True
            )

        task: Task = Task(
            row[0],
            row[1],
            row[2].split("\n"),
            bool(row[3])
        )
        
        return task


    def select_all_uncompleted() -> list[Self]:
        sql: str = "SELECT id, title, details, current FROM tasks WHERE completed = 0;"
        res = cursor.execute(sql)
        rows: list[tuple] = res.fetchall()
        tasks: list[Task] = list(
            map(
                lambda item: Task(item[0], item[1], item[2], item[3]),
                rows
            )
        )

        return tasks


    def select_one(_id: int) -> Self:
        sql: str = "SELECT id, title, details, current FROM tasks WHERE id = ?;"
        res = cursor.execute(sql, (_id,))
        row: tuple = res.fetchone()

        if row == None:
            raise ValueException("A task with this id do not exist.")

        return Task(
            row[0],
            row[1],
            row[2].split("\n"),
            bool(row[3])
        )
    
    def insert(title: str, details: list[str], current: bool):
        details: str = "\n".join(details)
        current = 1 if current else 0

        sql: str = "INSERT INTO tasks (title, details, completed, current) VALUES (?, ?, 0, ?);"
        cursor.execute(sql, (title, details, current))

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

    def change_current(_id: int):
        current_task: Task = Task.get_current()
        sql: str = "UPDATE tasks SET current = 0 WHERE id = ?;";
        db_conn.execute(sql, (current_task._id,))
        
        sql: str = "UPDATE tasks SET current = 1 WHERE id = ?;";
        db_conn.execute(sql, (_id,))
        
        db_conn.commit()
    
    def mark_done(_id):
        sql: str = "UPDATE tasks SET completed = 1 WHERE id = ?;"
        cursor.execute(sql, (_id,))
        
        db_conn.commit()
