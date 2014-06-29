#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: main.py

from __future__ import division
import sys
import numpy as np

from config import *
from retrieval import query_top10_images, gist_top10_images, get_img2gist
from utils import get_name2path

from PIL import Image
from cropresize import crop_resize
import leargist

img2gist = get_img2gist()

query_miss = 0
hash_miss = 0


def main_proc(query, image_path):
    """
    Return distance of a (query, image) pair
    """
    global query_miss, hash_miss

    im = Image.open(image_path)
    im = crop_resize(im, normal_size, True)
    desc = leargist.color_gist(im)

    A = query_top10_images(query)
    B = gist_top10_images(image_path)
    if not A:
        query_miss += 1
    if not B:
        hash_miss += 1
    sim_set = []
    for i in A:
        gist_i = img2gist[i]
        for j in B:
            v = np.sum((gist_i - img2gist[j]) ** 2)
            sim_set.append(v)
        sim_set.append(np.sum((gist_i - desc) ** 2))

    return min(sim_set)


def test_on_dev():
    # load name2path
    name2path = get_name2path(dev_file_map)

    rel_d = {'Excellent': 3, 'Good': 2, 'Bad': 0}

    total_count = 0
    with open(dev_label, 'r') as f:
        for line in f:
            if line.strip():
                total_count += 1

    dcg = 0
    num_of_queries = 0
    with open(dev_label, 'r') as f:
        last_query = None
        qimgs = []
        count = 0
        for line in f:
            if line.split():
                arr = line.strip().split()
                query = arr[0].strip()
                name = arr[1].strip()
                rel = rel_d[arr[2].strip()]
                if (last_query is not None) and query != last_query:
                    num_of_queries += 1
                    qimgs.sort(lambda x, y: cmp(x[1], y[1]))
                    dcg += 0.01757 * \
                        sum([(2 ** t[0] - 1) / np.log2(i + 1)
                            for i, t in enumerate(qimgs[:25])])
                    qimgs = []
                qimgs.append((rel, main_proc(query, name2path[name])))
                last_query = query

                count += 1
                sys.stdout.write('%d/%d     \r' % (count, total_count))
                sys.stdout.flush()
        if qimgs:
            num_of_queries += 1
            qimgs.sort(lambda x, y: cmp(x[1], y[1]))
            dcg += 0.01757 * \
                sum([(2 ** t[0] - 1) / np.log2(i + 1)
                    for i, t in enumerate(qimgs[:25])])
    dcg /= num_of_queries

    print 'On Dev set'
    print 'Average DCG:', dcg
    print 'Query miss:', query_miss
    print 'Hash miss:', hash_miss


if __name__ == "__main__":
    test_on_dev()
