# Your tasks

Work through these milestones in order. Each one lists what "done" looks
like and a few hints - the design decisions are yours. Ask questions early
and commit small, working steps.

## Milestone 1 - Fuzzy search ("did you mean?")

Today, searching "EDD" finds nothing. It should suggest "ED".

**Where:** `fuzzy_search()` in [backend/search.py](backend/search.py). The
endpoint (`GET /api/suggest`) and the frontend "Did you mean?" list are
already wired to it - implement the function and the UI lights up.

**Done when:** the four skipped tests in
[tests/test_search.py](tests/test_search.py) pass (remove the
`@pytest.mark.skip` marker to run them).

**Hints**

- `difflib.SequenceMatcher` in the standard library gives you a similarity
  ratio between two strings with no extra dependencies. Levenshtein edit
  distance is the classic alternative.
- Decide on a score threshold: "XQWZKJ" shouldn't suggest anything.
- Consider also matching the *expansion* text, so searching "emergency"
  finds ED. Is that fuzzy search's job or exact search's?

## Milestone 2 - Adding acronyms

The "Add a new acronym" form in the UI already posts to
`POST /api/acronyms`, which currently returns 501.

**Where:** `add_acronym()` in [backend/main.py](backend/main.py).

**Done when:** submitting the form stores the acronym and it appears in
search results; duplicates are handled gracefully (the database has a
UNIQUE constraint on acronym + expansion - what should the API return when
it's violated?). Add API tests like the ones in
[tests/test_api.py](tests/test_api.py).

**Hints**

- Should "ed" and "ED" be the same acronym? Normalise before inserting.
- One acronym can legitimately have several expansions (ED could also be
  "eating disorder") - the schema allows this. Does the UI handle it?

## Milestone 3 - Suggestions and review workflow

Letting anyone add acronyms instantly may not be wise. Build a workflow
where users *suggest* additions or corrections, and someone reviews them.

**Where:** `submit_suggestion()` in [backend/main.py](backend/main.py); the
`suggestions` table already exists (see
[backend/database.py](backend/database.py)). You'll need new endpoints to
list pending suggestions and approve/reject them, plus a simple review
page in the frontend.

**Done when:** a user can submit a suggestion, a reviewer can see pending
suggestions and approve one, and approving it makes it searchable.

**Hints**

- Approving a suggestion is just an insert into `acronyms` plus a status
  update - reuse your milestone 2 logic.
- Should the add form from milestone 2 now create suggestions instead of
  inserting directly? Your call - be ready to justify it.

## Milestone 4 - Security

Right now anyone who can reach the API can do anything.

**Done when:** write operations (and the review page) require some form of
authentication, and you can explain the trade-offs of your approach.

**Hints**

- Simplest useful option: an API key checked by a FastAPI dependency
  (`Depends`) on the write endpoints. A session-based login is a step up.
- Think about what actually needs protecting: is read-only search safe to
  leave open on an internal network?

## Milestone 5 - Your ideas

See the stretch goals in [README.md](README.md) - external sources,
deployment, search analytics - or propose something you think the tool
needs. Agree the scope with your supervisor first.
