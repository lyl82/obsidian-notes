"""SQLite schema initialization for the 人生OS 1.0 project."""
from pathlib import Path
import sqlite3
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "life_os.db"

SCHEMA_STATEMENTS: Iterable[str] = (
    """
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        content TEXT NOT NULL,
        content_hash TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        expression TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_id INTEGER NOT NULL,
        rule_name TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (log_id) REFERENCES logs(id) ON DELETE CASCADE,
        FOREIGN KEY (rule_name) REFERENCES rules(name) ON DELETE CASCADE
    );
    """,
)




def connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> Path:
    with connect() as conn:
        for statement in SCHEMA_STATEMENTS:
            conn.execute(statement)
    return DB_PATH



if __name__ == "__main__":
    database_path = init_db()
    print(f"SQLite database initialized at {database_path}")
