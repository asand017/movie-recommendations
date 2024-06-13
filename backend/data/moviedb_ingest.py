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
df = pd.read_csv(movies_csv)#.head(20)
# print("sample set: ")
# print(df)

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
    # print("target columns: ")
    # print(df2.columns)
    writer = csv.writer(file)
    writer.writerow(df2.columns)

# def crawl_moviedb(file):
#     df = pd.read_csv(file)
#     url_find_movie = "https://api.themoviedb.org/3/find/"
#     url_reviews = "https://api.themoviedb.org/3/movie/"
#     tmdb_token = os.getenv('TMDB_TOKEN')
#     headers = {
#         "accept": "application/json",
#         "Authorization": "Bearer " + tmdb_token
#     }
    
#     new_df = df.copy()
#     new_df['description'] = ''
#     new_df['review'] = ''
#     for index, row in new_df.iterrows():
#         imdb_id = row['tconst']
#         full_find_url = url_find_movie + str(imdb_id) + "?external_source=imdb_id"
#         find_response = json.loads(requests.get(full_find_url, headers=headers).text)
#         # print("imdb_id: " + imdb_id)
#         results = []
#         if 'movie_results' in find_response:
#             results = find_response['movie_results']
#         elif 'results' in find_response:
#             results = find_response['results']
#         # print("find response: " + str(find_response))
#         for result in results:
#             if(result['original_title'] == row['primaryTitle']):
#                 moviedb_id = result['id']
#                 full_reviews_url = url_reviews + str(moviedb_id) + "/reviews?language=en-US&page=1"
#                 reviews_response = json.loads(requests.get(full_reviews_url, headers=headers).text)
#                 reviews_results = []
#                 if 'results' in reviews_response:
#                     reviews_results = reviews_response['results']
#                 else:
#                     print("no reviews found for tmdb id: " + str(moviedb_id))
                     
#                 for review in reviews_results:
#                     new_df.at[index, 'review'] = review['content']
#                     break
                
#                 new_df.at[index, 'description'] = result['overview']
                
#     directory = "./processed/"
#     os.makedirs(directory, exist_ok=True)
#     output = os.path.join(directory, 'movies.csv')
#     new_df.to_csv(output, index=False)
   
rows = [(index, row) for index, row in df2.iterrows()]
# print("rows:")
# print(rows)   

def fetch_tmdb_data(url):
    # headers = {
    #     "accept": "application/json",
    #     "Authorization": "Bearer " + tmdb_token
    # }
    # print(headers)
    r = requests.get(url, headers=headers)
    # print("tmdb response: ")
    # print(r.text)
    return json.loads(r.text)
    
def parse_row(row):
    final_row = row[1]
    # print("row " + str(row[0]) + ":")
    # print(final_row)
    
    final_row['description'] = ''
    final_row['review'] = ''
    imdb_id = row[1]['tconst']
    title = final_row['primaryTitle']
    url = url_find_movie + str(imdb_id) + "?external_source=imdb_id"
    # print("seeking " + title)
    
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
                # print("REVIEW::::")
                # print(review)
                # print("saving a review for " + title)
                final_row['review'] = review['content']
                break
            
            # print("saving description for " + title)
            final_row['description'] = result['overview']
            break
    
    with lock:
        # print("writing " + title + " to csv...")
        # print(final_row)
        with open(processed_movies_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(final_row)
            
    print("Done with " + final_row['primaryTitle'])
            
if __name__ == "__main__":
    # movies_csv = os.path.abspath("./raw/movies.csv")
    # crawl_moviedb(movies_csv)
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
    
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     future = executor.submit(parse_row, rows)
    #     print(future.result())
        
    end_time = time.time()
    print(f'tmdb ingestion complete in {end_time - start_time} seconds.')