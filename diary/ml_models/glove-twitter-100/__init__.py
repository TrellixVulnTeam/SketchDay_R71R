import os 
from gensim.models import KeyedVectors
from gensim.downloader import base_dir


def load_data():
    path = os.path.join(base_dir, 'glove-twitter-100', 'glove-twitter-100.gz')
    model = KeyedVectors.load_word2vec_format(path)
    return model
