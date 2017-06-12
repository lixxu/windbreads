#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
try:
    from Crypto.Cipher import AES
except ImportError:
    from Cryptodome.Cipher import AES

import windbreads.utils as wdu


def encrypt(text, key, iv, encoding='utf-8'):
    if isinstance(text, wdu.safe_unicode()):
        if wdu.IS_PY2:
            text = text.encode(encoding, 'ignore')
        elif wdu.IS_PY3:
            text = bytes(text, encoding, 'ignore')

    return AES.new(key, AES.MODE_CFB, iv).encrypt(text)


def decrypt(text, key, iv, encoding='utf-8'):
    text = AES.new(key, AES.MODE_CFB, iv).decrypt(text)
    if not isinstance(text, wdu.safe_unicode()):
        text = text.decode(encoding, 'ignore')

    return text
