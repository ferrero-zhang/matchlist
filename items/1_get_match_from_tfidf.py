#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import math

tf_idf_bow = {} #某商品、某分词的tf-idf值
identity_items = {}
cat_match = {}
item_info = {}

def readItems():
    global tf_idf_bow, item_info
    with open('tf_idf_bow.dat', 'rb') as f:
        tf_idf_bow = pickle.load(f)

    item_info = {}
    with open('dim_items.txt', 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            line=line.strip('\n')
            info = line.split(' ')
            item_info[info[0]] = info[1] #记录商品分类cat

def readCatMatch():
    global cat_match
    with open('cat_match_sm.dat', 'rb') as f:
        cat_match = pickle.load(f)

def calSimi(item1, item2):
    v1 = tf_idf_bow[item1]
    v2 = tf_idf_bow[item2]
    res = 0.0
    fenmu1 = 0.0
    for x in v1:
        fenmu1 += v1[x]*v1[x]
        if x in v2:
            res += v1[x]*v2[x]
    fenmu2 = 0.0
    for x in v2:
        fenmu2 += v2[x]*v2[x]
    res /= math.sqrt(fenmu1*fenmu2)
    return res

def solve():
    global tf_idf_bow, identity_items, cat_match

    with open('items_test_5.txt', 'r') as f:
        with open('fm_submissions_test_simi.txt', 'w') as f3:
            cnt = 0
            while 1:
                line = f.readline()
                if not line:
                    break
                line=line.strip('\n')
                identity_items = {}
                for item in tf_idf_bow:
                    # 相同类别不考虑
                    if item_info[item] == item_info[line]:
                        continue
                    # 没出现在搭配集中的类别搭配，不考虑
                    if item_info[line] in cat_match:
                        if item_info[item] not in cat_match[item_info[line]]:
                            continue
                    simi = calSimi(line, item) #tf-idf分词向量余弦相似度
                    identity_items[item] = simi #测试商品line与候选商品item的相似度

                cnt += 1
                print('answer:', cnt)
                i = 0
                f3.write("%s " % line)
                for k,v in sorted(identity_items.items(), key=lambda x:x[1], reverse=True):
                    if (i>=199 or i == len(identity_items)-1):
                        f3.write("%s\n" % (k))
                        break
                    else:
                        f3.write("%s," % (k))
                    i += 1


if __name__=="__main__":
    readItems()
    print('read item OK!')

    solve()
    print('solve OK!')