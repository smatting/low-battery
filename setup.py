#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="low-battery",
    version="1.0.0",
    packages=find_packages(),
    scripts=["bin/lowbattery"],

    author="Stefan Matting",
    author_email="stefan.matting@gmail.com",
    url="https://github.com/smatting/low-battery",
    description="A tool that notifies when the laptop battery runs low.",
    long_description=read('README.md'),
    license="MIT",
)
