#!/usr/bin/python
#-*- coding: utf-8 -*-
from Crawling import Crawling
from tqdm import tqdm
import re

class Preprocessing:
    def __init__(self):
        self.token = ' \n~`!@#$%^&*()?/<>,.:;\'"{}[]-_=+'
        self.emoticon = re.compile('['
            u"\U00002700-\U000027BF"    # Dingbats
            u"\U0001F600-\U0001F64F"    # Emoticons
            u"\U00002600-\U000026FF"    # Miscellaneous Symbols
            u"\U0001F300-\U0001F5FF"    # Miscellaneous Symbols & Pictographs
            u"\U0001F900-\U0001F9FF"    # Supplemental Symbols & Pictographs
            u"\U0001FA70-\U0001FAFF"    # Symbols & Pictographs Extended-A
            u"\U0001F680-\U0001F6FF"    # Transport & Map Symbols
            u"\U0001F1E0-\U0001F1FF"    # Flags (iOS)
        ']+', flags=re.UNICODE)
        self.alphabet = re.compile('['
            u"\U00000041-\U0000005A"    # Big Alphabet
            u"\U00000061-\U0000007A"    # Small Alphabet
        ']+', flags=re.UNICODE)

    def processData(self, data):
        print("Preprocess Start...")
        print("Make Sentences...")
        self.sentences = list()
        for idx, key in enumerate(data.keys()):
            print(f'Link[{idx+1}] processing...')
            for comment in tqdm(data[key]):
                for sentence in comment.split('\n'):
                    self.sentences.append(sentence.strip(self.token))

        print('\nMake Words...')
        self.words = list()
        for sentence in tqdm(self.sentences):
            for word in sentence.split(' '):
                self.words.append(self.emoticon.sub(r'',word).strip(self.token))
    
    def getData(self):
        return self.words

if __name__=='__main__':
    print('Testing Start...')