import pandas as pd
import os

def ingest_movies(imdb_title, imdb_crew, imdb_names):
    print("reading file...")
    df = pd.read_table(imdb_title, dtype={4: str})
    crew_df = pd.read_table(imdb_crew)
    names_df = pd.read_table(imdb_names)
    print("crew:" + crew_df.head(5))
    print("names:" + names_df.head(5))

    preprocessed = df[(df['startYear'] != '\\N') & (df['runtimeMinutes'] != '\\N')].copy()
    preprocessed.loc[:,'startYear'] = preprocessed['startYear'].astype(int).copy()
    preprocessed.loc[:,'runtimeMinutes'] = preprocessed['runtimeMinutes'].astype(int).copy()
    movies = preprocessed[(preprocessed['titleType'] == 'movie') & (preprocessed['startYear'] > 1920) & (preprocessed['runtimeMinutes'] > 60)]#.sample(n=sample_size, random_state=2)
    # print(movies.head(15))
    #print(movies.head(100))
    print(movies[movies['primaryTitle'] == 'Civil War'])

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
    ingest_movies(movie_titles_tsv, crew_tsv, names_tsv)

    # df = pd.read_csv('raw/movies.csv')
    # df['primaryTitle'] = df['primaryTitle'].str.replace(' ', '_').str.replace('[,\'\:\-]', '', regex=True)
    # df['primaryTitle'] = df['primaryTitle'].str.lower()
    # # df['primaryTitle'] = df['primaryTitle'].str.lower().replace(' ', '_').replace("'", "").replace(":", "")
    # print(df['primaryTitle'].head(10))