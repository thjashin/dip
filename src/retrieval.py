#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: retrieval.py

import sys

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser

from config import *

def create_index():
    schema = Schema(img=STORED(), query_doc=TEXT(stored=True))
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    counter = 0
    with open(train_click_log, 'r') as f:
        image = None
        last_image = None
        query_doc = []
        for line in f:
            arr = line.strip().split('\t')
            image = arr[0].strip()
            query = arr[1].strip()
            if ((last_image is None) or (image != last_image)):
                counter += 1
                sys.stdout.write('\r%d ...' % counter)
                sys.stdout.flush()
                if (last_image is not None):
                    writer.add_document(img=last_image, query_doc=u' '.join(query_doc))
                last_image = image
                query_doc = []
            try:
                query_doc.append(unicode(query, 'utf-8'))
            except UnicodeError:
                pass

        if (image is not None):
            writer.add_document(img=image, query_doc=u' '.join(query_doc))
            writer.commit()

        sys.stdout.write('\rfinished!\n')
        sys.stdout.flush()


def test_search():
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        parser = QueryParser('query_doc', ix.schema)
        myquery = parser.parse(u'black history')
        results = searcher.search(myquery)
        print len(results)
        for i in results:
            print i



if __name__ == "__main__":
    # create_index()
    test_search()
