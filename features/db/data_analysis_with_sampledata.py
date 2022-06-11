#!/usr/bin/python3

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
from konlpy.tag import Okt
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

warnings.filterwarnings('ignore')

df = pd.read_csv("https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/tripadviser_review.csv") # 데이터 불러오기 - sample data
'''
#데이터 살펴보기
#print(df.head())
#print(df.shape) # 차원 확인
#print(df.isnull().sum()) # 결측치 확인
#print(df.info()) # information
#print(df['text'][0])
#print(df['text'][100])

# 데이터 전처리
def apply_regular_expression(text):
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')  # 한글 추출 규칙: 띄어 쓰기(1 개)를 포함한 한글
    result = hangul.sub('', text)  # 위에 설정한 "hangul"규칙을 "text"에 적용(.sub)시킴
    return result
#print(apply_regular_expression(df['text'][0])) # example

# 명사 형태소 추출 함수
okt = Okt()  
#nouns = okt.nouns(apply_regular_expression(df['text'][0])) # example
#print(nouns)

# 말뭉치 생성
corpus = "".join(df['text'].tolist())
#print(corpus) # example

# 정규 표현식 적용
#apply_regular_expression(corpus)

# 전체 말뭉치(corpus)에서 명사 형태소 추출
nouns = okt.nouns(apply_regular_expression(corpus))
#print(nouns)

# 빈도 탐색
counter = Counter(nouns)
#print(counter.most_common(10))

# 한글자 명사 제거
available_counter = Counter({x: counter[x] for x in counter if len(x) > 1})
#print(available_counter.most_common(10))
'''
# 불용어 사전
stopwords = pd.read_csv("https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt").values.tolist()
#print(stopwords[:10])
'''
# 관련 불용어 손수 추가 - 예제 데이터 관련 -> 유투브 동영상 하나하나 다 해줄 수 없을 것 같아서 생략
#jeju_hotel_stopwords = ['제주', '제주도', '호텔', '리뷰', '숙소', '여행', '트립']
#for word in jeju_hotel_stopwords:
#    stopwords.append(word)
'''
def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')  # 정규 표현식 처리
    result = hangul.sub('', text)
    okt = Okt()  # 형태소 추출
    nouns = okt.nouns(result)
    nouns = [x for x in nouns if len(x) > 1]  # 한글자 키워드 제거
    nouns = [x for x in nouns if x not in stopwords]  # 불용어 제거
    return nouns

vect = CountVectorizer(tokenizer = lambda x: text_cleaning(x))
bow_vect = vect.fit_transform(df['text'].tolist())
word_list = vect.get_feature_names()
count_list = bow_vect.toarray().sum(axis=0)
#print(word_list)
#print(count_list)
'''
# 각 단어의 리뷰별 등장 횟수
#print(bow_vect.toarray())
# "단어" - "총 등장 횟수" Matching
word_count_dict = dict(zip(word_list, count_list))
#print(word_count_dict)
'''
# TF-IDF
tfidf_vectorizer = TfidfTransformer()
tf_idf_vect = tfidf_vectorizer.fit_transform(bow_vect)
#print(tf_idf_vect.shape)
'''
# 첫 번째 리뷰에서의 단어 중요도(TF-IDF 값) -- 0이 아닌 것만 출력
#print(tf_idf_vect[0])
# 첫 번째 리뷰에서 모든 단어의 중요도 -- 0인 값까지 포함
#print(tf_idf_vect[0].toarray().shape)
#print(tf_idf_vect[0].toarray())
'''
#벡터 - 단어 mapping
#print(vect.vocabulary_)
invert_index_vectorizer = {v: k for k, v in vect.vocabulary_.items()}
#print(str(invert_index_vectorizer)[:100]+'...')

# 데이터셋 생성 1/0
def rating_to_label(rating): # 여기서는 평점이 5점 만점에 3점 이상이면 1, 아니면 0으로 함 -> 유튜브 댓글에는 수정 필요(댓글의 좋아요가 상위 30~50%인 경우 1, 아니면 0?)
    if rating > 3:
        return 1
    else:
        return 0
    
df['y'] = df['rating'].apply(lambda x: rating_to_label(x))
#print(df.head())
#print(df["y"].value_counts())
'''
x = tf_idf_vect
y = df['y']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=1)

# model traning
# fit in training set
lr = LogisticRegression(random_state = 0)
lr.fit(x_train, y_train)

# predict in test set
y_pred = lr.predict(x_test)

# classification result for test set
#print('accuracy: %.2f' % accuracy_score(y_test, y_pred))
#print('precision: %.2f' % precision_score(y_test, y_pred))
#print('recall: %.2f' % recall_score(y_test, y_pred))
#print('F1: %.2f' % f1_score(y_test, y_pred))
'''
# sampling 재조정
positive_random_idx = df[df['y']==1].sample(275, random_state=12).index.tolist()
negative_random_idx = df[df['y']==0].sample(275, random_state=12).index.tolist()

random_idx = positive_random_idx + negative_random_idx
x = tf_idf_vect[random_idx]
y = df['y'][random_idx]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=1)

#모델 재학습
lr2 = LogisticRegression(random_state = 0)
lr2.fit(x_train, y_train)
y_pred = lr2.predict(x_test)

# classification result for test set
#print('accuracy: %.2f' % accuracy_score(y_test, y_pred))
#print('precision: %.2f' % precision_score(y_test, y_pred))
#print('recall: %.2f' % recall_score(y_test, y_pred))
#print('F1: %.2f' % f1_score(y_test, y_pred))

# 긍정/부정 분석
coef_pos_index = sorted(((value, index) for index, value in enumerate(lr2.coef_[0])), reverse = True)
coef_neg_index = sorted(((value, index) for index, value in enumerate(lr2.coef_[0])), reverse = False)

# enumerate: 인덱스 번호와 컬렉션의 원소를 tuple형태로 반환함
invert_index_vectorizer = {v: k for k, v in vect.vocabulary_.items()}
#print(invert_index_vectorizer) total?
#긍정, 부정 단어 10개씩 출력
print('positive')
for coef in coef_pos_index[:10]:
    print(invert_index_vectorizer[coef[1]], coef[0])
print('negative')
for coef in coef_neg_index[:10]:
    print(invert_index_vectorizer[coef[1]], coef[0])
