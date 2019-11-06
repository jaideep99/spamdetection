import loaddata
import collections
import pandas as pd
import numpy as np
import math
from nltk.corpus import stopwords
from nltk import PorterStemmer,word_tokenize


stopwords = stopwords.words('english')
stemmer = PorterStemmer()

total_words = 0
def ir_trim(messages):
    for i in range(len(messages)):
        text = messages[i]
        tokens = word_tokenize(text)
        tokens = [x for x in tokens if x not in stopwords and len(x)>2]
        tokens = [stemmer.stem(x) for x in tokens]
        tokens = ' '.join(tokens)
        messages[i] = tokens

    return messages


def inverted_matrix(data,gram = 1):
    global total_words
    total = collections.defaultdict(lambda : dict({'tf':0,'mOccur':0,'idf':0}))
    spam = collections.defaultdict(lambda : dict({'tf':0}))
    ham = collections.defaultdict(lambda : dict({'tf':0}))
    for i in range(len(data['text'])):
        if(i>=958):
            i=i+410
        words = word_tokenize(data['text'][i])
        total_words += len(words)
        for x in np.unique(words):
            total[x]['mOccur']+=1
        for x in words:
            total[x]['tf']+=1
            if(data['spam'][i]==1):
                spam[x]['tf']+=1
                ham[x]['tf']+=0
            else:
                spam[x]['tf']+=0
                ham[x]['tf']+=1

    for x in total:
        total[x]['idf'] = math.log(float(len(data['text']))/(total[x]['mOccur']))

    print(total)
    print(spam)
    print(ham)


data = loaddata.get_normalisedData()
data['text'] = ir_trim(data['text'])
train = data[:958].append(data[1368:2326])
test = data[958:1368].append(data[2326:2736])
# x_train,y_train,x_test,y_test = train['text'],train['spam'],test['text'],test['spam']
inverted_matrix(train)

