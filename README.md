# Acronym Searcher

An interactive acronym lookup tool. We use a lot of acronyms (ED = Emergency
Department, OP = Outpatients, ...) and this app lets people search them,
and - once you've built it - get "did you mean?" suggestions for typos and
submit new acronyms.

The scaffold runs end-to-end today with exact search. The interesting parts
are left for you: **start with [TASKS.md](TASKS.md)**.

## Architecture

```
React (Vite, port 5173)  --/api/*-->  FastAPI (uvicorn, port 8000)  -->  SQLite (acronyms.db)
```

- **backend/** - FastAPI app. `search.py` holds the search logic,
  `database.py` the SQLite schema, `seed.py` loads the sample data.
- **frontend/** - React app. The Vite dev server proxies `/api` requests to
  the backend, so both run locally side by side.
- **tests/** - pytest suite. The skipped tests in `test_search.py` describe
  the fuzzy search you're going to build.

## Getting started

Prerequisites: [uv](https://docs.astral.sh/uv/) and Node.js (18+).

### 1. Backend

```bash
uv sync                                  # install Python dependencies
uv run python -m backend.seed            # create acronyms.db with sample data
uv run uvicorn backend.main:app --reload # start the API on :8000
```

Interactive API docs: http://localhost:8000/docs

### 2. Frontend (in a second terminal)

```bash
cd frontend
npm install
npm run dev                              # start the UI on :5173
```

Open http://localhost:5173 and search for "ED".

### 3. Tests

```bash
uv run pytest          # 8 pass, 4 skipped (the skipped ones are milestone 1)
```

## Importing a real acronym list

`backend/data/acronyms.csv` is the seed data. Replace or extend it (columns:
`acronym,expansion,description`) and re-run `uv run python -m backend.seed`.
Existing entries are left untouched.

## Stretch goals

Once the TASKS.md milestones are done, some bigger ideas to discuss:

- **External sources** - supplement our list with online resources, e.g. the
  [NHS Data Dictionary](https://www.datadictionary.nhs.uk/) or public
  acronym/abbreviation APIs. Where would lookups from an external source
  slot into the search flow? How do you mark where a definition came from?
- **Deployment** - where should this live so colleagues can use it? What
  changes when it's no longer running on localhost (HTTPS, a real database,
  backups)?
- **Analytics** - which acronyms do people search for and not find? That's
  exactly the list of acronyms worth adding next.
