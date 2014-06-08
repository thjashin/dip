#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: data_analysis.py

from __future__ import division
from config import *

def query_existed():
    train_queries = []
    with open(train_click_log, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[1].strip()
            train_queries.append(query)

    dev_count = 0
    existed_count = 0
    with open(dev_label, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[0].strip()
            dev_count += 1
            if query in train_queries:
                existed_count += 1
    print 'existed ratio:', existed_count/dev_count


if __name__ == "__main__":
    query_existed()