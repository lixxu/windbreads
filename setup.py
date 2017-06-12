#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
windbreads
----------------

Small handy snippets of non-GUI python
"""
from setuptools import setup
import windbreads

setup(
    name='windbreads',
    version=windbreads.__version__,
    url='https://github.com/lixxu/windbreads',
    license='BSD',
    author=windbreads.__author__,
    author_email='xuzenglin@gmail.com',
    description='Small handy snippets of non-GUI python',
    long_description=__doc__,
    packages=['windbreads'],
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
