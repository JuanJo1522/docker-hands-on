import os

from pymongo import MongoClient

from app import app


def test_movies_endpoint_reads_seeded_real_mongodb():
    """Exercise the Flask endpoint against the MongoDB service from Compose."""
    uri = os.environ["TEST_MONGO_URI"]
    mongo = MongoClient(uri, serverSelectionTimeoutMS=5000)
    database = mongo["movies_db"]
    mongo.admin.command("ping")
    assert database.movies.count_documents({}) == 24

    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/api/movies?category=drama")

    mongo.close()
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 8
    assert any(movie["title"] == "The Shawshank Redemption" for movie in data["movies"])
    assert all("_id" not in movie for movie in data["movies"])
