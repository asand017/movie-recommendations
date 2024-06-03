import pandas as pd

def ingest_movies(tsv_file, sample_size=1000):
    df = pd.read_table(tsv_file)
    movies = df[df['titleType'] == 'movie']
    print(movies.head(15))

if __name__ == '__main__':
    movie_titles_tsv = '/Volumes/Malenia/Data/title.basics.tsv'
    ingest_movies(movie_titles_tsv)