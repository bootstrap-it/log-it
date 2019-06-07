#!/usr/bin/env python

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="log_it",
    py_modules=["log_it"],
    version="0.0.1",
    description="Logging module with nice formating",
    author="Mikalai Davydzenka",
    author_email="mikalai.davydzenka@gmail.com",
    # url="",
    # download_url="",
    long_description=readme,
    long_description_content_type="text/markdown; charset=UTF-8",
    install_requires=[
        "termcolor",
    ],
    license="MIT license",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)