#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="txStatHat",
    version='0.2.0',
    description="Twisted wrapper for StatHat.com",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        ],
    install_requires=['Twisted'],
    platforms=["any"],
    license="MIT",
    author="Hynek Schlawack",
    author_email="hs@ox.cx",
    url="https://github.com/hynek/txStatHat",
    py_modules=['txstathat'],
)
