import pytest
import mongomock
from unittest.mock import Mock, patch

@pytest.fixture
def client():
    """Sets up an in-memory MongoDB instance and Flask test client."""
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["movies_db"]
    mock_db.movies.insert_many([
        {"title": "The Dark Knight", "category": "thriller", "year": 2008, "synopsis": "Batman protects Gotham."},
        {"title": "Superbad", "category": "comedy", "year": 2007, "synopsis": "Two friends go on an adventure."}
    ])

    with patch("app.db", mock_db):
        from app import app
        app.config["TESTING"] = True
        with app.test_client() as test_client:
            yield test_client

def test_get_movies_filtering_and_projection(client):
    """Verify endpoint status, filtering logic, and _id exclusion."""
    # Test category filtering
    res = client.get("/api/movies?category=thriller")
    assert res.status_code == 200
    
    data = res.get_json()
    assert data["count"] == 1
    assert data["movies"][0]["title"] == "The Dark Knight"
    assert "_id" not in data["movies"][0]

    # Test all movies fallback
    res_all = client.get("/api/movies")
    assert res_all.status_code == 200
    assert res_all.get_json()["count"] == 2

def test_recommendations_requires_category(client):
    res = client.get("/api/recommendations")
    assert res.status_code == 400
    assert res.get_json()["error"] == "category is required"

def test_recommendations_forwards_category_and_titles(client):
    fake_response = Mock()
    fake_response.json.return_value = {
        "category": "comedy",
        "recommendation": "Superbad puede gustarte por su humor entre amigos.",
        "model": "test-model",
    }
    fake_response.raise_for_status.return_value = None

    with patch("app.requests.post", return_value=fake_response) as post:
        res = client.get("/api/recommendations?category=comedy")

    assert res.status_code == 200
    assert res.get_json()["recommendation"].startswith("Superbad")
    assert post.call_args.kwargs["json"] == {"category": "comedy", "titles": ["Superbad"]}
