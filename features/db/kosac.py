#!/usr/bin/python3
from konlpy.tag import Kkma
import pandas as pd
import numpy as np
import warnings
import re
from konlpy.tag import Okt
from collections import Counter
from urllib.request import urlretrieve
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
warnings.filterwarnings('ignore')

def kosac(path):
	df = pd.read_csv(path) # 데이터 불러오기

	kosac = pd.read_csv("./polarity.csv")
	kkma = Kkma()
	total=df.iloc[:,0] # 댓글 가져옴
	pos={} # 긍정 단어
	neg={} # 부정 단어
	emotion=[0 for i in range(len(total))] # 감정 지수
	aa = ""
	for k in range(0, len(total)):
	    characters = "ㅋㄱ"
	    try:
	        aa = ''.join( x for x in total[k] if x not in characters)
	        data = kkma.pos(aa, join=True)
	    except:
	        data = kkma.pos(total[k], join=True)
	    #print(data)
	    count_POS = 0
	    count_NEG = 0
	    i = 0
	    while i < len(data):
	        for j in range(0, len(kosac)):
	            if data[i] == kosac.iloc[j, 0]:
	                try:
	                    if data[i+1] == kosac.iloc[j+1, 0].split(";")[1]:
	                        if data[i+2] == kosac.iloc[j+2, 0].split(";")[2]:
	                            #print(f"단어: {kosac.iloc[j+2, 0]}, 긍부정:{kosac.loc[j+2, 'max.value']}")
	                            i += 3
	                            if kosac.loc[j+2, 'max.value'] == 'POS': 
	                                count_POS += 1
	                                if data[i+2] not in pos:
	                                    pos[data[i+2]]=1
	                                else : pos[data[i+2]]=pos[data[i+2]]+1
	                            elif kosac.loc[j+2, 'max.value'] == 'NEG': 
	                                count_NEG += 1
	                                if data[i+2] not in neg:
	                                    neg[data[i+2]]=1
	                                else : neg[data[i+2]]=neg[data[i+2]]+1
	                            break
	                        else:
	                            #print(f"단어: {kosac.iloc[j+1, 0]}, 긍부정:{kosac.loc[j+1, 'max.value']}")
	                            i += 2
	                            if kosac.loc[j+1, 'max.value'] == 'POS': 
	                                count_POS += 1
	                                if data[i+2] not in pos:
	                                    pos[data[i+2]]=1
	                                else : pos[data[i+2]]=pos[data[i+2]]+1
	                            elif kosac.loc[j+1, 'max.value'] == 'NEG': 
	                                count_NEG += 1
	                                if data[i+2] not in neg:
	                                    neg[data[i+2]]=1
	                                else : neg[data[i+2]]=neg[data[i+2]]+1
	                            break
	                    else:
	                        #print(f"단어: {kosac.iloc[j, 0]}, 긍부정:{kosac.loc[j, 'max.value']}")
	                        i += 1
	                        if kosac.loc[j, 'max.value'] == 'POS': 
	                            count_POS += 1
	                            if data[i+2] not in pos:
	                                pos[data[i+2]]=1
	                            else:
	                                pos[data[i+2]]=pos[data[i+2]]+1
	                        elif kosac.loc[j, 'max.value'] == 'NEG':
	                            count_NEG += 1
	                            if data[i+2] not in neg:
	                                neg[data[i+2]]=1
	                            else :
	                                neg[data[i+2]]=neg[data[i+2]]+1
	                        break
	                except:
	                    print("",end="")
	            elif data[i] != kosac.iloc[j, 0] and j == len(kosac)-1:
	                i += 1
	    print(f"긍정개수: {count_POS}, 부정개수: {count_NEG}")
	    emotion[k]= count_POS - count_NEG
	#print(f"긍정개수: {count_POS}, 부정개수: {count_NEG}")
	pos=sorted(pos.items(),key=lambda item:item[1],reverse=True)
	neg=sorted(neg.items(),key=lambda item:item[1],reverse=True)
	print("positive") # 긍정 단어, 개수 출력
	for i in pos:
		list(i)
		word,_= str(i[0]).split('/')
		print(word+" "+str(i[1]))
	print("negative") # 부정 단어, 개수 출력
	for i in neg:
		list(i)
		word,_= str(i[0]).split('/')
		print(word+" "+str(i[1]))
