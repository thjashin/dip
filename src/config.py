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

# trial dir
trial_dir = 'trial/'
trial_images_dir = pjoin(trial_dir, 'images')

# trial files
trial_click_log = pjoin(trial_dir, 'IRC2014MMTrial.keyquery.tsv')
trial_file_map = pjoin(trial_dir, 'images_map.tsv')

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

# hash dictionary
hash2img_file = pjoin(data_dir, 'hash2img')
img2hash_file = pjoin(data_dir, 'img2hash')

# image name to path
name2path = pjoin(data_dir, 'name2path')

# -----------------------------------------------------------------------------

# redis config
redis_config = {'redis': {'host': 'localhost', 'port': 6379}}

# redis persistence file
redis_rdb = 'dump.rdb'

# saved LSH random values
matrices_file = 'matrices.npz'

# -----------------------------------------------------------------------------
# gist image size
normal_size = (32, 32)

# length of hash
hash_len = 32
