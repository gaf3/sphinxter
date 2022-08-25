#!/usr/bin/env python

import sphinxter

sphinxter.Sphinxter(
    sphinxter,
    {
        'index': "sphinxter.Sphinxter",
        'reader': "sphinxter.Reader",
        'writer': "sphinxter.Writer",
        'document': "sphinxter.Document"
    },
    [
        'self',
        'reader',
        'writer',
        'document'
    ]
).process()
