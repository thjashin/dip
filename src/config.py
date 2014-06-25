#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: config.py

import os
pjoin = os.path.join

# train dir
train_dir = '/opt/dip-data/Train'
train_images_dir = pjoin(train_dir, 'images')

# train files
train_click_log = pjoin(train_dir, 'TrainClickLog.tsv')
train_file_map = pjoin(train_dir, 'images_map.tsv')

# dev dir
dev_dir = '/opt/dip-data/Dev'

# dev files
dev_label = pjoin(dev_dir, 'DevSetLabel.tsv')

# -----------------------------------------------------------------------------
# data dir
data_dir = 'data/'

# image name to gist feature
name2gist_file = pjoin(data_dir, 'img2gist')

# query doc
query_file = pjoin(data_dir, 'query_doc.txt')

# vocabulary file
vocab_file = pjoin(data_dir, 'vocab.txt')

# index dir
index_dir = 'whoosh_index'

# hash raw data
hash_dir = pjoin(data_dir, 'hash')

# hash dictionary
hash2img_file = pjoin(data_dir, 'hash2img')
img2hash_file = pjoin(data_dir, 'img2hash')

# -----------------------------------------------------------------------------
# gist image size
normal_size = (128, 128)
