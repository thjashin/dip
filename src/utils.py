#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: utils.py

import sys

from config import *


def get_name2path():
    ret = {}
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
                ret[name] = rpath
                sys.stdout.write('%d/%d\r     ' % (count, total_num))
                sys.stdout.flush()
    return ret

name2path = get_name2path()

if __name__ == "__main__":
    pass
