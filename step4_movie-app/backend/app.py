import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
client = MongoClient(
    os.getenv("MONGO_URI", "mongodb://movie-db:27017/movies_db"),
    serverSelectionTimeoutMS=5000,
)
db = client.get_database("movies_db")
AI_URL = os.getenv("AI_URL", "http://movie-ai:8000")

@app.get("/api/movies")
def get_movies():
    category = request.args.get("category", "").lower().strip()
    query = {"category": category} if category else {}
    try:
        movies = list(db.movies.find(query, {"_id": 0}))
        return jsonify({"category": category or "all", "count": len(movies), "movies": movies})
    except Exception:
        app.logger.exception("Could not fetch movies")
        return jsonify({"error": "Could not fetch movies"}), 503

@app.get("/api/recommendations")
def recommendations():
    category = request.args.get("category", "").lower().strip()
    if not category:
        return jsonify({"error": "category is required"}), 400
    try:
        titles = [movie["title"] for movie in db.movies.find({"category": category}, {"_id": 0, "title": 1})]
        response = requests.post(f"{AI_URL}/recommend", json={"category": category, "titles": titles}, timeout=180)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException:
        app.logger.exception("AI recommendation service unavailable")
        return jsonify({"error": "AI recommendation service unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
