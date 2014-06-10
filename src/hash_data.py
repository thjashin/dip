#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: hash_data.py

import os
import cPickle as pickle

from config import *


def hash_raw_to_dict():
    img2hash = dict()
    hash2img = dict()
    for name in os.listdir(hash_dir):
        filename = pjoin(hash_dir, name)
        if filename.endswith('.dat'):
            with open(filename, 'r') as f:
                for line in f:
                    if line.strip():
                        arr = line.strip().split(' ')
                        imgname = arr[0].strip()
                        hashcode = arr[1].strip()
                        img2hash[imgname] = hashcode
                        hash2img[hashcode] = imgname

    with open(hash2img_file, 'w') as f:
        pickle.dump(hash2img, f)

    with open(img2hash_file, 'w') as f:
        pickle.dump(img2hash, f)

    return img2hash, hash2img


def get_img2hash_dict():
    try:
        _hash_dict = None
        with open(img2hash_file, 'w') as f:
            _hash_dict = pickle.load(f)
        return _hash_dict
    except Exception:
        return hash_raw_to_dict()[0]


def get_hash2img_dict():
    try:
        _hash2img = None
        with open(hash2img_file, 'w') as f:
            _hash2img = pickle.load(f)
        return _hash2img
    except Exception:
        return hash_raw_to_dict()[1]

img2hash = get_img2hash_dict()
hash2img = get_hash2img_dict()


if __name__ == "__main__":
    for k, v in img2hash.iteritems():
        print k, v
        break
