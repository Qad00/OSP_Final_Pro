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
from urllib.request import urlretrieve
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
warnings.filterwarnings('ignore')

df = pd.read_csv("./youtube_title.csv") # 데이터 불러오기 - sample data
print("original data")
print(df.head())

# 불용어 사전
stopwords = pd.read_csv("https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt").values.tolist()

def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')  # 정규 표현식 처리
    result = hangul.sub('', text)
    okt = Okt()  # 형태소 추출
    nouns = okt.nouns(result)
    nouns = [x for x in nouns if len(x) > 1]  # 한글자 키워드 제거
    nouns = [x for x in nouns if x not in stopwords]  # 불용어 제거
    return nouns
#test code    
#print(text_cleaning(df.iloc[3,0]))

vect = CountVectorizer(tokenizer = lambda x: text_cleaning(x))
bow_vect = vect.fit_transform(df.iloc[:,0].tolist())
word_list = vect.get_feature_names()
count_list = bow_vect.toarray().sum(axis=0)
print("data analysis - 1 : 긍정 -1 : 부정 0 : 중립")
print(word_list)
print(count_list)

neg=pd.read_csv("./neg_pol_word.csv",sep='\t')
pos=pd.read_csv("./pos_pol_word.csv",sep='\t')

np=[0 for i in range(len(word_list))]
for i in range(len(word_list)):
	for j in range(len(neg.iloc[15:,0])):
		if neg.iloc[j+15,0] == word_list[i]:
			np[i]=-1
			break
	for j in range(len(pos.iloc[15:,0])):
		if pos.iloc[j+15,0] == word_list[i]:
			np[i]=1
			break
print(np)
