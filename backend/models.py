"""Pydantic models shared by the API endpoints."""

from pydantic import BaseModel, Field


class Acronym(BaseModel):
    id: int
    acronym: str
    expansion: str
    description: str = ""


class AcronymCreate(BaseModel):
    acronym: str = Field(min_length=1, max_length=20)
    expansion: str = Field(min_length=1)
    description: str = ""


class Suggestion(BaseModel):
    """A 'did you mean?' suggestion returned by fuzzy search.

    score should be between 0 and 1, where 1 is a perfect match. How you
    calculate it is up to you - see fuzzy_search() in search.py.
    """

    acronym: str
    expansion: str
    score: float


class SuggestionCreate(BaseModel):
    """A user-submitted suggestion for a new or corrected acronym."""

    acronym: str = Field(min_length=1, max_length=20)
    expansion: str = Field(min_length=1)
    description: str = ""
