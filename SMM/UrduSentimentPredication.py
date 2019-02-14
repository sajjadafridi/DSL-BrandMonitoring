import re
import numpy as np
import pandas as pd
from keras.layers import Embedding, Dense, Input, Conv1D, MaxPool1D, Concatenate, Flatten, Dropout
from keras.models import Model, load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from sklearn.metrics import *
import nltk
from sklearn.model_selection import train_test_split

from setmoke.Util import getBasePath
from setmoke.sentiment_urdu.utilities import preprocessing as preprocess
texts=[]
labels=[]
np.random.seed(1337)
maxlen = 6  # max words in a sentence
max_words = 5750  # max unique words in the dataset
embedding_dim = 300


def predOnData(data):
    '''
    This function will done the prediction on the data
        :param data: (string) sentences for which the system will perform the prediction
        :return: result: (string) labels for sentences
    '''
    temp1, temp2, tokenizer = preprocess(texts, labels)
    stopwords = open(getBasePath() + "/sentiment_urdu/data/Dataset/stop words_ur", encoding='utf-8').read()
    model = load_model(getBasePath() + '/sentiment_urdu/data/models/model')
    model.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['acc'])
    result = []
    for i in range(len(data)):
        tokens = nltk.wordpunct_tokenize(data[i])
        words = [word for word in tokens if not word in stopwords]
        seq = tokenizer.texts_to_sequences(words)
        words = pad_sequences(seq, maxlen=maxlen)
        y_pred = model.predict(words)
        pos, neg, neu = 0, 0, 0
        for x in y_pred.argmax(axis=1):
            if x == 1:
                pos = pos + 1
            if x == 0:
                neg = neg + 1
            if x == 2:
                neu = neu + 1
        if pos > neg:
            result.append('Positive')
        elif pos < neg:
            result.append('Negative')
        elif pos == neg:
            result.append('Neutral')
    return result


def loadData():
    '''
    This function will load the sentiment data create lists from each word in the data and its corresponding label
        :returns: list of all the words of corpus labels and labels of each words
        :rtype: list,list
    '''

    import os
    question_Dataset = getBasePath() + '/sentiment_urdu/data/Dataset'
    positive = []
    negative = []
    neutral = []

    for fname in os.listdir(question_Dataset):
        if fname[-3:] == 'neg':
            f = open(os.path.join(question_Dataset, fname))
            for line in f:
                texts.append(line)
                negative.append(line)
                labels.append(0)
            f.close()
        if fname[-3:] == 'pos':
            f = open(os.path.join(question_Dataset, fname))
            for line in f:
                texts.append(line)
                positive.append(line)
                labels.append(1)
            f.close()
        if fname[-4:] == '.neu':
            f = open(os.path.join(question_Dataset, fname))
            for line in f:
                texts.append(line)
                neutral.append(line)
                labels.append(2)
            f.close()