'''#!/usr/bin/python3'''
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class Wordcloud:
    def __init__(self, pdata=None, ndata=None):
        self.pdata = pdata
        self.ndata = ndata

    def makeWordCloud(self):
        okt = Okt()

        positive_data = list()
        negative_data = list()

        for word in self.pdata:
            result = okt.pos(word)
            for word, tag in result:
                if tag in ['Noun', 'Adjective']:
                    positive_data.append(word)

        for word in self.ndata:
            result = okt.pos(word)
            for word, tag in result:
                if tag in ['Noun', 'Adjective']:
                    negative_data.append(word)

        # 긍정 단어 중 가장 많이 나온 단어부터 40개를 저장한다.
        pcounts = Counter(positive_data)
        ptags = pcounts.most_common(40)
        print('Tag: ',dict(ptags))
        
        # 부정 단어 중 가장 많이 나온 단어부터 40개를 저장한다.
        ncounts = Counter(positive_data)
        ntags = ncounts.most_common(40)
        print('Tag: ',dict(ntags))
        
        # WordCloud를 생성한다.
        img = Image.open('C:/Users/user/Desktop/OSP Final TP/features/Data_process/Hear shape.png')
        mask_arr = np.array(img)

        wc = WordCloud(font_path='{Font Path}',background_color="white",width=700,height=700,random_state=42,mask=mask_arr)
        pcloud = wc.generate_from_frequencies(dict(ptags))
        ncloud = wc.generate_from_frequencies(dict(ntags))

        # 생성된 WordCloud를 test.jpg로 보낸다.
        pcloud.to_file('features/Crawling/positive.jpg')
        ncloud.to_file('features/Crawling/negative.jpg')
        # plt.figure(figsize=(10, 8))
        # plt.axis('off')
        # plt.imshow(cloud)
        # plt.show()

if __name__=='__main__':
    print('Testing start...')
    # ...
    wordT = Wordcloud(pdata=None, ndata=None)
    wordT.makeWordCloud()