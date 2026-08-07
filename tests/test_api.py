"""Example API tests using FastAPI's TestClient.

Use these as a template when you build the add/suggest endpoints.
"""


def test_list_acronyms(client):
    response = client.get("/api/acronyms")
    assert response.status_code == 200
    acronyms = [item["acronym"] for item in response.json()]
    assert acronyms == sorted(acronyms)
    assert "ED" in acronyms


def test_search_returns_matches(client):
    response = client.get("/api/search", params={"q": "ed"})
    assert response.status_code == 200
    assert response.json()[0]["expansion"] == "Emergency Department"


def test_search_no_match_returns_empty(client):
    response = client.get("/api/search", params={"q": "ZZZ"})
    assert response.status_code == 200
    assert response.json() == []


def test_stubbed_endpoints_return_501(client):
    """These endpoints are yours to implement - update these tests when you do."""
    assert client.get("/api/suggest", params={"q": "EDD"}).status_code == 501
    assert (
        client.post(
            "/api/acronyms",
            json={"acronym": "TTO", "expansion": "To Take Out"},
        ).status_code
        == 501
    )
    assert (
        client.post(
            "/api/suggestions",
            json={"acronym": "TTO", "expansion": "To Take Out"},
        ).status_code
        == 501
    )
