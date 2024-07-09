import requests # type: ignore
import os
import pandas as pd # type: ignore
import json
from dotenv import load_dotenv # type: ignore

import concurrent.futures
import time
import csv
import threading

load_dotenv(dotenv_path='../../.env')

movies_csv = os.path.abspath("./raw/movies.csv")
processed_movies_csv = os.path.abspath("./processed/movies.csv")
df = pd.read_csv(movies_csv)

start_time = time.time()

url_find_movie = "https://api.themoviedb.org/3/find/"
url_reviews = "https://api.themoviedb.org/3/movie/"
tmdb_token = os.getenv('TMDB_TOKEN')
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + tmdb_token
}

lock = threading.Lock()

with open(processed_movies_csv, mode='w', newline='') as file:
    df2 = df.copy()
    df2['description'] = ''
    df2['review'] = ''
    writer = csv.writer(file)
    writer.writerow(df2.columns)
   
rows = [(index, row) for index, row in df2.iterrows()] 

def fetch_tmdb_data(url):
    r = requests.get(url, headers=headers)
    return json.loads(r.text)
    
def parse_row(row):
    final_row = row[1]
    final_row['description'] = ''
    final_row['review'] = ''
    imdb_id = row[1]['tconst']
    url = url_find_movie + str(imdb_id) + "?external_source=imdb_id"
    
    find_res = fetch_tmdb_data(url)
    
    tmdb_results = []
    if 'movie_results' in find_res:
        tmdb_results = find_res['movie_results']
    elif 'results' in find_res:
        tmdb_results = find_res['results']
        
    for result in tmdb_results:
        if(result['original_title'] == final_row['primaryTitle']):
            moviedb_id = result['id']
            full_reviews_url = url_reviews + str(moviedb_id) + "/reviews?language=en-US&page=1"
            reviews_res = fetch_tmdb_data(full_reviews_url)
            
            reviews_results = []
            if 'results' in reviews_res:
                reviews_results = reviews_res['results']
            else:
                print("no reviews found for tmdb id: " + str(moviedb_id))
            
            for review in reviews_results:
                final_row['review'] = review['content']
                break
            
            final_row['description'] = result['overview']
            break
    
    with lock:
        with open(processed_movies_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(final_row)
            
    print("Done with " + final_row['primaryTitle'])
            
if __name__ == "__main__":
    print("starting moviedb ingestion...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        rows_to_parse = {executor.submit(parse_row, row): row for row in rows}
        for future in concurrent.futures.as_completed(rows_to_parse):
            movie = rows_to_parse[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (movie, exc))
            else:
                print("done with movie: ")
                print(movie)
        
    end_time = time.time()
    print(f'tmdb ingestion complete in {end_time - start_time} seconds.')