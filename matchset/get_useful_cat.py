#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pickle
import random

INPUTNAME = "matchset_"
OUTPUTNAME = 'cat_match_rate_'
cat_match_rate = {} #match degree of terms，not used

global cat_match_count, item_info
cat_match_count = {}

item_info = {}

def addToMatchCount(match_set):
    global cat_match_count, item_info
    for i in range(len(match_set)):
        for j in range(len(match_set)):
            if i == j:
                continue
            for ki in range(len(match_set[i])):
                for kj in range(len(match_set[j])):
                    cat1 = item_info[match_set[i][ki]] # feature of item match_set[i][ki]
                    cat2 = item_info[match_set[j][kj]] # feature of item match_set[j][kj]
                    if cat1 not in cat_match_count:
                        cat_match_count[cat1] = {}
                    if cat2 not in cat_match_count[cat1]:
                        cat_match_count[cat1][cat2] = 1
                    else:
                        cat_match_count[cat1][cat2] += 1


def calMatch():
    global cat_match_count, item_info
    filename = 'dim_fashion_matchsets.txt'
    cnt = 0
    with open(filename, 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            line=line.strip('\n')
            ms = line.split(' ')[1]
            match_set = ms.split(';')
            for i in range(len(match_set)):
                items = match_set[i]
                match_set[i] = items.split(',')
            #get each two items and add to the match rate
            cnt += 1
            print('match_set no. ', cnt)
            addToMatchCount(match_set)

def readItems():
    global cat_match_count, item_info
    filename = 'dim_items.txt'
    with open(filename, 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            line=line.strip('\n')
            info = line.split(' ')
            item_info[info[0]] = info[1] #only save cat

def printResult():
    with open('cat_match_all.txt', 'w') as f:
        for cat1 in cat_match_count:
            for cat2 in cat_match_count[cat1]:
                f.write("%s %s %s\n" %(cat1,cat2,cat_match_count[cat1][cat2]))
    with open('cat_match_all.dat', 'wb') as f:
        pickle.dump(cat_match_count, f)

if __name__=="__main__":
    readItems()
    print('read item OK!')
    calMatch()
    print('calculate match OK!')

    printResult()
    print('solve OK!')
    