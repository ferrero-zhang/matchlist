#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import random
import datetime

INPUTNAME = "matchset_"
OUTPUTNAME = 'term_match_rate_'
ANSRATE = 'ans_history_rate_'

global item_info,test_item_similar,item_match_rate,match_item

item_info = {}
item_match_rate = {}
test_item_similar = {}
match_item = []

def readItems():
    global item_info,item_match_rate
    with open('dim_items.dat', 'rb') as f:
        item_info = pickle.load(f)

def readRate():
    global item_info,item_match_rate,match_item
    match_item = []
    with open('match_item.txt', 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            line=line.strip('\n')
            match_item += [line]


def diffItem(item1, item2): #item1为预测商品，item2为匹配商品
    global item_info,item_match_rate
    # if item_info[item1][0] == item_info[item2][0]:
    #     cat = 1
    # else:
    #     cat = 0
    # term = 0
    a_list = item_info[item1][1]
    b_list = item_info[item2][1]
    ret_list = list((set(a_list).union(set(b_list)))^(set(a_list)^set(b_list)))
    bing_list = list(set(a_list).union(set(b_list)))
    # for x in item_info[item1][1]:
    #     if x in item_info[item2][1]:
    #         term += 1
    term = len(ret_list) * 1.0 / len(bing_list)
    # res = cat * 0.4 + term * 0.6
    return term

def calTestItemSimilarity():
    global item_info,test_item_similar,item_match_rate,match_item

    test_item_similar = {}
    with open('test_items.txt', 'r') as f2:
        cnt = 0
        while 1:
            line = f2.readline()
            if not line:
                break
            line=line.strip('\n')

            test_item_similar[line] = {}
            matcnt = 0
            mmin = 10000000000.0
            for item in match_item:
                if item_info[item][0] != item_info[line][0]:
                    continue
                simi = diffItem(line, item)
                if matcnt==0 or simi>0.1:
                    matcnt += 1
                    test_item_similar[line][item] = simi
                    #mmin = min(mmin, simi)
            cnt += 1
            print(cnt, matcnt)

if __name__=="__main__":
    readItems()
    readRate()
    print('pre read OK!')

    calTestItemSimilarity()
    print('calculate similarity OK!')

    global item_info,test_item_similar,item_match_rate
    with open('test_item_similar_all.dat', 'wb') as f:
        pickle.dump(test_item_similar, f)
