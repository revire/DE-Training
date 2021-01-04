"""Add additional filtering by genre.
Multiple genres (like "Comedy" and "Adventure") can be passed an input,
in this case both should be found in a movie."""

import psycopg2
import re
import sys


sys.path.append('./task_postgres')
import db_config
DBNAME= db_config.DBNAME
USER= db_config.USER
PASSWORD= db_config.PASSWORD
HOST= db_config.HOST


def connect(dbname, user, password, host):
    con = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = con.cursor()
    return (con, cur)


def close(con, cur):
    con.close()
    cur.close()


def clean_string(string):
    return re.sub('[^a-zA-Z0-9]+', ' ', string)


def get_by_genre(string):
    query = clean_string(string)
    con, cur = connect('de_training', USER, PASSWORD, HOST)
    cur.execute('''
       select distinct
          movie_title, actor_1_name, genres, imdb_score
       from movie_metadata
       where to_tsvector(genres) @@ to_tsquery(replace(%s, ' ', '&'))
       order by imdb_score desc limit 5;
    ''', (query, ))

    movies = list(cur)
    return movies

    close(con, cur)


if __name__ == '__main__':
    query = ' '.join(sys.argv[1:])
    movies = get_by_genre(query)
    for movie in movies:
        print(*movie)