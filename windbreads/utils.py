#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pickle


def get_copy_right(text=None):
    return text if text else '(C) Nypro & Jabil Shanghai TE Support'


def dump_pickle(data, pk_file, silent=True):
    try:
        with open(pk_file, 'wb') as f:
            pickle.dump(data, f)

    except:
        if not silent:
            raise


def load_pickle(pk_file, silent=True):
    try:
        with open(pk_file, 'rb') as f:
            return pickle.load(f)

    except:
        if silent:
            return {}

        raise
