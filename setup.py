#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
windbreads
----------------

Small handy snippets of non-GUI python
"""
import os.path

from setuptools import setup

folder = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(folder, "windbreads/__init__.py")) as f:
    for line in f:
        if line.startswith("__version__ = "):
            version = line.split("=")[-1].strip().replace('"', "")
        elif line.startswith("__author__ = "):
            author = line.split("=")[-1].strip().replace('"', "")
            break

setup(
    name="windbreads",
    version=version.replace("'", ""),
    url="https://github.com/lixxu/windbreads",
    license="BSD",
    author=author.replace("'", ""),
    author_email="xuzenglin@gmail.com",
    description="Small handy snippets of non-GUI python",
    long_description=__doc__,
    packages=["windbreads"],
    zip_safe=False,
    platforms="any",
    install_requires=["six"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
