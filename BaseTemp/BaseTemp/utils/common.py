# -*- coding:utf-8 -*-
# Author : oldman
# License : (C) Copyright 2015-2017, minivision
import re


def get_num(strs):
    num = re.match('.*?(\d+).*',strs).group(1)
    return num


def get_all_num(s):
    sl = list(s)
    num = []
    for s in sl:
        if s.isdigit() or s == '(' or s == ')':
            num.append(s)
    num = ''.join(num)
    return num


if __name__ =='__main__':
    pass