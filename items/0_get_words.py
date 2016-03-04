#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import math

term = {} #包含分词的商品总数
tf_idf_bow = {} #某商品、某分词的tf-idf值

def readItems():
    global term, tf_idf_bow
    tf_idf_bow = {}
    term = {}
    with open('../data/dim_items.txt', 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            line=line.strip('\n')
            info = line.split(' ')
            terms = info[2].split(',')
            words = set(terms)
            tf_idf_bow[info[0]] = {}
            if (len(tf_idf_bow) % 1000 == 0):
                print(len(tf_idf_bow))
            for word in words:
                if word not in term:
                    term[word] = 1
                else:
                    term[word] += 1
                tf_idf_bow[info[0]][word] = terms.count(word)*1.0/len(terms) #TF值
    for item in tf_idf_bow:
        for word in tf_idf_bow[item]:
            tf_idf_bow[item][word] *= math.log(len(tf_idf_bow)*1.0/term[word])#IDF值
    with open('../data/tf_idf_bow.dat', 'wb') as f:
        pickle.dump(tf_idf_bow, f)

if __name__=="__main__":
    readItems()
    print('read item OK!')