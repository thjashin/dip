#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @file: config.py

import os
pjoin = os.path.join

# train dir
train_dir = '/opt/dip-data/Train'

# train files
train_click_log = pjoin(train_dir, 'TrainClickLog.tsv')

# dev dir
dev_dir = '/opt/dip-data/Dev'

# dev files
dev_label = pjoin(dev_dir, 'DevSetLabel.tsv')

