"""Add additional filtering by genre.
Multiple genres (like "Comedy" and "Adventure") can be passed an input,
in this case both should be found in a movie."""


import psycopg2
import re
import sys

# from .de_training_database import connect, close, clean_string

DBNAME=
USER=
PASSWORD=
HOST=



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
    print(query)
    cur.execute('''
       select
          movie_title, actor_1_name, genres, imdb_score
       from movie_metadata
       where to_tsvector(genres) @@ to_tsquery(replace(%s, ' ', '&'))
       order by imdb_score desc limit 5;
    ''', (query, ))

    movies = list(cur)
    print(*movies)
    close(con, cur)


def main():
    query = sys.argv[1]
    get_by_genre(query)


if __name__ == '__main__':

    main()