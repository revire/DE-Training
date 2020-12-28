"""Install Postgres database. Download csv file from git.
Write a program in any language which loads data (only needed fields)
from this file into some table in efficient manner"""


import csv
import logging
import psycopg2
import requests
import re

# sys.path.append('./task_postgres')
# sys.path.remove('./task_postgres')
import db_config

DBNAME= db_config.DBNAME
USER= db_config.USER
PASSWORD= db_config.PASSWORD
HOST= db_config.HOST



logging.basicConfig(level=logging.INFO)

def get_list_of_movies(url):
    logging.info('Collecting dataset from url')
    data = requests.get(url)
    list_of_movies_raw = list(csv.reader(data.content.decode().splitlines(), delimiter=','))
    list_of_movies = []
    for movie in list_of_movies_raw:
        if movie not in list_of_movies:
            list_of_movies.append(movie)
    logging.info('The dataset is ready')
    return list_of_movies


def clean_string(string):
    return re.sub('[^a-zA-Z0-9]+', ' ', string)


def connect(dbname, user, password, host):
    con = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = con.cursor()
    logging.info(f'Collected to {dbname}')
    return (con, cur)


def close(con, cur):
    dbname = con.get_dsn_parameters()['dbname']
    con.close()
    cur.close()
    logging.info(f'Connection to {dbname} is closed')


def create_database(db_name):
    con, cur = connect(DBNAME, USER, PASSWORD, HOST)
    try:
        con.set_isolation_level(0)
        cur.execute(f'create database {db_name}')
    except psycopg2.errors.DuplicateDatabase:
        logging.warn('Database already exists')
    close(con, cur)


def create_movie_metadata(con, cur):
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
            movie_facebook_likes int
        )
    ''')
    con.commit()
    logging.info('Table movie_metadata is created')


def insert_movie_metadata(con, cur, list_of_movies):
    for row in list_of_movies[1:]:
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
    logging.info('Table movie_metadata is populated')


def create_base():
    list_of_movies = get_list_of_movies('https://raw.githubusercontent.com/Godoy/imdb-5000-movie-dataset/master/data/movie_metadata.csv')
    create_database('de_training')
    con, cur = connect('de_training', USER, PASSWORD, HOST)
    create_movie_metadata(con, cur)
    insert_movie_metadata(con, cur, list_of_movies)
    close(con, cur)


if __name__ == '__main__':
    create_base()




