from django.apps import AppConfig
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim.downloader
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import joblib


class DiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diary'

    print('load song_df')
    song_df = pd.read_csv('diary/ml_models/df_vectorized_10word_100vec.csv')
    print('load recommendation_music_model')
    rec_model = joblib.load('diary/ml_models/recommendation_music_model.pkl')
    print('load word2vec')
    glove_vectors = KeyedVectors.load('diary/ml_models/glove-twitter-100')



