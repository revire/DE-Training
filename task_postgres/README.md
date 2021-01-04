# DE-Training

To start code, install Postgres and Python3

CREATE FILE db_config.py AND PASTE YOUR CREDENTIALS for database connection:
```
DBNAME=
USER=
PASSWORD=
HOST=
```

- `de_training_database.py` creates database, a table and fills it with a imdb movie dataset.
`python3 de_training.py`


- `get_movie_by_title.py` searches for movies with the given words in titles.
`python3 get_movie_by_title 'lord rings'`



- `get_movie_by_genre.py` searches for movies with the given genres in additional information.
`python3 get_movie_by_genre 'romance, adventure'`

 