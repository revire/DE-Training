"""Add additional filtering by genre.
Multiple genres (like "Comedy" and "Adventure") can be passed an input,
in this case both should be found in a movie."""


import psycopg2
import sys

from .de_training_database import connect, close, clean_string


def get_by_genre(string):
    query = clean_string(string)
    con, cur = connect('de_training', DBNAME, USER, PASSWORD, HOST)
    print(query)
    cur.execute('''
       select
          movie_title, genres, imdb_score
       from movie_metadata
       where to_tsvector(genres) @@ to_tsquery(replace(%s, ' ', '&'))
       order by imdb_score desc limit 5;
    ''', (query, ))

    res = list(cur)
    print(*res)
    close(con, cur)


def main():
    query = sys.argv[0]
    get_by_genre(query)


if __name__ == '__main__':

    main()