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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    movie_page = db.paginate(db.select(Movie), page=page, per_page=per_page)
    movies = movie_page.items
    return jsonify({
        'data': [movie.to_dict() for movie in movies],
        'total': movie_page.total,
        'pages': movie_page.pages,
        'current_page': movie_page.page,
        'next_page': movie_page.next_num,
        'prev_page': movie_page.prev_num,
        'has_next': movie_page.has_next,
        'has_prev': movie_page.has_prev
    })
    
@api.route('/rate/<int:movie_id>', methods=['POST'])
def rate_movie(movie_id):
    req = request.get_json()
    movie = db.session.execute(db.select(Movie).filter_by(id=movie_id))
    print("rating " + movie.title)
    print(req)
    return 200
    

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