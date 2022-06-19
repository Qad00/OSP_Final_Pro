'''#!/usr/bin/python3'''
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class Wordcloud:
    def __init__(self, data=None):
        self.words = data

    def makeWordCloud(self):
        okt = Okt()

        noun_adj_data = list()

        for word in self.words:
            result = okt.pos(word)
            for word, tag in result:
                if tag in ['Noun', 'Adjective']:
                    noun_adj_data.append(word)

        # 가장 많이 나온 단어부터 40개를 저장한다.
        counts = Counter(noun_adj_data)
        tags = counts.most_common(40)
        print('Tag: ',dict(tags))
        
        # WordCloud를 생성한다.
        img = Image.open('features/Data_process/heart.png')
        mask_arr = np.array(img)

        wc = WordCloud(font_path='features/Data_process/ADOBEGOTHICSTD-BOLD.otf',background_color="white",width=700,height=700,random_state=42,mask=mask_arr)
        cloud = wc.generate_from_frequencies(dict(tags))

        # 생성된 WordCloud를 test.jpg로 보낸다.
        cloud.to_file('features/Data_process/positive.jpg')
        # plt.figure(figsize=(10, 8))
        # plt.axis('off')
        # plt.imshow(cloud)
        # plt.show()

if __name__=='__main__':
    print('Testing start...')
    # ...
    data = ['안녕','반가워','하이','바이','헬로우','누구','나야','테스트','아니','맞아','카드','리딘','김','현','지','이','연','수','반가워','헬로우','반가워','안녕']
    wordT = Wordcloud(data=data)
    wordT.makeWordCloud()