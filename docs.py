#!/usr/bin/env python

import logging

import sphinxter
import sphinxter.unittest

logging.getLogger().setLevel(logging.INFO)

sphinxter.Sphinxter(
    [sphinxter, sphinxter.unittest],
    {
        'index': "sphinxter",
        'sphinxter': "sphinxter.Sphinxter",
        'reader': "sphinxter.Reader",
        'writer': "sphinxter.Writer",
        'document': "sphinxter.Document",
        'unittest': "sphinxter.unittest"
    },
    [
        'self',
        'sphinxter',
        'reader',
        'writer',
        'document',
        'unittest'
    ]
).process()
