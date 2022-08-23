import unittest
import unittest.mock

import io
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

    def test_parameters(self):

        self.assertEqual(sphinxter.Reader.parameters(example.func), {
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

    FUNCTION = {
            "name": "func",
            "description": "Some basic func",
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

    STATICMETHOD = {
        "name": "stat",
        "method": "static",
        "description": "Some static stat",
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
            "description": "things"
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

        self.assertEqual(sphinxter.Reader.attributes(example.Complex, body=True), {
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


class TestContent(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        content = sphinxter.Content("people", "stuff", "things")

        self.assertEqual(content.module, "people")
        self.assertEqual(content.kind, "stuff")
        self.assertEqual(content.parsed, "things")


class TestDocument(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        document = sphinxter.Document("people", "stuff")

        self.assertEqual(document.path, "people")
        self.assertEqual(document.indent, "stuff")
        self.assertEqual(document.contents, {})

    def test_add(self):

        document = sphinxter.Document(None, None)

        document.add("people", "stuff", "things", 7)

        self.assertEqual(document.contents[7][0].module, "people")
        self.assertEqual(document.contents[7][0].kind, "stuff")
        self.assertEqual(document.contents[7][0].parsed, "things")


class TestWriter(unittest.TestCase):

    maxDiff = None

    def setUp(self):

        document = sphinxter.Document(None, '    ')
        self.file = io.StringIO()
        self.file.write("\n")

        self.writer = sphinxter.Writer(document, self.file)

    def test___init__(self):

        writer = sphinxter.Writer("people", "stuff")

        self.assertEqual(writer.document, "people")
        self.assertEqual(writer.file, "stuff")

    def test_line(self):

        self.writer.line("a ", before=True)
        self.writer.line("b  ", 1, after=True)

        self.assertEqual(self.file.getvalue(), """

a
    b

""")

    def test_lines(self):

        self.writer.lines("a", 0, before=True)
        self.writer.lines("b\nc", 1, after=True)

        self.assertEqual(self.file.getvalue(), """

a
    b
    c

""")

    def test_types(self):

        self.assertEqual(self.writer.types("people"), "people")
        self.assertEqual(self.writer.types(["stuff", "things"]), "stuff or things")

    def test_description(self):

        self.writer.description({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        self.writer.description({"description": "a\nb\n"}, 1)
        self.assertEqual(self.file.getvalue(), """

    a
    b
""")

    def test_parameter(self):

        parsed = {
            "name": "small"
        }

        self.writer.parameter(parsed, 1)
        self.assertEqual(self.file.getvalue(), """
    :param small:
""")

        parsed = {
            "name": "big",
            "description": "stuff",
            "type": "int"
        }

        self.writer.parameter(parsed, 1)
        self.assertEqual(self.file.getvalue(), """
    :param small:
    :param big: stuff
    :type big: int
""")

    def test_parameters(self):

        self.writer.parameters({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "parameters": [
                {
                    "name": "small"
                },
                {
                    "name": "big",
                    "description": "stuff",
                    "type": "int"
                }
            ]
        }

        self.writer.parameters(parsed, 1)
        self.assertEqual(self.file.getvalue(), """
    :param small:
    :param big: stuff
    :type big: int
""")

    def test_returns(self):

        self.writer.returns({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "return": {
                "description": "stuff",
                "type": "int"
            }
        }

        self.writer.returns(parsed, 1)
        self.assertEqual(self.file.getvalue(), """
    :return: stuff
    :rtype: int
""")

    def test_raises(self):

        self.writer.raises({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "raises": {
                "Exception": "oh no"
            }
        }

        self.writer.raises(parsed, 1)
        self.assertEqual(self.file.getvalue(), """
    :raises Exception: oh no
""")

    def test_execution(self):

        self.writer.execution({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "parameters": [
                {
                    "name": "small"
                },
                {
                    "name": "big",
                    "description": "stuff",
                    "type": "int"
                }
            ],
            "return": {
                "description": "stuff",
                "type": "int"
            },
            "raises": {
                "Exception": "oh no"
            }
        }

        self.writer.execution(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    :param small:
    :param big: stuff
    :type big: int
    :return: stuff
    :rtype: int
    :raises Exception: oh no
""")

    def test_usage(self):

        self.writer.usage({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "usage": "a\nb"
        }

        self.writer.usage(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    **Usage**

    a
    b
""")

    def test_function(self):

        self.writer.function(TestReader.FUNCTION, 1)
        self.assertEqual(self.file.getvalue(), """

    .. function:: func(a, b, *args, **kwargs)

        Some basic func

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
        :rtype: str or None
        :raises Exception: if oh noes

        **Usage**

        Do some cool stuff::

            like this

        It's great
""")

    def test_attribute(self):

        parsed = {
            "name": "small"
        }

        self.writer.attribute(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    .. attribute:: small
""")

        parsed = {
            "name": "big",
            "description": "stuff",
            "type": "int"
        }

        self.writer.attribute(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    .. attribute:: small

    .. attribute:: big
        :type: int

        stuff
""")

    def test_attributes(self):

        self.writer.attributes({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "attributes": [
                {
                    "name": "small"
                },
                {
                    "name": "big",
                    "description": "stuff",
                    "type": "int"
                }
            ]
        }

        self.writer.attributes(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    .. attribute:: small

    .. attribute:: big
        :type: int

        stuff
""")

    def test_method(self):

        self.writer.method(TestReader.METHOD, 1)
        self.assertEqual(self.file.getvalue(), """

    .. method:: meth(a, b, *args, **kwargs)

        Some basic meth

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
        :rtype: str or None
        :raises Exception: if oh noes

        **Usage**

        Do some cool stuff::

            like this

        It's great
""")

    def test_definition(self):

        self.writer.definition({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        parsed = {
            "definition": "a\nb"
        }

        self.writer.definition(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    **Definition**

    a
    b
""")

    def test_cls(self):

        self.writer.cls(TestReader.COMPLEX_CLASS, 1)
        self.assertEqual(self.file.getvalue(), """

    .. class:: Complex(a, b, *args, **kwargs)

        Complex class

        call me

        **Definition**

        make sure you do this::

            wowsa

        Ya sweet

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:

        **Usage**

        Do some cool stuff::

            like this

        It's great

        .. attribute:: a

            The a team

        .. attribute:: b

            The b team

            Not as good as the a team

        .. attribute:: big

            Bunch a

        .. classmethod:: classy(a, b, *args, **kwargs)

            Some class meth

            :param a: The a More stuff
            :param b: The b
            :param args:
            :param kwargs:
            :return: things
            :rtype: str

        .. method:: meth(a, b, *args, **kwargs)

            Some basic meth

            :param a: The a More stuff
            :param b: The b
            :param args:
            :param kwargs:
            :return: things
            :rtype: str or None
            :raises Exception: if oh noes

            **Usage**

            Do some cool stuff::

                like this

            It's great

        .. staticmethod:: stat(a, b, *args, **kwargs)

            Some static stat

            :param a: The a More stuff
            :param b: The b
            :param args:
            :param kwargs:
            :return: things
""")

    def test_module(self):

        self.writer.module(TestReader.MODULE, 1)
        self.assertEqual(self.file.getvalue(), """

    .. module:: test.example

    test.example
    ============

    mod me

    .. attribute:: a

        The a team

    .. attribute:: b

        The b team

        Not as good as the a team

    .. attribute:: big

        Bunch a
""")

    EXAMPLE = """
.. created by sphinxter
.. default-domain:: py

.. module:: test.example

test.example
============

mod me

.. attribute:: a

    The a team

.. attribute:: b

    The b team

    Not as good as the a team

.. attribute:: big

    Bunch a

.. function:: func(a, b, *args, **kwargs)

    Some basic func

    :param a: The a More stuff
    :param b: The b
    :param args:
    :param kwargs:
    :return: things
    :rtype: str or None
    :raises Exception: if oh noes

    **Usage**

    Do some cool stuff::

        like this

    It's great

.. class:: Basic

    Basic class

.. class:: Complex(a, b, *args, **kwargs)

    Complex class

    call me

    **Definition**

    make sure you do this::

        wowsa

    Ya sweet

    :param a: The a More stuff
    :param b: The b
    :param args:
    :param kwargs:

    **Usage**

    Do some cool stuff::

        like this

    It's great

    .. attribute:: a

        The a team

    .. attribute:: b

        The b team

        Not as good as the a team

    .. attribute:: big

        Bunch a

    .. classmethod:: classy(a, b, *args, **kwargs)

        Some class meth

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
        :rtype: str

    .. method:: meth(a, b, *args, **kwargs)

        Some basic meth

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
        :rtype: str or None
        :raises Exception: if oh noes

        **Usage**

        Do some cool stuff::

            like this

        It's great

    .. staticmethod:: stat(a, b, *args, **kwargs)

        Some static stat

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
"""

    def test_dump(self):

        # actual

        self.writer.document = sphinxter.Document(None, '    ')

        self.writer.document.add("test.example", "module", TestReader.MODULE, 0)

        self.writer.document.add("test.example", "function", TestReader.FUNCTION, 0)

        self.writer.document.add("test.example", "class", TestReader.BASIC_CLASS, 0)

        self.writer.document.add("test.example", "class", TestReader.COMPLEX_CLASS, 0)

        self.writer.dump()

        self.assertEqual(self.file.getvalue(), self.EXAMPLE)

        # modules

        document = sphinxter.Document(None, '    ')
        file = io.StringIO()
        file.write("\n")

        writer = sphinxter.Writer(document, file)

        writer.document.add("people", "module", TestReader.MODULE, 0)

        writer.document.add("stuff", "function", TestReader.FUNCTION, 20)

        writer.document.add("things", "class", TestReader.BASIC_CLASS, 10)

        writer.dump()

        self.assertEqual(file.getvalue(), """
.. created by sphinxter
.. default-domain:: py

.. module:: test.example

test.example
============

mod me

.. attribute:: a

    The a team

.. attribute:: b

    The b team

    Not as good as the a team

.. attribute:: big

    Bunch a

.. currentmodule:: things

.. class:: Basic

    Basic class

.. currentmodule:: stuff

.. function:: func(a, b, *args, **kwargs)

    Some basic func

    :param a: The a More stuff
    :param b: The b
    :param args:
    :param kwargs:
    :return: things
    :rtype: str or None
    :raises Exception: if oh noes

    **Usage**

    Do some cool stuff::

        like this

    It's great
""")


class TestSphinxter(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        # defaults

        instance = sphinxter.Sphinxter("people")

        self.assertEqual(instance.modules, ["people"])
        self.assertEqual(instance.base, "docs/source")
        self.assertEqual(instance.indent, '    '
        )

        # values

        instance = sphinxter.Sphinxter("people", "stuff", "things")

        self.assertEqual(instance.modules, ["people"])
        self.assertEqual(instance.base, "stuff")
        self.assertEqual(instance.indent, "things")

    def test_document(self):

        parsed = {}

        instance = sphinxter.Sphinxter("people")

        # empty

        instance.document("stuff", "things", parsed)

        self.assertEqual(instance.documents["index.rst"].path, "docs/source/index.rst")
        self.assertEqual(instance.documents["index.rst"].indent, '    ')
        self.assertEqual(instance.documents["index.rst"].contents[0][0].module, "stuff")
        self.assertEqual(instance.documents["index.rst"].contents[0][0].kind, "things")
        self.assertEqual(instance.documents["index.rst"].contents[0][0].parsed, parsed)

        # skip

        parsed = {
            "sphinx": False
        }

        instance.document("stuff", "things", parsed)

        self.assertEqual(len(instance.documents["index.rst"].contents[0]), 1)

        # full

        parsed = {
            "sphinx": {
                "path": "new.rst",
                "order": 10
            }
        }

        instance.document("stuffins", "thingies", parsed)

        self.assertEqual(instance.documents["new.rst"].path, "docs/source/new.rst")
        self.assertEqual(instance.documents["new.rst"].contents[10][0].module, "stuffins")
        self.assertEqual(instance.documents["new.rst"].contents[10][0].kind, "thingies")
        self.assertEqual(instance.documents["new.rst"].contents[10][0].parsed, parsed)

    def test_read(self):

        instance = sphinxter.Sphinxter(example)

        instance.read()

        self.assertEqual(instance.documents["index.rst"].contents[0][0].module, "test.example")
        self.assertEqual(instance.documents["index.rst"].contents[0][0].kind, "module")
        self.assertEqual(instance.documents["index.rst"].contents[0][0].parsed, TestReader.MODULE)

        self.assertEqual(instance.documents["index.rst"].contents[0][1].module, "test.example")
        self.assertEqual(instance.documents["index.rst"].contents[0][1].kind, "function")
        self.assertEqual(instance.documents["index.rst"].contents[0][1].parsed, TestReader.FUNCTION)

        self.assertEqual(instance.documents["index.rst"].contents[0][2].module, "test.example")
        self.assertEqual(instance.documents["index.rst"].contents[0][2].kind, "class")
        self.assertEqual(instance.documents["index.rst"].contents[0][2].parsed, TestReader.BASIC_CLASS)

        self.assertEqual(instance.documents["index.rst"].contents[0][3].module, "test.example")
        self.assertEqual(instance.documents["index.rst"].contents[0][3].kind, "class")
        self.assertEqual(instance.documents["index.rst"].contents[0][3].parsed, TestReader.COMPLEX_CLASS)

        self.assertEqual(len(instance.documents["index.rst"].contents), 1)
        self.assertEqual(len(instance.documents["index.rst"].contents[0]), 4)

    @unittest.mock.patch('sphinxter.open', new_callable=unittest.mock.mock_open)
    def test_write(self, mock_open):

        instance = sphinxter.Sphinxter(example)

        instance.read()
        instance.write()

        mock_open.assert_called_once_with("docs/source/index.rst", "w")

        self.assertEqual("\n" + "".join([call.args[0] for call in mock_open.return_value.write.mock_calls]), TestWriter.EXAMPLE)

    @unittest.mock.patch('sphinxter.open', new_callable=unittest.mock.mock_open)
    def test_process(self, mock_open):

        instance = sphinxter.Sphinxter(example)

        instance.process()

        self.assertEqual("\n" + "".join([call.args[0] for call in mock_open.return_value.write.mock_calls]), TestWriter.EXAMPLE)
