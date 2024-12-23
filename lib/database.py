import sqlite3 as sqlite
from pathlib import Path

def get_database_connection() -> sqlite.Connection:
    home_path: str = str(Path.home())
    db_conn_str: str = f"{home_path}/todo_tasks.db"
    db_conn = sqlite.connect(db_conn_str)
    
    return db_conn
