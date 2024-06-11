import pandas as pd
import os
from app import create_app, db
from app.models import Movie, Rating, User
from sqlalchemy.exc import IntegrityError

app = create_app()
app.app_context().push()

def ingest_movies(file):
    if(db.first_or_404(db.select(Movie))):
        print("Movies already ingested")
        return
    
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        movie = Movie(title=row['primaryTitle'],
                      genre=row['genres'], year=row['release_date'], description='', review='',
                        directors=row['directors'], runtime=row['runtimeMinutes'], 
                        imdb_rating=row['averageRating'], imdb_votes=row['numVotes'])
        db.session.add(movie)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            break

# def ingest_ratings(file):
#     df = pd.read_csv(file)
#     movies = db.session.execute(db.select(Movie))
#     print(movies)
    
#     for _, row in df.iterrows():
#         movie = Rating(title=row['primaryTitle'],
#                       genre=row['genres'], year=row['release_date'],
#                         directors=row['directors'], runtime=row['runtimeMinutes'])
#         db.session.add(movie)
        
#         try:
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()
#             break
    

# def ingest_users():
#     user = User(username="testUser", email="aaron.san", password="123456")


if __name__ == '__main__':
    data_file = os.path.abspath('data/raw/movies.csv')
    ingest_movies(data_file)