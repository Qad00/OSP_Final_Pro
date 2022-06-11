'''#!/usr/bin/python3
#-*- coding: utf-8 -*-'''
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
from PIL import Image
import numpy as np

class Wordcloud:
    def __init__(self):
        self.wc = None

    def makeWordCloud(self):
        okt = Okt()

        sentences_tag = list()
        sentences_tag = okt.pos()

        noun_adj_list = list()

        # tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
        for word, tag in sentences_tag:
            if tag in ['Noun' , 'Adjective']: 
                noun_adj_list.append(word)

        # 가장 많이 나온 단어부터 40개를 저장한다.
        counts = Counter(noun_adj_list)
        tags = counts.most_common(40) 
        print('Tag: ',dict(tags))
        
        # WordCloud를 생성한다.
        img = Image.open('{Image Path}')
        mask_arr = np.array(img)

        wc = WordCloud(font_path='{Font Path}',background_color="white",width=700,height=700,random_state=42,mask=mask_arr)
        cloud = wc.generate_from_frequencies(dict(tags))

        # 생성된 WordCloud를 test.jpg로 보낸다.
        cloud.to_file('features/Crawling/test.jpg')

    def getData(self):
        return self.wc

if __name__=="__main__":
    print('Testing start...')