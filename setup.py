#!/usr/bin/env python

from setuptools import setup

with open("/opt/service/README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="sphinxter",
    version="0.1.0",
    package_dir = {'': 'lib'},
    py_modules = ['sphinxter'],
    install_requires=[
        'Sphinx==5.1.1',
        'PyYAML==6.0'
    ],
    url="https://github.com/gaf3/sphinxter",
    author="Gaffer Fitch",
    author_email="sphinxter@gaf3.com",
    description="Converts YAML docstrings and code comments to sphinx documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)