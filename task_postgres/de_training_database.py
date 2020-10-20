# Homework
# • Install Postgres database
# • Download csv file from

# • Write a program which takes some string as an input
# and performs search by title over movie database.
# Search should work for partial match, be case insensitive and should
# cover different word forms, like for "big heroes" input, "Big Hero 6" movie should be found.
# For each found movie, display its title, main actor, genres and imdb_score. Sort results by imdb_score.

# • Add additional filtering by genre.
# Multiple genres (like "Comedy" and "Adventure") can be passed an input,
# in this case both should be found in a movie.


import csv
import requests
import psycopg2
from psycopg2 import sql
import re

# • Write a program in any language which loads data (only needed fields)
# from this file into some table in efficient manner

def get_dataset_from_url(url):
    # url = 'https://raw.githubusercontent.com/Godoy/imdb-5000-movie-dataset/master/data/movie_metadata.csv'
    data = requests.get(url)
    list_of_movies_raw = list(csv.reader(data.content.decode().splitlines(), delimiter=','))
    list_of_movies = []
    for movie in list_of_movies_raw:
        if movie not in list_of_movies:
            list_of_movies.append(movie)
    return list_of_movies

def connect_postgres():
    pass

def create_databse():
    connect_postgres()
    creating new base


pos = psycopg2.connect()
pos_cur = pos.cursor()
dbname = 'de_training'
pos.set_isolation_level(0)
pos_cur.execute(sql.SQL("create database {}").format(sql.Identifier(dbname)))
pos_cur.close()
pos.close()


con = psycopg2.connect()
cur = con.cursor()
# print (con.get_dsn_parameters(),"\n")

cur.execute('''
    create table if not exists movie_metadata (
        id serial,
        color text,
        director_name text,
        num_critic_for_reviews int,
        duration int,
        director_facebook_likes int,
        actor_3_facebook_likes int,
        actor_2_name text,
        actor_1_facebook_likes int,
        gross int,
        genres text,
        actor_1_name text,
        movie_title text,
        num_voted_users int,
        cast_total_facebook_likes int,
        actor_3_name text,
        facenumber_in_poster int,
        plot_keywords text,
        movie_imdb_link text,
        num_user_for_reviews int,
        language text,
        country text,
        content_rating text,
        budget bigint,
        title_year date,
        actor_2_facebook_likes int,
        imdb_score float,
        aspect_ratio float,
        movie_facebook_likes int,
        unique()
    )
''')
con.commit()
cur.close()
con.close()


for row in my_list[1:]:
    cur.execute('''
        insert into movie_metadata(
            color ,
            director_name ,
            num_critic_for_reviews ,
            duration ,
            director_facebook_likes ,
            actor_3_facebook_likes ,
            actor_2_name ,
            actor_1_facebook_likes ,
            gross ,
            genres ,
            actor_1_name ,
            movie_title ,
            num_voted_users ,
            cast_total_facebook_likes ,
            actor_3_name ,
            facenumber_in_poster ,
            plot_keywords ,
            movie_imdb_link ,
            num_user_for_reviews ,
            language ,
            country ,
            content_rating ,
            budget ,
            title_year ,
            actor_2_facebook_likes ,
            imdb_score ,
            aspect_ratio ,
            movie_facebook_likes
        ) values(
            nullif(%s, ''), -- color
            nullif(%s, ''), -- director_name
            nullif(%s, '')::int, -- num_critic_for_reviews
            nullif(%s, '')::int, -- duration
            nullif(%s, '')::int, -- director_facebook_likes
            nullif(%s, '')::int, -- actor_3_facebook_likes
            nullif(%s, ''), -- actor_2_name
            nullif(%s, '')::int, -- actor_1_facebook_likes
            nullif(%s, '')::int, -- gross
            nullif(%s, ''), -- genres
            nullif(%s, ''), -- actor_1_name
            nullif(trim(%s), ''), -- movie_title
            nullif(%s, '')::int, -- num_voted_users
            nullif(%s, '')::int, -- cast_total_facebook_likes
            nullif(%s, ''), -- actor_3_name
            nullif(%s, '')::int, -- facenumber_in_poster
            nullif(%s, ''), -- plot_keywords
            nullif(%s, ''), -- movie_imdb_link
            nullif(%s, '')::int, -- num_user_for_reviews
            nullif(%s, ''), -- language
            nullif(%s, ''), -- country
            nullif(%s, ''), -- content_rating
            nullif(%s, '')::bigint, -- budget
            to_date(%s::text, 'YYYY'), -- title_year
            nullif(%s, '')::int, -- actor_2_facebook_likes
            nullif(%s, '')::float, -- imdb_score
            nullif(%s, '')::float, -- aspect_ratio
            nullif(%s, '')::int -- movie_facebook_likes
        )
    ''', row)
con.commit()
cur.close()
con.close()


def clean_string(string):
    return re.sub('[^a-zA-Z0-9]+', ' ', string)


def get_film(string):
    query = clean_string(string)
    print(query)
    cur.execute('''
       select
        movie_title, genres, imdb_score
       from movie_metadata
       where to_tsvector(movie_title) @@ to_tsquery(replace(%s, ' ', '&'))
       order by imdb_score desc;
    ''', (query, ))

    res = list(cur)
    print(*res)

def get_by_genre(string):
    query = clean_string(string)
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


# get_film('big & heroes', cur)
get_by_genre('romance, comedy')


def main():





cur.close()
con.close()
