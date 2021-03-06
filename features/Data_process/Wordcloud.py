#!/usr/bin/python3
#-*- coding: utf-8 -*-
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
from PIL import Image
import numpy as np
import os

class Wordcloud:
    def __init__(self, data=None, dtype='pos'):
        ''' Word data 저장'''
        self.words = data
        self.imgPath = os.path.abspath(os.curdir).replace('\\','/') + '/static/images'
        self.fontPath = os.path.abspath(os.curdir).replace('\\','/') + '/features/Fonts'
        if dtype == 'pos':
            self.fontCol = 'spring'
        elif dtype == 'neg':
            self.fontCol = 'PuBu'

    def makeWordCloud(self, index):
        okt = Okt()

        noun_adj_data = list()

        # 저장된 Word data의 형태소 분석 및 명사, 형용사 단어만 저장
        for word in self.words:
            result = okt.pos(word)
            for word, tag in result:
                if tag in ['Noun', 'Adjective']:
                    noun_adj_data.append(word)
        
        # 가장 많이 나온 단어 기준, 상위 40개 저장
        counts = Counter(noun_adj_data)
        tags = counts.most_common(40)
        print('Tag: ',dict(tags))

        # WordCloud 생성
        img = Image.open(self.imgPath+'/heart.png')
        mask_arr = np.array(img)

        wc = WordCloud(font_path=self.fontPath+'/ADOBEGOTHICSTD-BOLD.OTF',background_color="white",width=700,height=700,random_state=42,mask=mask_arr, colormap=self.fontCol)
        cloud = wc.generate_from_frequencies(dict(tags))

        # 생성된 WordCloud를 이미지 파일로 따로 저장
        cloud.to_file(self.imgPath + '/wordcloud' + str(index) +'.png')
        # Wordcloud 결과 보기
        # plt.figure(figsize=(10, 8))
        # plt.axis('off')
        # plt.imshow(cloud)
        # plt.show()
        return '/wordcloud' + str(index) +'.png'

if __name__=='__main__':
    print('Testing start...')
    # data = ['안녕','반가워','하이','바이','헬로우','누구','나야','테스트','아니','맞아','카드','리딘','김','현','지','이','연','수','반가워','헬로우','반가워','안녕']
    # wordT = Wordcloud(data=data)
    # wordT.makeWordCloud()
