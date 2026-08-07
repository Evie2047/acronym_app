"""SQLite connection handling and schema setup.

The database is a single file (acronyms.db) in the project root. SQLite ships
with Python, so there is nothing to install or run separately.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "acronyms.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS acronyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acronym TEXT NOT NULL,
    expansion TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    UNIQUE (acronym, expansion)
);

-- Suggestions submitted by users: new acronyms or corrections to existing
-- ones. The intern will build the workflow around this table (see TASKS.md).
CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acronym TEXT NOT NULL,
    expansion TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',  -- pending / approved / rejected
    submitted_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Open a connection with rows accessible by column name.

    check_same_thread=False lets FastAPI use the connection from its worker
    threads; it's safe because each request opens its own connection.
    """
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    """Create tables if they don't exist. Safe to call on every startup."""
    conn = get_connection(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
