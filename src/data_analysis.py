#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: data_analysis.py

from __future__ import division
import sys

import ngram

from config import *

def query_existed():
    """
    Results:

    train: 11701890
    existed: 355
    dev: 1000
    existed ratio: 0.355
    """
    train_queries = set()
    with open(train_click_log, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[1].strip()
            train_queries.add(query)

    dev_queries = set()
    with open(dev_label, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[0].strip()
            dev_queries.add(query)
    existed = len(dev_queries.intersection(train_queries))
    total = len(dev_queries)
    print 'train:', len(train_queries)
    print 'existed:', existed
    print 'dev:', total
    print 'existed ratio:', existed/total


def query_search_test():
    print 'generate queries in train set...'
    sys.stdout.flush()

    train_queries = []
    with open(train_click_log, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[1].strip()
            train_queries.append(query)

    print 'generate queries in dev set...'
    sys.stdout.flush()

    dev_queries = []
    with open(dev_label, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            query = arr[0].strip()
            dev_queries.add(query)

    print 'conduct a search...'
    sys.stdout.flush()

    G = ngram.NGram(train_queries)
    print G.NGram.search(dev_queries[0], threshold=0.3)


if __name__ == "__main__":
    # query_existed()
    query_search_test()