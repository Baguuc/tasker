import sqlite3 as sqlite

def get_database_connection() -> sqlite.Connection:
    db_conn_str: str = f"./.tasker.db"
    db_conn = sqlite.connect(db_conn_str)
    
    return db_conn
