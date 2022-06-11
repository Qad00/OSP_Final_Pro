'''#!/usr/bin/python3'''
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class Wordcloud:
    def makeWordCloud(self):
        okt = Okt()

        text = open('{Data Path}', 'r')
        line = text.readline()
        print(line)
        text.close()

        sentences_tag = list()
        sentences_tag = okt.pos(line)

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
        # plt.figure(figsize=(10, 8))
        # plt.axis('off')
        # plt.imshow(cloud)
        # plt.show()

if __name__=='__main__':
    wordT = Wordcloud()
    wordT.makeWordCloud()