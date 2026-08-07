"""FastAPI application.

Run with:  uv run uvicorn backend.main:app --reload
Interactive API docs are served at http://localhost:8000/docs
"""

import sqlite3
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import database, search
from .models import Acronym, AcronymCreate, Suggestion, SuggestionCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(title="Acronym Searcher", lifespan=lifespan)

# The React dev server runs on a different port, so allow it to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = database.get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/api/acronyms", response_model=list[Acronym])
def list_acronyms(conn: sqlite3.Connection = Depends(get_db)):
    """All acronyms, alphabetically."""
    rows = conn.execute(
        "SELECT id, acronym, expansion, description FROM acronyms ORDER BY acronym"
    ).fetchall()
    return [Acronym(**dict(row)) for row in rows]


@app.get("/api/search", response_model=list[Acronym])
def search_acronyms(
    q: str = Query(min_length=1), conn: sqlite3.Connection = Depends(get_db)
):
    """Exact/prefix search. Returns an empty list if nothing matches."""
    return search.exact_search(conn, q)


@app.get("/api/suggest", response_model=list[Suggestion])
def suggest_acronyms(
    q: str = Query(min_length=1), conn: sqlite3.Connection = Depends(get_db)
):
    """'Did you mean?' suggestions for queries with no exact match.

    Wired to search.fuzzy_search() - implement that function and this
    endpoint starts working (TASKS.md milestone 1).
    """
    try:
        return search.fuzzy_search(conn, q)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Not implemented - see TASKS.md milestone 1")


@app.post("/api/acronyms", response_model=Acronym, status_code=201)
def add_acronym(
    payload: AcronymCreate, conn: sqlite3.Connection = Depends(get_db)
):
    """Add a new acronym directly (TASKS.md milestone 2).

    Things to think about: duplicates, normalising case, and whether adding
    should really be instant or go through the suggestions workflow instead.
    """
    raise HTTPException(status_code=501, detail="Not implemented - see TASKS.md milestone 2")


@app.post("/api/suggestions", status_code=201)
def submit_suggestion(
    payload: SuggestionCreate, conn: sqlite3.Connection = Depends(get_db)
):
    """Submit a suggestion for review (TASKS.md milestone 3).

    The suggestions table already exists in the database - see database.py.
    You will also want endpoints to list pending suggestions and to
    approve/reject them.
    """
    raise HTTPException(status_code=501, detail="Not implemented - see TASKS.md milestone 3")
