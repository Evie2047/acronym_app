"""Search logic.

exact_search() works and is what the UI uses today. fuzzy_search() is the
interesting part and is left for you to implement - see TASKS.md milestone 1.
"""

import sqlite3

from .models import Acronym, Suggestion


def exact_search(conn: sqlite3.Connection, query: str) -> list[Acronym]:
    """Case-insensitive exact and prefix match on the acronym itself.

    "ed" matches "ED"; "ec" matches "ECG" and "ECHO". This is deliberately
    basic - it finds nothing if the user mistypes ("EDD" returns no results).
    """
    rows = conn.execute(
        """
        SELECT id, acronym, expansion, description
        FROM acronyms
        WHERE acronym LIKE ? COLLATE NOCASE
        ORDER BY length(acronym), acronym
        """,
        (f"{query}%",),
    ).fetchall()
    return [Acronym(**dict(row)) for row in rows]


def fuzzy_search(conn: sqlite3.Connection, query: str) -> list[Suggestion]:
    """Return 'did you mean?' suggestions for a query with no exact matches.

    YOUR TASK (see TASKS.md milestone 1):

    Given a query like "EDD", return close matches such as ED, ordered by
    similarity (best first). Each result is a Suggestion with a score
    between 0 and 1.

    Ideas to explore:
      - Edit distance (Levenshtein). Python's difflib.SequenceMatcher is a
        good starting point and needs no extra dependencies.
      - Should you also match against the expansion text, so searching
        "emergency" finds ED = "emergency department"?
      - How many suggestions is useful? What score is too low to show?

    The endpoint (GET /api/suggest?q=...) and the frontend "Did you mean?"
    component are already wired to this function - as soon as it returns
    results they will appear in the UI.
    """
    raise NotImplementedError("fuzzy_search is your task - see TASKS.md")
