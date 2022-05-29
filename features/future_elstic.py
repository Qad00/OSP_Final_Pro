#!/usr/bin/python3

import sys
from elasticsearch import Elasticsearch

es_host ="http://localhost:9200"

def search(word,result): # word : string, result : list
	e1={ word:list(result)
	   }
	return e1


def url_result(url,title,num,pn,p_percent,p_word,n_word,file_path): # url : string, title : string, num: integer, pn : integer(0-positive/1-negetive), p_percent : integer, p_word : list, n_word : list, file_path: string
	e2={ url:{"Title":title,
		  "result number": num,
	          "positive/negetive" : pn,
	          "positive percent" : p_percent,
	          "positive word": list(p_word),
	          "negetive word": list(n_word),
	          "word cloud" : file_path
	         }
	   }
	return e2;

# test code
#if __name__== '__main__':	
	#es = Elasticsearch(es_host)
	#res = es.index(index='knu', id=1, document= search('aaa',[1,2,3]))
	#print(res)
	#res = es.index(index='knu', id=2, document= url_result("AAA",'bbb',100,1,80,[1,2,3],[4,5,6],"example"))
	#print(res)
