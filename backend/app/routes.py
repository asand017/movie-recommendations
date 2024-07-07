from flask import Blueprint, request, jsonify # type: ignore
from sqlalchemy import text # type: ignore
from app.models import Movie
from app.recommender import recommend_movies
from datetime import datetime, timedelta, timezone
from app import db, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt, set_access_cookies # type: ignore
import os
import requests # type: ignore

api = Blueprint('api', __name__)

@api.after_request
def refreshing_expired_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
        

@api.route('/')
def home():
    return jsonify({"msg":"Welcome to the Movie Recommendation System"}), 200

# authenticate user and send back jwt
@api.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        print("Bad username or password")
        return jsonify({"msg": "Bad username or password"}), 401
    print("Good username and password")
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@api.route("/logout", methods=["POST"])
def logout():
    print("logging out")
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# tmdb call to get configuration
@api.route('/configuration', methods=['GET'])
def get_configuration():
    tmdb_token = os.getenv('TMDB_TOKEN')
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + tmdb_token
    }
    
    url = "https://api.themoviedb.org/3/configuration"
    response = requests.get(url, headers=headers)
    return jsonify(response.json())
    
@api.route('/tmdb/movies', methods=['GET'])
def get_tmdb_movies():
    tmdb_token = os.getenv('TMDB_TOKEN')
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + tmdb_token
    }
    
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@api.route('/tmdb/search', methods=['GET'])
def get_tmdb_search():
    tmdb_token = os.getenv('TMDB_TOKEN')
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + tmdb_token
    }
    
    search = request.args.get('search', '', type=str)
    url = f"https://api.themoviedb.org/3/search/movie?query={search}&include_adult=false&language=en-US&page=1"
    response = requests.get(url, headers=headers)
    return jsonify(response.json())
    

# todo: refine search if possible
@api.route('/movies', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    print("page: " + str(page))
    print("per_page: " + str(per_page))  
    
    # Apply the search filter
    query = db.select(Movie).where(Movie.poster_path != "")
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))

    # Paginate the filtered results
    movie_page = db.paginate(query, page=page, per_page=per_page)
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
    }), 200
    
@api.route('/rate/<int:movie_id>', methods=['POST'])
@jwt_required()
def rate_movie(movie_id):
    current_user = get_jwt_identity()
    print("current_user: " + current_user)
    
    req = request.get_json()
    movie = db.session.execute(db.select(Movie).filter_by(id=movie_id))
    print("rating " + movie.title)
    print(req)
    return 200
    

@api.route('/recommend', methods=['POST'])
@jwt_required()
def recommend():
    current_user = get_jwt_identity()
    print("current_user: " + current_user)
    return jsonify({"message": "This is the recommend endpoint"}), 200

@api.route('/test_db', methods=['GET'])
def test_db():
    try:
        # Attempt to connect to the database
        db.session.execute(db.select(text('1')))
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500