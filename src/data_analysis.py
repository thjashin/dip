#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: data_analysis.py

from __future__ import division
from config import *

def query_existed():
    train_queries = set()
    with open(train_click_log, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[1].strip()
            print query
            break
            train_queries.add(query)

    dev_queries = set()
    with open(dev_label, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[0].strip()
            print query
            break
            dev_queries.add(query)
    existed = len(dev_queries.intersection(train_queries))
    total = len(dev_queries)
    print 'existed:', existed
    print 'dev:', total
    print 'existed ratio:', existed/total


if __name__ == "__main__":
    query_existed()
