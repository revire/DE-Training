"""Write a program which takes some string as an input
and performs search by title over movie database.
Search should work for partial match, be case insensitive and should
cover different word forms, like for "big heroes" input, "Big Hero 6"
movie should be found. For each found movie, display its title, main actor,
genres and imdb_score. Sort results by imdb_score."""

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
    return con, cur


def close(con, cur):
    con.close()
    cur.close()


def clean_string(string):
    return re.sub('[^a-zA-Z0-9]+', ' ', string)


def get_film(query):
    con, cur = connect('de_training', USER, PASSWORD, HOST)
    query = clean_string(query)
    cur.execute('''
       select distinct
        movie_title, actor_1_name, genres, imdb_score
       from movie_metadata
       where to_tsvector(movie_title) @@ to_tsquery(replace(%s, ' ', '&'))
       order by imdb_score desc;
    ''', (query, ))

    movies = list(cur)
    close(con, cur)

    return movies


if __name__ == '__main__':
    query = ' '.join(sys.argv[1:])
    movies = get_film(query)
    for movie in movies:
        print(*movie)