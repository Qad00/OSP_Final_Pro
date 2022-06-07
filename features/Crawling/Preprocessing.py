'''#!/usr/bin/python
#-*- coding: utf-8 -*-'''
import Crawling

class Preprocessing:
    def processData(self, data):
        for key in data.keys():
            for comment in data[key]:
                for word in comment.split(' '):
                    print(word)

if __name__=='__main__':
    # Testing
    crawling = Crawling.Crawling()
    crawling.setVComment(link='https://www.youtube.com/watch?v=8C23JB50dYI&list=RD8C23JB50dYI&start_radio=1')
    comment = crawling.getVComment()

    preprocess = Preprocessing()
    preprocess.processData(data=comment)
    crawling.closeDriver()
    print()