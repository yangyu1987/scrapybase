# -*-coding:utf-8 -*-
from datetime import datetime
import pymongo
import os

# print(datetime.now().strftime('%Y-%m-%d'))
#
#
# client = pymongo.MongoClient('localhost',27017)
# imdb = client['imdb']
# movie = imdb['movie']
#
# data = {
#     'title':'dadada',
#     'time':'2017',
# }
#
# movie.insert(data)

s = '+(12)212121num.dsds3432232ada'


def get_all_num(s):
    sl = list(s)
    num = []
    for s in sl:
        if s.isdigit() or s == '(' or s == ')':
            num.append(s)
    num = ''.join(num)
    return num

# print(get_all_num(s))

# name2list = []
# name3list = []
# with open('name.txt','r') as f:
#     for index,name in enumerate(f.read().split('#')):
#         if len(name) == 2:
#             name2list.append(name)
#         elif len(name) == 3:
#             name3list.append(name)
#
#     print(len(name2list))
#     print(len(name3list))


name5002list = []
name5003list = []
with open('name500.txt','r') as f:
    for name in f.readlines():
        print(str(name.split()))
        # if len(name) == 2:
        #     name5002list.append(name)
        # elif len(name) == 3:
        #     name5003list.append(name)

    print(len(name5002list))
    print(len(name5003list))


