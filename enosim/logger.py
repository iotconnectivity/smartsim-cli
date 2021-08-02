#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Pod Group Ltd.
#
# Authors:
#   - J. Félix Ontañón <felix.ontanon@podgroup.com>
#   - Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>

import logging

# create logger
logger = logging.getLogger('enosim')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

if __name__ == '__main__':

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')