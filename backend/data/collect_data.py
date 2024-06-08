import pandas as pd
import os

def ingest_movies(imdb_title, imdb_crew, imdb_names, imdb_ratings):
    print("reading file...")
    titles_df = pd.read_table(imdb_title, dtype={4: str})
    crew_df = pd.read_table(imdb_crew)
    names_df = pd.read_table(imdb_names)
    ratings_df = pd.read_table(imdb_ratings)
    # print("crew: " + crew_df.head(5))
    # print("names: " + names_df.head(5))
    # print("titles: " + titles_df.head(5))

    df_1 = pd.merge(titles_df, crew_df, left_on='tconst', right_on='tconst', how='inner')
    df_final = pd.merge(df_1, names_df, left_on='directors', right_on='nconst', how='inner')
    df_final_ratings = pd.merge(df_final, ratings_df, left_on='tconst', right_on='tconst', how='inner')
    # print("df_final:")
    # print(df_final.head(5))
    # print(df_final.columns)

    df = df_final_ratings[['titleType', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes', 'genres', 'primaryName', 'averageRating', 'numVotes']]
    df = df.rename(columns={'primaryName': 'directors'})
    # print("FINAL")
    # print(df.head(10))

    preprocessed = df[(df['startYear'] != '\\N') & (df['runtimeMinutes'] != '\\N')].copy()
    preprocessed.loc[:,'startYear'] = preprocessed['startYear'].astype(int).copy()
    preprocessed.loc[:,'runtimeMinutes'] = preprocessed['runtimeMinutes'].astype(int).copy()
    movies = preprocessed[(preprocessed['titleType'] == 'movie') & (preprocessed['startYear'] > 1920) & (preprocessed['runtimeMinutes'] > 60)]#.sample(n=sample_size, random_state=2)
    movies = movies.rename(columns={'startYear': 'release_date'})
    # print(movies.head(15))
    #print(movies.head(100))

    # duplicates = movies.groupby('primaryTitle').filter(lambda x: len(x) > 1)
    # print(duplicates.head(20))
    # print(movies[movies['primaryTitle'].str.contains('Fargo', na=False)])
    print(movies[movies['directors'].str.contains('Alex Garland', na=False)])


    # we can take [primaryTitle -> Movie.title, genres -> genre (comma separated string), year -> startYear]
    # TODO: description is not in the imdb dataset, so we need to find another data source for movie plot descriptions

    # Directory path
    directory = 'raw/'

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Full file path
    file_path = os.path.join(directory, 'movies.csv')

    print("writing to file...")
    # Write DataFrame to CSV file
    movies.to_csv(file_path, index=False)

if __name__ == '__main__':
    movie_titles_tsv = '/Volumes/Malenia/Data/title.basics.tsv'
    crew_tsv = '/Volumes/Malenia/Data/title.crew.tsv'
    names_tsv = '/Volumes/Malenia/Data/name.basics.tsv'
    ratings_tsv = '/Volumes/Malenia/Data/title.ratings.tsv'
    ingest_movies(movie_titles_tsv, crew_tsv, names_tsv, ratings_tsv)

    # df = pd.read_csv('raw/movies.csv')
    # df['primaryTitle'] = df['primaryTitle'].str.replace(' ', '_').str.replace('[,\'\:\-]', '', regex=True)
    # df['primaryTitle'] = df['primaryTitle'].str.lower()
    # # df['primaryTitle'] = df['primaryTitle'].str.lower().replace(' ', '_').replace("'", "").replace(":", "")
    # print(df['primaryTitle'].head(10))