import pandas as pd # type: ignore
import os
from app import create_app, db
from app.models import Movie
from sqlalchemy.exc import IntegrityError # type: ignore

""" ingest data sources into recommendation app db """

app = create_app()
app.app_context().push()

def ingest_movies(file):
    
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
        
        db.session.add(movie)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            break

if __name__ == '__main__':
    data_file = os.path.abspath('data/processed/movies.csv')
    ingest_movies(data_file)