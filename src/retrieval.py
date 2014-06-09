#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: retrieval.py

import sys

from whoosh.index import create_in
from whoosh.fields import *

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
                    writer.add_document(img=last_image, query_doc=query_doc)
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


if __name__ == "__main__":
    create_index()
