#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import platform
import pickle


def tt(text, lang=None, po={}):
    if lang:
        return po.get(lang, {}).get(text, text)

    return text


def tr_text(text, t=None):
    return t(text) if t else text


def get_lang_list(names=['en', 'zh']):
    return [get_lang_name(lang) for lang in names]


def get_lang_name(lang):
    if lang == 'zh':
        return 'Chinese - 简体中文'
    else:
        return 'en'


def get_lang_key(name):
    if 'Chinese' in name or 'Simplied' in name:
        return 'zh'

    return 'en'


def get_copy_right(text=None):
    return text if text else '(C) Nypro & Jabil Shanghai TE Support'


def get_platform_info():
    return '{} ({})\n{}'.format(platform.platform(),
                                platform.machine(),
                                platform.processor())


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
