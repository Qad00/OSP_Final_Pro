#!/usr/bin/python
#-*- coding: utf-8 -*-
from tqdm import tqdm
import re

class Preprocessing:
    def __init__(self):
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
        self.token = ' \n~`!@#$%^&*()?/<>,.:;\'"{}[]-_=+abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def chatToSentence(self, data: list):
        ''' data: crawled comment data'''
        
        print("Make Sentences...")
        self.sentences = list()
        for idx, key in enumerate(data.keys()):
            print(f'Link[{idx+1}] processing...')
            for comment in tqdm(data[key]):
                for sentence in comment.split('\n'):
                    sentence = sentence.strip(self.token)
                    if sentence:
                        self.sentences.append(sentence)
        print('Done.')
    
    def sentenceToWord(self, data: list):
        ''' data: may be several sentence data or preprocessed sentence data'''
        
        print('Make Words...')
        self.words = list()
        for sentence in tqdm(data):
            for word in sentence.split(' '):
                # Delete Emoticons
                word = self.emoticon.sub(r'',word)
                # Delete Special Characters, Alphabets, Numbers
                word = word.strip(self.token)
                # Store the word
                if word:
                    self.words.append(word)
        print('Done.')
    
    def getWord(self):
        return self.words
        
    def getSentence(self):
        return self.sentences

if __name__=='__main__':
    print('Testing Start...')
    # preTool = Preprocessing()
    # keyword = ['Sinseoyugi','klsdjfklsdajflksjadlkfjsdlafjlasdjf;klas','로로로로로로롤']
    # preTool.sentenceToWord(data=keyword)
    # print(preTool.getWord())
