#!/usr/bin/python

import sys
from elasticsearch import Elasticsearch

es_host ="http://localhost:9200"
es = Elasticsearch(es_host)

def search_list(word,result): # word : string, result : dict
	e1={ word:result
	   }
	return e1


def url_result(url,title,image,hits,good,num,pn,p_percent,p_word,n_word,file_path): 
# url : 유투브 링크, title : 유투브 제목, image : 썸네일, hits : 조회수, good : 좋아요, num : 분석 결과 개수, pn : 긍정인지 부정인지, p_percent : 긍정 퍼센트, p_word : 긍정 단어, n_word : 부정 단어, file_path : wordcloud 파일 경로
# url : string, title : string, image : string, hits : integer, good : integer, num: integer, pn : integer(0-positive/1-negetive), p_percent : integer, p_word : list, n_word : list, file_path: string
	e2={ url:{"title":title,
		  "image" : image,
		  "hits":hits,
		  "good" : good,
		  "result number": num,
	          "positive/negetive" : pn,
	          "positive percent" : p_percent,
	          "positive word": list(p_word),
	          "negetive word": list(n_word),
	          "word cloud" : file_path
	         }
	   }
	return e2

def insert(idx, i, doc): 
# idx : string, i : integer, doc : document
	res = es.index(index=idx, id=i, document=doc)
	return res

def search(idx): # all print
	query={"query":{"match_all":{}}} # index 안에 있는 모든 데이터 다 불러옴
	while True:
		try:
			docs = es.search (index=idx, body=query, size=10)
			break
		except Exception as e:
			print(1)
			continue
	for doc in docs['hits']['hits']:
		print(doc['_source'])
		
# test code
#if __name__== '__main__':
#	es = Elasticsearch(es_host)
#	e2=url_result("AA",'bbb','image',1000,50,100,1,80,[1,2,3],[4,5,6],"example")
#	print(insert('result',1,e2))
#	print(insert('search',3,search_list('ee',dict(e2))))
#	search('result')
#	search('search')
