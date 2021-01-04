import re
import pandas as pd

from nltk.stem import *
stemmer = PorterStemmer()


def clean_string(string):
    return re.sub('[^a-zA-Z0-9]+', ' ', string)


def create_movie_df(link):
    df = pd.read_csv(link)
    df['genres_stemmed'] = df['genres'].apply(lambda tokens: [stemmer.stem(token) for token in tokens.split('|')])
    df['movie_stemmed'] = df['movie_title'].apply(
        lambda tokens: [stemmer.stem(token) for token in clean_string(tokens).strip().split(' ')])
    return df


def get_movie_by_title(string, df):
    query = [stemmer.stem(token) for token in clean_string(string).strip().split(' ')]

    res = df[df['movie_stemmed'].apply(lambda tokens: sum([token in query for token in tokens]) > 0)]
    return res[['movie_title', 'actor_1_name', 'genres', 'imdb_score']]


def get_movie_by_genres(string, df):
    query = [stemmer.stem(token) for token in clean_string(string).strip().split(' ')]
    res = df[df['genres_stemmed'].apply(lambda tokens: sum([token in query for token in tokens]) > 0)]
    return res[['movie_title', 'actor_1_name', 'genres', 'imdb_score']]



