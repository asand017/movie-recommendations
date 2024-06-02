from flask import Blueprint, request, jsonify
from app import db
from app.models import Movie
from app.recommender import recommend_movies

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return "Welcome to the Movie Recommendation System"

@api.route('/movies', methods=['GET'])
def get_movies():
    pass
    # movies = Movie.query.all()
    # return jsonify([movie.title for movie in movies])

@api.route('/recommend', methods=['POST'])
def recommend():
    pass
    # user_preferences = request.json
    # recommendations = recommend_movies(user_preferences)
    # return jsonify(recommendations)
