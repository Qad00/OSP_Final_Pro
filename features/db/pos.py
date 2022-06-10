#!/usr/bin/python3

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
from konlpy.tag import Okt
from collections import Counter
from urllib.request import urlretrieve
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

pos=pd.read_csv("./pos_pol_word.csv",sep='\t')
neg=pd.read_csv("./neg_pol_word.csv",sep='\t')
print(len(pos.iloc[15:,0]))
print(len(neg.iloc[15:,0]))
a=[0 for i in range(10)]
a.insert(2,1)
print(a[2])

