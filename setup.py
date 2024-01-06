#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup,find_namespace_packages
from src.version import version

setup(
    name="mb_dash",
    version=version,
    description="mb_dash packages",
    author=["Malav Bateriwala"],
    packages=find_namespace_packages(include=["mb_dash.*"]),
    scripts=[],
    install_requires=[],
    python_requires='>=3.8',)
