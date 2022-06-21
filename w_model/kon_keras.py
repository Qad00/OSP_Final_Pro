#!/usr/bin/python3
from tensorflow import keras
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics
from konlpy.tag import Okt
import json
import os

okt = Okt()


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
    # JSON 파일로 저장
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")

tokens = [t for d in train_docs for t in d[0]]
print(len(tokens))

import nltk

text = nltk.Text(tokens, name='NMSC')

# 시간이 꽤 걸립니다! 시간을 절약하고 싶으면 most_common의 매개변수를 줄여보세요.
selected_words = [f[0] for f in text.vocab().most_common(2000)]


def term_frequency(doc):
    return [doc.count(word) for word in selected_words]


train_x = [term_frequency(d) for d, _ in train_docs]
train_y = [c for _, c in train_docs]

import numpy as np

x_train = np.asarray(train_x).astype('float32')
y_train = np.asarray(train_y).astype('float32')

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(2000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=0.001),
              loss=losses.binary_crossentropy,
              metrics=[metrics.binary_accuracy])

model.fit(x_train, y_train, epochs=100, batch_size=512)
model.save(os.path.abspath(os.curdir) + '/w_model/pos_neg_model.h5')


def predict_pos_neg(review):
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if (score > 0.5):
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(review, score * 100))
    else:
        print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^;\n".format(review, (1 - score) * 100))

    return score
