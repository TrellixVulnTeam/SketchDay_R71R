from django.test import TestCase
import sqlite3
import pandas as pd
# Create your tests here.
class MLTests(TestCase):
    print('load sql')
    sql = sqlite3.connect("db.sqlite3")
    print('load df')
    a = 6
    df = pd.read_sql("SELECT vector,author_id FROM diary_diary", sql, index_col=None)
    df = df.loc[df['author_id'] != a]
    print(df.tail())