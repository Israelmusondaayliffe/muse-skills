import sqlite3
from pathlib import Path


def initialize(database: Path) -> None:
    with sqlite3.connect(str(database)) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
        connection.execute("CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, action TEXT NOT NULL)")
