#!/usr/bin/env python

import sphinxter

sphinxter.Sphinxter(
    sphinxter,
    {
        'index': "sphinxter",
        'sphinxter': "sphinxter.Sphinxter",
        'reader': "sphinxter.Reader",
        'writer': "sphinxter.Writer",
        'document': "sphinxter.Document"
    },
    [
        'self',
        'sphinxter',
        'reader',
        'writer',
        'document'
    ]
).process()
