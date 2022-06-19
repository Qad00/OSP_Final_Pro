import re
from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Okt
from konlpy.tag import Komoran
import pandas as pd
from collections import Counter

stopwords = pd.read_csv(
    "https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt").values.tolist()


# function for deleting white space type chars with special chars
def clean_text(str_tmp):
    #print("\n\nStart :")
    #print(str_tmp)
    # white space
    str_tmp = str_tmp.replace("\n", " ")
    str_tmp = str_tmp.replace("\t", " ")
    str_tmp = str_tmp.replace("                 ", " ")
    str_tmp = str_tmp.strip()

    #print("\n\n str before nums : ")
    #print(str_tmp)
    # spec chars
    str_tmp = re.sub("[0-9]+", "", str_tmp)
    str_tmp = re.sub("[a-zA-Z]+", "", str_tmp)
    str_tmp = re.sub("[-=+,#/?:^$.@*\"~&%!\\'|()\[\]<>`]+", "", str_tmp)

    #rint("\n\n str after nums : ")
    #print(str_tmp)

    # korean spec chars
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')  # 한글 추출 규칙: 띄어 쓰기(1 개)를 포함한 한글
    result = hangul.sub('', str_tmp)  # 위에 설정한 "hangul"규칙을 "text"에 적용(.sub)시킴

    #print("\nstr_tmp after : ")
    #print(result)

    okt = Okt()
    nouns = okt.nouns(result)
    #print("\n\nNouns ")
    #print(nouns)

    # remove 1 letter word
    nouns = [x for x in nouns if len(x) > 1]
    #print("\n\nAfter removing 1 letter words")
    #print(nouns)

    # removing stopwords
    #rint("/n/n checking stopwords")
    #print(stopwords[:10])

    nouns = [x for x in nouns if x not in stopwords]
    #print("\n\n Nouns after removing stopwords\n\n")

    return nouns


def classify_sentences(data):
    return data.split('\n')


def classify_words(result):
    okt = Okt()
    nouns = okt.nouns(result)
    #print("\n\nNouns ")
    #print(nouns)

    # remove 1 letter word
    nouns = [x for x in nouns if len(x) > 1]
    #print("\n\nAfter removing 1 letter words")
    #print(nouns)

    # removing stopwords
    #print("/n/n checking stopwords")
    #print(stopwords[:10])

    nouns = [x for x in nouns if x not in stopwords]
    #print("\n\n Nouns after removing stopwords\n\n")

    return nouns


def count_word_fre(words):
    counter = Counter(words)
    available_counter = Counter({x: counter[x] for x in counter if len(x) > 1})
    return available_counter


def word_count_vector(data):
    vect = CountVectorizer(tokenizer=lambda x: clean_text(x))
    bow_vect = vect.fit_transform(data)
    word_list = vect.get_feature_names_out()
    count_list = bow_vect.toarray().sum(axis=0)

    word_count_dict = dict(zip(word_list, count_list))
    print("\nlist length : ", len(word_list))
    print("Word List:")
    print(word_list)
    return word_count_dict


def text_preprocess(x):
    text = []
    a = re.sub('[\n\ta-zA-Z]+', ' ', x)
    a = re.sub("[-=+,#/?;:^.$@*\"~&%!\\'|()\[\]<>_`]+", " ", a)
    a = re.sub("[0-9]+", " ", a)
    # korean spec chars
    #hangul = re.compile('[^가-힣]')  # 한글 추출 규칙: 띄어 쓰기(1 개)를 포함한 한글
    #a = hangul.sub(' ', a)  # 위에 설정한 "hangul"규칙을 "text"에 적용(.sub)시킴
    #for i in a.split():
    #    text.append(i)
    #return ' '.join(text)
    return a

def tokenize(x):
    okt = Okt()
    #twitter = Twitter()
    text = []
    tokens = okt.pos(x)
    #tokens = twitter.pos(x)
    for token in tokens:
        if token[1] == 'Adjective' or token[1] == 'Adverb' or token[1] == 'Determiner' or token[1] == 'Noun' or token[
            1] == 'Verb':
            text.append(token[0])

    return text


def remove_stopwords(words):
    without_stopwords = [x for x in words if x not in stopwords]
    longer_words = [x for x in without_stopwords if len(x) > 1]
    # return without_stopwords
    return longer_words
