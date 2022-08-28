import unittest
import unittest.mock

import inspect

import sphinxter
from test import example

class TestReader(unittest.TestCase):

    maxDiff = None

    @unittest.mock.patch("inspect.getsourcelines")
    def test_source(self, mock_lines):

        def lines(source):
            return ([f"{line}\n" for line in source.split("\n")],)

        mock_lines.side_effect = lines

        self.assertEqual(sphinxter.Reader.source("people"), "people\n")
        self.assertEqual(sphinxter.Reader.source("  stuff\n    people"), "stuff\n  people\n")
        self.assertEqual(sphinxter.Reader.source("\tstuff\n\t\tpeople"), "stuff\n\tpeople\n")

    def test_parse(self):

        # None

        self.assertEqual(sphinxter.Reader.parse(None), {})

        # str

        self.assertEqual(sphinxter.Reader.parse("ya"), {
            "description": "ya"
        })

        # dict

        self.assertEqual(sphinxter.Reader.parse("a: 1"), {
            "a": 1
        })

    def test_update(self):

        # empty

        primary = {}
        secondary = {
            "name": "foole",
            "description": "sure",
            "b": 2
        }

        sphinxter.Reader.update(primary, secondary)

        self.assertEqual(primary, {
            "name": "foole",
            "description": "sure",
            "b": 2
        })

        # full

        primary = {
            "name": "fool",
            "description": "Ya",
            "a": 1,
            "b": 1
        }
        secondary = {
            "name": "foole",
            "description": "sure",
            "b": 2
        }

        sphinxter.Reader.update(primary, secondary, skip="name")

        self.assertEqual(primary, {
            "name": "fool",
            "description": "Ya\n\nsure",
            "a": 1,
            "b": 2
        })

    def test_comments(self):

        self.assertEqual(sphinxter.Reader.comments(example.func), {
            "a": {
                "description": "The a"
            },
            "b": {
                "description": "The b"
            },
            "args": {},
            "kwargs": {
                "a": 1,
                "b": 2
            }
        })

        def func(
            a,              # The a
            b:bool=False    # The b
        ):
            pass

        self.assertEqual(sphinxter.Reader.comments(func), {
            "a": {
                "description": "The a"
            },
            "b": {
                "description": "The b"
            }
        })

    def test_annotations(self):

        self.assertEqual(sphinxter.Reader.annotations(example.func), {
            "parameters": {
                "a": {
                    "type": "int"
                },
                "b": {
                    "type": "str"
                }
            },
            "return": {}
        })

        self.assertEqual(sphinxter.Reader.annotations(example.Complex.stat), {
            "parameters": {},
            "return": {
                "type": "list"
            }
        })

    FUNCTION = {
            "name": "func",
            "description": "Some basic func",
            "signature": "(a: int, b: 'str', *args, **kwargs)",
            "parameters": [
                {
                    "name": "a",
                    "description": "The a More stuff",
                    "type": "int"
                },
                {
                    "name": "b",
                    "description": "The b",
                    "more": "stuff",
                    "type": "str"
                },
                {
                    "name": "args"
                },
                {
                    "name": "kwargs",
                    "a": 1,
                    "b": 2
                }
            ],
            "return": {
                "description": "things",
                "type": [
                    'str',
                    'None'
                ]
            },
            "raises": {
                "Exception": "if oh noes"
            },
            "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
        }

    STATICMETHOD = {
        "name": "stat",
        "method": "static",
        "description": "Some static stat",
        "signature": "(a, b, *args, **kwargs) -> list",
        "parameters": [
            {
                "name": "a",
                "description": "The a More stuff"
            },
            {
                "name": "b",
                "description": "The b",
                "more": "stuff"
            },
            {
                "name": "args"
            },
            {
                "name": "kwargs",
                "a": 1,
                "b": 2
            }
        ],
        "return": {
            "description": "things",
            "type": "list"
        }
    }

    CLASSMETHOD = {
        "name": "classy",
        "method": "class",
        "description": "Some class meth",
        "signature": "(a, b, *args, **kwargs)",
        "parameters": [
            {
                "name": "a",
                "description": "The a More stuff"
            },
            {
                "name": "b",
                "description": "The b",
                "more": "stuff"
            },
            {
                "name": "args"
            },
            {
                "name": "kwargs",
                "a": 1,
                "b": 2
            }
        ],
        "return": {
            "description": "things",
            "type": 'str'
        }
    }

    METHOD = {
        "name": "meth",
        "method": "",
        "description": "Some basic meth",
        "signature": "(a, b, *args, **kwargs)",
        "parameters": [
            {
                "name": "a",
                "description": "The a More stuff"
            },
            {
                "name": "b",
                "description": "The b",
                "more": "stuff"
            },
            {
                "name": "args"
            },
            {
                "name": "kwargs",
                "a": 1,
                "b": 2
            }
        ],
        "return": {
            "description": "things",
            "type": [
                'str',
                'None'
            ]
        },
        "raises": {
            "Exception": "if oh noes"
        },
        "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
    }

    def test_function(self):

        self.assertEqual(sphinxter.Reader.function(inspect.getattr_static(example, 'func')), self.FUNCTION)

        self.assertEqual(sphinxter.Reader.function(inspect.getattr_static(example.Complex, 'stat'), method=True), self.STATICMETHOD)

        self.assertEqual(sphinxter.Reader.function(inspect.getattr_static(example.Complex, 'classy'), method=True), self.CLASSMETHOD)

        self.assertEqual(sphinxter.Reader.function(inspect.getattr_static(example.Complex, 'meth'), method=True), self.METHOD)

    def test_attributes(self):

        self.assertEqual(sphinxter.Reader.attributes(example.Complex), {
            "a": {
                "description": "The a team"
            },
            "b": {
                "description": "The b team\n\nNot as good as the a team"
            },
            "big": {
                "a": 1,
                "b": 2,
                "description": "Bunch a"
            }
        })

        self.assertEqual(sphinxter.Reader.attributes(example), {
            "a": {
                "description": "The a team"
            },
            "b": {
                "description": "The b team\n\nNot as good as the a team"
            },
            "big": {
                "a": 1,
                "b": 2,
                "description": "Bunch a"
            }
        })

    BASIC_CLASS = {
        "name": "Basic",
        "description": "Basic class",
        "methods": [],
        "attributes": [],
        "classes": []
    }

    COMPLEX_CLASS = {
        "name": "Complex",
        "description": "Complex class\n\ncall me",
        "signature": "(a, b, *args, **kwargs)",
        "definition": "make sure you do this::\n\n    wowsa\n\nYa sweet\n",
        "parameters": [
            {
                "name": "a",
                "description": "The a More stuff"
            },
            {
                "name": "b",
                "description": "The b",
                "more": "stuff"
            },
            {
                "name": "args"
            },
            {
                "name": "kwargs",
                "a": 1,
                "b": 2
            }
        ],
        "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n",
        "attributes": [
            {
                "name": "a",
                "description": "The a team"
            },
            {
                "name": "b",
                "description": "The b team\n\nNot as good as the a team"
            },
            {
                "name": "big",
                "a": 1,
                "b": 2,
                "description": "Bunch a"
            }
        ],
        "methods": [
            CLASSMETHOD,
            METHOD,
            STATICMETHOD
        ],
        "classes": [
            {
                "name": "Subber",
                "description": "Sub class",
                "methods": [],
                "attributes": [],
                "classes": []
            }
        ]
    }

    def test_cls(self):

        self.assertEqual(sphinxter.Reader.cls(example.Basic), self.BASIC_CLASS)

        self.assertEqual(sphinxter.Reader.cls(example.Complex), self.COMPLEX_CLASS)

    MODULE = {
            "name": "test.example",
            "description": "mod me",
            "attributes": [
                {
                    "name": "a",
                    "description": "The a team"
                },
                {
                    "name": "b",
                    "description": "The b team\n\nNot as good as the a team"
                },
                {
                    "name": "big",
                    "a": 1,
                    "b": 2,
                    "description": "Bunch a"
                }
            ],
            "functions": [
                FUNCTION
            ],
            "classes": [
                BASIC_CLASS,
                COMPLEX_CLASS
            ],
            "attributes": [
                {
                    "name": "a",
                    "description": "The a team"
                },
                {
                    "name": "b",
                    "description": "The b team\n\nNot as good as the a team"
                },
                {
                    "name": "big",
                    "a": 1,
                    "b": 2,
                    "description": "Bunch a"
                }
            ]
        }

    def test_module(self):

        self.assertEqual(sphinxter.Reader.module(example), self.MODULE)
