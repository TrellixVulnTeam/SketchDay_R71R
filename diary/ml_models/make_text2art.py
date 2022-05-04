# 자연어 처리
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from collections import Counter

# 파파고 API
import requests


# 불용어 처리
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
stop_words = set(stopwords.words('english'))
stop_words.update(['well', 'first', 'think'])

lemmatizer = WordNetLemmatizer()
token = RegexpTokenizer('[\w]+')

prompt = "child's drawing"

def papago(text) :
    client_id = "Tw6A3Hs3oWBY6Bxa7vbo" # <-- client_id 기입
    client_secret = "ajQ2rOwLmG" # <-- client_secret 기입

    data = {'text' : text,
            'source' : 'ko',
            'target': 'en'}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)

def make_prompts(text, sentiment) :
    #변역
    text_en_papago = papago(text)

    tokens = []
    tokens.append(' '.join(word for word in text_en_papago.split() if not word in stop_words))
    # 숫자 제거
    tokens[0] = re.sub(r'[0-9]+', '', tokens[0])

    # 표제어 추출
    result_pre_lem = [token.tokenize(i) for i in tokens]
    middel_pre_lem = [r for i in result_pre_lem for r in i]
    final_lem = [lemmatizer.lemmatize(i) for i in middel_pre_lem if not i in stop_words]

    # 빈도수
    english = Counter(final_lem)
    result = english.most_common(5)
    words = [word for word, num in result]

    text = ' '.join(words) +'|' + prompt + '|' + papago(sentiment)

    return text
    