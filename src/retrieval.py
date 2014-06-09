#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: retrieval.py

from whoosh import create_in
from whoosh.fields import *

from config import *

def create_index():
    schema = Schema(img=STORED(stored=True), query_doc=TEXT(stored=True))
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    with open(train_click_log, 'r') as f:
        last_image = None
        query_doc = ''
        for line in f:
            arr = line.strip().split('\t')
            image = arr[0].strip()
            query = arr[1].strip()
            if (image != last_image):
                print last_image
                print query_doc
                break
                writer.add_document(img=last_image, query_doc=query_doc)
                last_image = image
                query_doc = ''
            query_doc += ' ' + query

        writer.add_document(img=image, query_doc=query_doc)
        writer.commit()


if __name__ == "__main__":
    create_index()
