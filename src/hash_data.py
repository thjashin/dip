#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: hash_data.py

import os
import cPickle as pickle

from config import *


def hash_raw_to_dict():
    img2hash = dict()
    for name in os.listdir(hash_dir):
        filename = pjoin(hash_dir, name)
        if filename.endswith('.dat'):
            with open(filename, 'r') as f:
                for line in f:
                    if line.strip():
                        arr = line.strip().split(' ')
                        print arr
                        break
                        imgname = arr[0].strip()
                        hashcode = arr[1].strip()
                        img2hash[imgname] = hashcode

    with open(hash_dict_file, 'w') as f:
        pickle.dump(img2hash, f)

    return img2hash


def get_hash_dict():
    try:
        _hash_dict = None
        with open(hash_dict_file, 'w') as f:
            _hash_dict = pickle.load(f)
        return _hash_dict
    except Exception:
        return hash_raw_to_dict()


hash_dict = get_hash_dict()


if __name__ == "__main__":
    for k, v in hash_dict:
        print k, v
        break
