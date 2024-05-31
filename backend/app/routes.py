from flask import request, jsonify, current_app
from app import db
from app.models import Movie
from app.recommender import recommend_movies

@current_app.route('/')
def home():
    return "Welcome to the Movie Recommendation System"

@current_app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.title for movie in movies])

@current_app.route('/recommend', methods=['POST'])
def recommend():
    user_preferences = request.json
    recommendations = recommend_movies(user_preferences)
    return jsonify(recommendations)
