import pandas as pd # type: ignore
import os

def ingest_movies(imdb_title, imdb_crew, imdb_names, imdb_ratings):
    print("reading file...")
    titles_df = pd.read_table(imdb_title, dtype={4: str})
    crew_df = pd.read_table(imdb_crew)
    names_df = pd.read_table(imdb_names)
    ratings_df = pd.read_table(imdb_ratings)

    df_1 = pd.merge(titles_df, crew_df, left_on='tconst', right_on='tconst', how='inner')
    df_final = pd.merge(df_1, names_df, left_on='directors', right_on='nconst', how='inner')
    df_final_ratings = pd.merge(df_final, ratings_df, left_on='tconst', right_on='tconst', how='inner')

    df = df_final_ratings[['titleType', 'tconst', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes', 'genres', 'primaryName', 'averageRating', 'numVotes']]
    df = df.rename(columns={'primaryName': 'directors'})

    preprocessed = df[(df['startYear'] != '\\N') & (df['runtimeMinutes'] != '\\N')].copy()
    preprocessed.loc[:,'startYear'] = preprocessed['startYear'].astype(int).copy()
    preprocessed.loc[:,'runtimeMinutes'] = preprocessed['runtimeMinutes'].astype(int).copy()
    movies = preprocessed[(preprocessed['titleType'] == 'movie') & (preprocessed['startYear'] > 1920) & (preprocessed['runtimeMinutes'] > 60)]
    movies = movies.rename(columns={'startYear': 'release_date'})

    print(movies[movies['directors'].str.contains('Alex Garland', na=False)])

    directory = 'raw/'
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'movies.csv')

    print("writing to file...")
    movies.to_csv(file_path, index=False)

if __name__ == '__main__':
    movie_titles_tsv = '/Volumes/Malenia/Data/title.basics.tsv'
    crew_tsv = '/Volumes/Malenia/Data/title.crew.tsv'
    names_tsv = '/Volumes/Malenia/Data/name.basics.tsv'
    ratings_tsv = '/Volumes/Malenia/Data/title.ratings.tsv'
    ingest_movies(movie_titles_tsv, crew_tsv, names_tsv, ratings_tsv)