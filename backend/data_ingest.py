import pandas as pd # type: ignore
import requests # type: ignore
import json
import os
import sys
from app import create_app, db
from app.models import Movie
# import concurrent.futures
# import threading
import time
from sqlalchemy.exc import IntegrityError # type: ignore
from sqlalchemy import update, select, desc # type: ignore


""" ingest data sources into recommendation app db """
tmdb_token = os.getenv('TMDB_TOKEN')
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + tmdb_token
}
tmdb_find_base_url = "https://api.themoviedb.org/3/find/"

run_flag = os.getenv("RUN_FLAG")

app = create_app()
# lock = threading.Lock()

def ingest_movies(file):
    with app.app_context():
        try:
            if(db.first_or_404(db.select(Movie))):
                print("Movies already ingested")
                return
        except Exception as e:
            print(f"error checking movies db for elements e: {e}")
        
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            # if the movie has already been added, just updating the column values per db row
            
            movie = Movie(title=row['primaryTitle'],
                        genre=row['genres'], year=row['release_date'], description=row['description'], review=row['review'],
                            directors=row['directors'], runtime=row['runtimeMinutes'], 
                            imdb_rating=row['averageRating'], imdb_votes=row['numVotes'], imdb_id=row['tconst'])
            
            try:
                db.session.add(movie)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Integrity error adding movie: {movie.title}")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding movie: {e}")
        
def get_tmdb_data(full_url):
    time.sleep(0.1)
    r = requests.get(full_url, headers=headers)
    return json.loads(r.text)
        
def add_images(movie_updates):
    print("batch adding...")
    print(movie_updates)
    with app.app_context():
        try:
            # Perform bulk update
            # db.session.bulk_update_mappings(Movie, movie_updates)
            db.session.execute(update(Movie), movie_updates)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during bulk update: {e}")
        finally:
            db.session.close()
    

if __name__ == '__main__':
    print("run flag = " + str(run_flag))
    if(run_flag == "True"):
        job = sys.argv[1]
        if(job == "ingest"):
            data_file = os.path.abspath('data/processed/movies.csv')
            ingest_movies(data_file)
        elif(job == "add_movie_images"):
            # print("ADDING IMAGES")
            with app.app_context():
                stmt = select(Movie).where(Movie.tmdb_id == None).order_by(desc(Movie.id))
                print(stmt)
                movies = db.session.execute(stmt).scalars().all()
                print("length of selection: " + str(len(movies)))     
                
                movie_updates = []
                # print("empty movie updates list:")
                # print(movie_updates)
                for movie in movies:
                    
                    # print("imdb_id: " + str(movie.imdb_id))
                    # break
                    relative_url = tmdb_find_base_url + str(movie.imdb_id) + "?external_source=imdb_id"
                    res = get_tmdb_data(relative_url)
                    
                    tmdb_results = []
                    if 'movie_results' in res:
                        tmdb_results = res['movie_results']
                    elif 'results' in res:
                        tmdb_results = res['results']
                        
                    tmdb_movie = tmdb_results[0] if len(tmdb_results) > 0 else {}
                    print(len(tmdb_movie))
                    if len(tmdb_movie) > 0:
                        print("adding movie")
                        movie_update = {
                            'id': movie.id,
                            'tmdb_id': str(tmdb_movie['id']) if tmdb_movie['id'] is not None else None,
                            'backdrop_path': tmdb_movie['backdrop_path'] if tmdb_movie['backdrop_path'] is not None else None,
                            'poster_path': tmdb_movie['poster_path'] if tmdb_movie['poster_path'] is not None else None
                        }
                        movie_updates.append(movie_update)
                        print("updates list length: " + str(len(movie_updates)))
                        if len(movie_updates) % 30 == 0:                        
                            add_images(movie_updates)
                            print("emptying movie_updates list: size - " + str(len(movie_updates)))
                            movie_updates = []
                
                add_images(movie_updates)
                db.session.close()