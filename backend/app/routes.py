from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.models import Movie
from app.recommender import recommend_movies
from app import db

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return "Welcome to the Movie Recommendation System"

@api.route('/movies', methods=['GET'])
def get_movies():
    return jsonify({"message": "This is the movies endpoint"})

@api.route('/recommend', methods=['POST'])
def recommend():
    return jsonify({"message": "This is the recommend endpoint"})

@api.route('/test_db', methods=['GET'])
def test_db():
    try:
        # Attempt to connect to the database
        db.session.execute(db.select(text('1')))
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500