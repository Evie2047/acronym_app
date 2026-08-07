"""Load acronyms from data/acronyms.csv into the SQLite database.

Run with:  uv run python -m backend.seed

Safe to run repeatedly - existing rows are left alone. To import a real
acronym list later, replace (or extend) the CSV: the only required columns
are acronym, expansion and an optional description.
"""

import csv
from pathlib import Path

from . import database

CSV_PATH = Path(__file__).resolve().parent / "data" / "acronyms.csv"


def seed(csv_path: Path = CSV_PATH) -> int:
    database.init_db()
    conn = database.get_connection()
    inserted = 0
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cur = conn.execute(
                    """
                    INSERT OR IGNORE INTO acronyms (acronym, expansion, description)
                    VALUES (?, ?, ?)
                    """,
                    (
                        row["acronym"].strip(),
                        row["expansion"].strip(),
                        row.get("description", "").strip(),
                    ),
                )
                inserted += cur.rowcount
        conn.commit()
    finally:
        conn.close()
    return inserted


if __name__ == "__main__":
    count = seed()
    print(f"Seeded {count} new acronym(s) into {database.DB_PATH}")
