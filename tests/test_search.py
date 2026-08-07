"""Tests for backend/search.py.

The exact-search tests pass today. The fuzzy-search tests are marked as
skipped: they describe the behaviour fuzzy_search() should have once you
implement it (TASKS.md milestone 1). Remove the skip markers as you go -
they are your acceptance criteria.
"""

import pytest

from backend.search import exact_search, fuzzy_search


class TestExactSearch:
    def test_exact_match(self, db):
        results = exact_search(db, "ED")
        assert [r.acronym for r in results] == ["ED"]
        assert results[0].expansion == "Emergency Department"

    def test_is_case_insensitive(self, db):
        assert [r.acronym for r in exact_search(db, "ed")] == ["ED"]

    def test_prefix_match_shortest_first(self, db):
        assert [r.acronym for r in exact_search(db, "EC")] == ["ECG", "ECHO"]

    def test_no_match_returns_empty_list(self, db):
        assert exact_search(db, "ZZZ") == []


@pytest.mark.skip(reason="fuzzy_search not implemented yet - TASKS.md milestone 1")
class TestFuzzySearch:
    def test_close_typo_suggests_correction(self, db):
        """A one-character typo should still find the acronym."""
        suggestions = fuzzy_search(db, "EDD")
        assert "ED" in [s.acronym for s in suggestions]

    def test_best_match_comes_first(self, db):
        """Results should be ordered by score, highest first."""
        suggestions = fuzzy_search(db, "ECG")
        scores = [s.score for s in suggestions]
        assert scores == sorted(scores, reverse=True)

    def test_scores_are_normalised(self, db):
        suggestions = fuzzy_search(db, "EDD")
        assert all(0 <= s.score <= 1 for s in suggestions)

    def test_nonsense_query_returns_nothing(self, db):
        """Completely unrelated input should not produce suggestions."""
        assert fuzzy_search(db, "XQWZKJ") == []
