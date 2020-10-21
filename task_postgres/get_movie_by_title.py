"""Write a program which takes some string as an input
and performs search by title over movie database.
Search should work for partial match, be case insensitive and should
cover different word forms, like for "big heroes" input, "Big Hero 6"
movie should be found. For each found movie, display its title, main actor,
genres and imdb_score. Sort results by imdb_score."""


import sys

from .de_training_database import connect, close, clean_string


def get_film(query):
    con, cur = connect('de_training', USER, PASSWORD, HOST)
    query = clean_string(query)
    cur.execute('''
       select
        movie_title, actor_1_name, genres, imdb_score
       from movie_metadata
       where to_tsvector(movie_title) @@ to_tsquery(replace(%s, ' ', '&'))
       order by imdb_score desc;
    ''', (query, ))

    movies = list(cur)
    print(*movies)
    close(con, cur)

def main():
    query = sys.argv[0]
    get_film(query)


if __name__ == '__main__':

    main()