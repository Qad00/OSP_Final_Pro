#!/usr/bin/python3

import sys
from elasticsearch import Elasticsearch

class Elastic_class:
    def __init__(self, es_host='http://localhost:9200'):
        self.es = Elasticsearch(es_host)

    def get_db(self):
        return self.es

    def search_list(self, word, result):  # word : string, result : dict(db1)
        e1 = {word: result}
        return e1

    # db1 : url : 유투브 링크, title : 유투브 제목, image : 썸네일, hits : 조회수, good : 좋아요
    # db2 : list
    # db3 : num : 분석 결과 개수, pn : 긍정인지 부정인지, p_percent : 긍정 퍼센트, p_word : 긍정 단어, n_word : 부정 단어, file_path : wordcloud 파일 경로

    def db1(self, url, title, image, hits, good):
        # url : 유투브 링크, title : 유투브 제목, image : 썸네일, hits : 조회수, good : 좋아요
        # url : string, title : string, image : string, hits : integer, good : integer
        e2 = {
            url: {
                "title": title,
                "img": image,
                "hits": hits,
                "likes": good,
            }
        }
        return e2;


    def db2(self, url, comments):
        # comments : 댓글, list
        e2 = {url: {"comments": comments}}
        return e2;

    def db3(self, url, num, pn, p_percent, p_word, n_word, file_path):
        # num : 분석 결과 개수, pn : 긍정인지 부정인지, p_percent : 긍정 퍼센트, p_word : 긍정 단어, n_word : 부정 단어, file_path : wordcloud 파일 경로
        # num: integer, pn : integer(0-positive/1-negetive), p_percent : integer, p_word : list, n_word : list, file_path: string
        e2 = {
            url: {
                "result number": num,
                "positive/negetive": pn,
                "positive percent": p_percent,
                "positive word": list(p_word),
                "negative word": list(n_word),
                "word cloud": file_path
            }
        }
        return e2;

    def insert(self, idx, doc):
        # idx : string, doc : document
        res = self.es.index(index=idx, document=doc, refresh=True)
        return res

    def search(self, idx, url):  # all print
        query = {"query": {"match_all": {}}}  # index 안에 있는 모든 데이터 다 불러옴
        while True:
            try:
                docs = self.es.search(index=idx, body=query, size=10)
                break
            except Exception as e:
                print(1)
                continue

        for doc in reversed(docs['hits']['hits']):
            try:
                #print(url)
                #print(doc['_source'][url])
                if url == "non":
                    return doc['_source']
                else:
                    return doc['_source'][url]
            except Exception as e:
                continue


# need testing!
# if __name__== '__main__':
#	es = Elasticsearch(es_host)
#	e2=url_result("AA",'bbb','image',1000,50,100,1,80,[1,2,3],[4,5,6],"example")
#	print(insert('result',1,e2))
#	print(insert('search',3,search_list('ee',dict(e2))))
#	search('result')
#	search('search')
