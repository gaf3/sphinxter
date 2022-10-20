import unittest
import unittest.mock
import sphinxter.unittest

import inspect

import sphinxter
import test.example

class Complex:

    class Subber:

        pass

class TestReader(sphinxter.unittest.TestCase):

    maxDiff = None

    BASIC_SOURCE = """class Basic(Exception):
    \"""
    Basic Exception
    \"""
"""

    SUBBER_SOURCE = """class Subber:
    \"""
    Sub class
    \"""
    pass
"""

    def test_source(self):

        self.assertEqual(sphinxter.Reader.source(test.example.Basic), self.BASIC_SOURCE)
        self.assertEqual(sphinxter.Reader.source(test.example.Complex.Subber), self.SUBBER_SOURCE)

        self.assertSphinxter(sphinxter.Reader.source, transform=False)

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

        self.assertSphinxter(sphinxter.Reader.parse)

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

        self.assertSphinxter(sphinxter.Reader.update)

    @unittest.mock.patch("logging.info")
    def test_comments(self, mock_log):

        self.assertEqual(sphinxter.Reader.comments(test.example.func), {
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

        mock_log.assert_has_calls([
            unittest.mock.call("%s parameter: %s", "func", "a"),
            unittest.mock.call("%s parameter: %s", "func", "b"),
            unittest.mock.call("%s parameter: %s", "func", "kwargs")
        ])

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

        self.assertSphinxter(sphinxter.Reader.comments)

    def test_annotations(self):

        self.assertEqual(sphinxter.Reader.annotations(test.example.func), {
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

        self.assertEqual(sphinxter.Reader.annotations(test.example.Complex.stat), {
            "parameters": {},
            "return": {
                "type": "list"
            }
        })

        self.assertSphinxter(sphinxter.Reader.annotations)

    FUNCTION = {
            "name": "func",
            "kind": "function",
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
        "kind": "staticmethod",
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
        "kind": "classmethod",
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
        "kind": "method",
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

    @unittest.mock.patch("logging.info")
    def test_routine(self, mock_log):

        self.assertEqual(sphinxter.Reader.routine(inspect.getattr_static(test.example, 'func')), self.FUNCTION)

        mock_log.assert_any_call("routine: %s", "func")

        self.assertEqual(sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'stat'), method=True), self.STATICMETHOD)

        self.assertEqual(sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'classy'), method=True), self.CLASSMETHOD)

        self.assertEqual(sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'meth'), method=True), self.METHOD)

        self.assertSphinxter(sphinxter.Reader.routine)

    @unittest.mock.patch("logging.info")
    def test_attributes(self, mock_log):

        self.assertEqual(sphinxter.Reader.attributes(test.example.Complex), {
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

        mock_log.assert_has_calls([
            unittest.mock.call("attribute comment: a"),
            unittest.mock.call("attribute comment: b"),
            unittest.mock.call("attribute docstring: b"),
            unittest.mock.call("attribute comment: big"),
            unittest.mock.call("attribute docstring: big")
        ])

        self.assertEqual(sphinxter.Reader.attributes(test.example), {
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

        self.assertSphinxter(sphinxter.Reader.attributes)

    BASIC_EXCEPTION = {
        "name": "Basic",
        "kind": "exception",
        "description": "Basic Exception",
        "methods": [],
        "attributes": [],
        "classes": [],
        "exceptions": []
    }

    COMPLEX_CLASS = {
        "name": "Complex",
        "kind": "class",
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
                "kind": "class",
                "description": "Sub class",
                "methods": [],
                "attributes": [],
                "classes": [],
                "exceptions": []
            }
        ],
        "exceptions": [
            {
                "name": "Excepter",
                "kind": "exception",
                "description": "Sub exception",
                "methods": [],
                "attributes": [],
                "classes": [],
                "exceptions": []
            }
        ]
    }

    @unittest.mock.patch("logging.info")
    def test_cls(self, mock_log):

        self.assertEqual(sphinxter.Reader.cls(test.example.Basic), self.BASIC_EXCEPTION)

        mock_log.assert_any_call("class: Basic")

        self.assertEqual(sphinxter.Reader.cls(test.example.Complex), self.COMPLEX_CLASS)

        self.assertSphinxter(sphinxter.Reader.cls)

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
                COMPLEX_CLASS
            ],
            "exceptions": [
                BASIC_EXCEPTION
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
            ],
            "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
        }

    @unittest.mock.patch("logging.info")
    def test_module(self, mock_log):

        self.assertEqual(sphinxter.Reader.module(test.example), self.MODULE)

        mock_log.assert_any_call("module: test.example")

        self.assertSphinxter(sphinxter.Reader.module)
