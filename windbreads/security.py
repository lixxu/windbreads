#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from Crypto.Cipher import AES


def encrypt(text, key, iv, encoding='utf-8'):
    if isinstance(text, unicode):
        text = text.encode(encoding, 'ignore')

    return AES.new(key, AES.MODE_CFB, iv).encrypt(text)


def decrypt(text, key, iv, encoding='utf-8'):
    text = AES.new(key, AES.MODE_CFB, iv).decrypt(text)
    if not isinstance(text, unicode):
        text = text.decode(encoding, 'ignore')

    return text
