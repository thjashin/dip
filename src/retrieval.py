#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: retrieval.py

import sys
import cPickle as pickle

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
import leargist
from PIL import Image
from lshash import LSHash
from cropresize import crop_resize
import json

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
                    writer.add_document(
                        img=last_image, query_doc=u' '.join(query_doc))
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
        myquery = parser.parse(u'black hitsory')
        results = searcher.search(myquery)
        print len(results)
        for i in results:
            print i


def query_top10_images(query):
    try:
        query = unicode(query, 'utf-8')
    except UnicodeError:
        return []

    ix = open_dir(index_dir)
    ret = None
    with ix.searcher() as searcher:
        parser = QueryParser('query_doc', ix.schema)
        query = parser.parse(query)
        results = searcher.search(query)
        ret = [i['img'] for i in results]

    return ret


def get_img2gist():
    try:
        img2gist = None
        with open(name2gist_file, 'rb') as f:
            print 'loading existed img2gist...'
            sys.stdout.flush()
            img2gist = pickle.load(f)
        return img2gist
    except Exception:
        img2gist = {}
        total_num = 0
        with open(train_file_map, 'r') as f:
            for line in f:
                if line.strip():
                    total_num += 1
        count = 0
        with open(train_file_map, 'r') as f:
            for line in f:
                if line.strip():
                    count += 1
                    arr = line.strip().split()
                    name = arr[0].strip()
                    rpath = arr[1].strip()
                    im = Image.open(pjoin(train_images_dir, rpath))
                    im = crop_resize(im, normal_size, True)
                    desc = leargist.color_gist(im)
                    img2gist[name] = desc
                    sys.stdout.write(
                        '%d/%d\r size:(%d, %d)    ' % (count, total_num, im.size[0], im.size[1]))
                    sys.stdout.flush()
        with open(name2gist_file, 'wb') as f:
            pickle.dump(img2gist, f)
        return img2gist


def create_hash2img():
    img2gist = get_img2gist()
    lsh = LSHash(32, 960, storage_config=redis_config,
                 matrices_filename=matrices_file)
    count = 0
    total_num = len(img2gist)
    for name, gist_v in img2gist.iteritems():
        count += 1
        lsh.index(gist_v, name)
        sys.stdout.write('%d/%d\r    ' % (count, total_num))
        sys.stdout.flush()

    print 'bucket ratio: %d/%d' % (len(lsh.hash_tables[0].keys()), 2 ** 16)
    return lsh


def get_hash2img():
    if os.path.exists(redis_rdb):
        lsh = LSHash(32, 960, storage_config=redis_config,
                     matrices_filename=matrices_file)
        return lsh
    else:
        return create_hash2img()


lsh = get_hash2img()


def gist_top10_images(img):
    global lsh
    # info of known dataset
    print lsh.hash_tables[0].keys()[0]
    print 'bucket ratio: %d/%d' % (len(lsh.hash_tables[0].keys()), 2 ** 32)
    counts = []
    t = lsh.hash_tables[0]
    for k in t.keys():
        counts.append(len(t.get_value(k)))
    print 'max conflicts:', max(counts)

    im = Image.open(img)
    im = crop_resize(im, normal_size, True)
    desc = leargist.color_gist(im)
    for i in xrange(len(desc)):
        desc[i] += 0.01
    res = lsh.query(desc, num_results=None, distance_func="hamming")
    print 'num of results:', len(res)
    for i in res:
        print json.loads(i[0])[1], i[1]

if __name__ == "__main__":
    # create_index()
    # test_search()
    # print query_top10_images('black history')
    # get_img2gist()

    # top should be +FG2AXmgIIbP8Q
    path = pjoin(train_images_dir, '11f/4e2006aa6911d7314c96a57f7d572.jpg')
    gist_top10_images(path)
