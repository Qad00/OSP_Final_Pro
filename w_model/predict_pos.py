#!/usr/bin/python3
from tensorflow import keras
from konlpy.tag import Okt
import numpy as np
import json, os
import nltk

okt = Okt()

model = keras.models.load_model(os.path.abspath(os.curdir) + '/w_model/pos_neg_model.h5')


def read_data(filename):
    with open(filename, 'r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        # txt 파일의 헤더(id document label)는 제외하기
        data = data[1:]
    return data


train_data = read_data(os.path.abspath(os.curdir) + '/w_model/ratings_train.txt')


def tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]


if os.path.isfile('train_docs.json'):
    with open('train_docs.json') as f:
        train_docs = json.load(f)
else:
    train_docs = [(tokenize(row[1]), row[2]) for row in train_data]
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")

tokens = [t for d in train_docs for t in d[0]]

text = nltk.Text(tokens, name='NMSC')

# 시간이 꽤 걸립니다! 시간을 절약하고 싶으면 most_common의 매개변수를 줄여보세요.
selected_words = [f[0] for f in text.vocab().most_common(2000)]


def term_frequency(doc):
    return [doc.count(word) for word in selected_words]


def predict_pos_neg(com):
    token = tokenize(com)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if score > 0.5:
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(com, score * 100))
    else:
        print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^\n".format(com, (1 - score) * 100))

    return score


def get_res_result(comments):
    if len(comments) > 0:
        pos_com = {}
        neg_com = {}
        for com in comments:
            score = predict_pos_neg(com)
            if score > 0.5:
                pos_com.update({com: score})
            else:
                neg_com.update({com: score})

        num_com = len(comments)
        # sort pos_neg with highest score
        p_tmp_list = sorted(pos_com.items(), key=lambda x: x[1], reverse=True)
        sorted_pos = dict(p_tmp_list)

        n_tmp_list = sorted(neg_com.items(), key=lambda x: x[1])
        sorted_neg = dict(n_tmp_list)

        pos_per = (len(sorted_pos) * 100) / num_com
        neg_per = 100 - pos_per

        #print("Pos dic")
        #print(sorted_pos)
        #print("\n\nneg dic")
        #print(sorted_neg)
        return num_com, sorted_pos.keys(), sorted_neg.keys(), pos_per
    else:
        return 0, "None", "None", 0
