#!/usr/bin/python3
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def detScore(num): # 강한 부정(-2)부터 강한 긍정(2)로 분류 
    if num < -0.5: return -2
    elif num >= -0.5 and num < 0:  return -1
    elif num == 0.0: return 0
    elif num > 0 and num <= 0.5: return 1
    else: return 2
   
df = pd.read_csv("./youtube_title.csv") # 데이터 불러오기 - sample data
sia = SentimentIntensityAnalyzer()
col_list =['score', 'predict', 'comments']
comments=[]
for i in range(len(df)):
	comments.append(['','',df.iloc[i,0]])
comments_list = pd.DataFrame(comments, columns=col_list)
for index, row in comments_list.iterrows():
    row['score'] = sia.polarity_scores(row['comments'])['compound']
comments_list['predict'] = comments_list.score.apply(detScore)
print(comments_list)
