#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: main.py

from __future__ import division
import numpy as np

from config import *
from retrieval import query_top10_images, gist_top10_images, get_img2gist
from utils import get_name2path

img2gist = get_img2gist()


def main_proc(query, image_path):
    """
    Return distance of a (query, image) pair
    """
    A = query_top10_images(query)
    B = gist_top10_images(image_path)
    sim_set = []
    for i in A:
        for j in B:
            v = np.sum((img2gist[i] - img2gist[j]) ** 2)
            sim_set.append(v)
    return min(sim_set)


def test_on_dev():
    # load name2path
    name2path = get_name2path(dev_file_map)

    rel_d = {'Excellent': 3, 'Good': 2, 'Bad': 0}

    dcg = 0
    num_of_queries = 0
    with open(dev_label, 'r') as f:
        last_query = None
        qimgs = []
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
        if qimgs:
            num_of_queries += 1
            qimgs.sort(lambda x, y: cmp(x[1], y[1]))
            dcg += 0.01757 * \
                sum([(2 ** t[0] - 1) / np.log2(i + 1)
                    for i, t in enumerate(qimgs[:25])])
    dcg /= num_of_queries

    print 'On Dev set'
    print 'Average DCG:', dcg


if __name__ == "__main__":
    test_on_dev()
