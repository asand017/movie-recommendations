# movie recommendations
Movie Recommendation System

Objective: The system will provide personalized movie recommendations based on user preferences and viewing history.

## How to run: (assumes docker is installed on host machine)
$ cd movie-recommendations && ./clean_start.sh

## Generating movie data

* 'collect_data.py' will write imdb dataset data to csv in data/raw/ folder
* 'moviedb_ingest.py' will write post-appended imdb csv data with descriptions and reviews if available from TMDB (the movie database)
* docker job 'docker-ingest' will push processed data to recommender db


## Development issues
1. gathering data (rottentomatoes.com blocking crawler, writing data to database despite computational limitations of docker containers - too many connection pools while threading, api rate limit issues when calling tmdb api) Soln - for the remaining items, call tmdb from the front end to get a movie's poster and backdrop if not in db, or write a new script to skip rows that have a value already. This way we don't make too many api calls.
