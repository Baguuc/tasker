import os
import sqlite3 as sqlite

migrations: list[str] = [
    """
    CREATE TABLE IF NOT EXISTS tasks (
	    id INTEGER PRIMARY KEY,
	    title TEXT,
	    details TEXT,
        completed INTEGER(1)
    );
    """
]

def migrate(project_dir: str, db_conn: sqlite.Connection):
    cursor: sqlite.Cursor = db_conn.cursor()
    
    sql: str = """
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY
    );
    """
    cursor.execute(sql)
    db_conn.commit()

    for idx,migration_sql in enumerate(migrations):
        sql: str = "SELECT 1 FROM migrations WHERE id = ?;"
        cursor.execute(sql, (idx+1,))
        res: tuple|None = cursor.fetchone()

        if not res is None:
            continue
             
        try:
            for statement in migration_sql.split(";"):
                if not statement.startswith('--'):
                    cursor.execute(f"{statement};")

            sql: str = "INSERT INTO migrations (id) VALUES (NULL);"
            cursor.execute(sql)
        except Exception as e:
            print(f"Migration number {idx+1} failed.")
            print(f"Migration SQL:\n{migration_sql}")
            print(e)
            exit()

        db_conn.commit()
