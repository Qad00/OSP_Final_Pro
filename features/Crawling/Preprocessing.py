'''#!/usr/bin/python
#-*- coding: utf-8 -*-'''
from Crawling import Crawling

class Preprocessing:
    def __init__(self):
        self.token = ' \n~`!@#$%^&*()?/<>,.:;\'"{}[]-_=+'
        self.emoji = ''

    def processData(self, data):
        print("Preprocess Start...")
        for key in data.keys():
            for comment in data[key]:
                for word in comment.split(' '):
                    print('Origin:\t\t',word)
                    print('Processed:\t',word.strip(self.token))

if __name__=='__main__':
    # Testing
    crawling = Crawling()
    crawling.setVComment(link='https://www.youtube.com/watch?v=8C23JB50dYI&list=RD8C23JB50dYI&start_radio=1')
    comment = crawling.getVComment()
    print("Done.")
    preprocess = Preprocessing()
    preprocess.processData(data=comment)
    crawling.closeDriver()
    print()