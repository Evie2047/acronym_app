"""Shared test fixtures.

Tests run against a temporary SQLite database seeded with a few known
acronyms, so they never touch the real acronyms.db file.
"""

import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend import database
from backend.main import app, get_db

TEST_ROWS = [
    ("ED", "Emergency Department", "Urgent and emergency care"),
    ("OP", "Outpatients", "Clinics without admission"),
    ("ECG", "Electrocardiogram", "Heart trace"),
    ("ECHO", "Echocardiogram", "Ultrasound of the heart"),
]


@pytest.fixture
def db(tmp_path) -> sqlite3.Connection:
    """A seeded, throwaway database connection."""
    path = tmp_path / "test.db"
    database.init_db(path)
    conn = database.get_connection(path)
    conn.executemany(
        "INSERT INTO acronyms (acronym, expansion, description) VALUES (?, ?, ?)",
        TEST_ROWS,
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def client(db) -> TestClient:
    """A FastAPI test client whose endpoints use the throwaway database."""
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()
