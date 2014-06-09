#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: data_analysis.py

from __future__ import division
import sys

import ngram
import nltk

from config import *

pjoin = os.path.join


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
            dev_queries.append(query)

    print 'conduct a search...'
    sys.stdout.flush()

    G = ngram.NGram(train_queries)
    print G.NGram.search(dev_queries[0], threshold=0.3)


def get_vocabulary():
    print 'get queries in train set...'
    sys.stdout.flush()

    query_doc_existed = False
    try:
        with open(query_doc, 'r') as f:
            query_doc_str = f.read()
        query_doc_existed = True
    except Exception:
        print 'query doc not existed...'
        sys.stdout.flush()
        train_queries = []
        with open(train_click_log, 'r') as f:
            for line in f:
                arr = line.strip().split('\t')
                query = arr[1].strip()
                train_queries.append(query)

    if not query_doc_existed:
        print 'write to query doc file...'
        sys.stdout.flush()
        query_doc_str = ' '.join(train_queries)
        with open(query_doc, 'w') as f:
            f.write(query_doc_str)

    print 'tokenize...'
    sys.stdout.flush()
    pre_tokens = []
    sentences = [sent for sent in nltk.sent_tokenize(query_doc_str)]
    print 'number of sentences', len(sentences)
    sys.stdout.flush()
    for sent in sentences:
        pre_tokens.extend([word for word in nltk.word_tokenize(sent)])
    pre_tokens = set(t.lower() for t in pre_tokens if len(t) >= 3)

    print 'remove stop word...'
    sys.stdout.flush()
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = set(t for t in pre_tokens if t not in stopwords)

    print 'remained/before:', len(tokens), '/', len(pre_tokens)
    print 'write to vocabulary file...'
    sys.stdout.flush()
    with open(vocab_file, 'w') as f:
        f.write('\t'.join(tokens))


if __name__ == "__main__":
    # query_existed()
    # query_search_test()
    get_vocabulary()
