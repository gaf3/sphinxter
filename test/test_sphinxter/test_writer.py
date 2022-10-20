import unittest
import unittest.mock
import sphinxter.unittest

import io

import sphinxter
from test import example
import test.test_sphinxter.test_reader

class TestWriter(sphinxter.unittest.TestCase):

    maxDiff = None

    def setUp(self):

        document = sphinxter.Document(None, "test.example", None, '    ')
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

        self.assertSphinxter(sphinxter.Writer.line, transform=False)

    def test_lines(self):

        self.writer.lines("a", 0, before=True)
        self.writer.lines("b\nc", 1, after=True)

        self.assertEqual(self.file.getvalue(), """

a
    b
    c

""")

        self.assertSphinxter(sphinxter.Writer.lines, transform=False)

    def test_types(self):

        self.assertEqual(self.writer.types("people"), "people")
        self.assertEqual(self.writer.types(["stuff", "things"]), "stuff or things")

        self.assertSphinxter(sphinxter.Writer.types)

    def test_description(self):

        self.writer.description({}, 1)
        self.assertEqual(self.file.getvalue(), """
""")

        self.writer.description({"description": "a\nb\n"}, 1)
        self.assertEqual(self.file.getvalue(), """

    a
    b
""")

        self.assertSphinxter(sphinxter.Writer.description, transform=False)

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

        self.assertSphinxter(sphinxter.Writer.parameter, transform=False)

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

        self.assertSphinxter(sphinxter.Writer.parameters, transform=False)

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

        self.assertSphinxter(sphinxter.Writer.returns, transform=False)

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

        self.assertSphinxter(sphinxter.Writer.raises, transform=False)

    def test_routine(self):

        self.writer.routine({}, 1)
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

        self.writer.routine(parsed, 1)
        self.assertEqual(self.file.getvalue(), """

    :param small:
    :param big: stuff
    :type big: int
    :return: stuff
    :rtype: int
    :raises Exception: oh no
""")

        self.assertSphinxter(sphinxter.Writer.routine, transform=False)

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

        self.assertSphinxter(sphinxter.Writer.usage, transform=[True, False, False])

    def test_function(self):

        self.writer.function(test.test_sphinxter.test_reader.TestReader.FUNCTION, 1)
        self.assertEqual(self.file.getvalue(), """

    .. function:: func(a: int, b: 'str', *args, **kwargs)

        Some basic func

        :param a: The a More stuff
        :type a: int
        :param b: The b
        :type b: str
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

        self.assertSphinxter(sphinxter.Writer.function, transform=[True, False])

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

        self.assertSphinxter(sphinxter.Writer.attribute, transform=False)

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

        self.assertSphinxter(sphinxter.Writer.attributes, transform=False)

    def test_method(self):

        self.writer.method(test.test_sphinxter.test_reader.TestReader.METHOD, 1)
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

        self.assertSphinxter(sphinxter.Writer.method, transform=[True, False, True, False, True, False])

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

        self.assertSphinxter(sphinxter.Writer.definition, transform=[True, False, False])

    def test_cls(self):

        self.writer.cls(test.test_sphinxter.test_reader.TestReader.BASIC_EXCEPTION, 1)
        self.assertEqual(self.file.getvalue(), """

    .. exception:: Basic

        Basic Exception
""")

        self.writer.cls(test.test_sphinxter.test_reader.TestReader.COMPLEX_CLASS, 1)
        self.assertEqual(self.file.getvalue(), """

    .. exception:: Basic

        Basic Exception

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

        .. staticmethod:: stat(a, b, *args, **kwargs) -> list

            Some static stat

            :param a: The a More stuff
            :param b: The b
            :param args:
            :param kwargs:
            :return: things
            :rtype: list

        .. class:: Subber

            Sub class

        .. exception:: Excepter

            Sub exception
""")

        self.assertSphinxter(sphinxter.Writer.cls, transform=[True, False, True, False])

    def test_module(self):

        self.writer.module(test.test_sphinxter.test_reader.TestReader.MODULE, 1)
        self.assertEqual(self.file.getvalue(), """

    .. module:: test.example

    mod me

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
""")

        self.assertSphinxter(sphinxter.Writer.module, transform=[True, False])

    def test_toctree(self):

        self.writer.toctree(['*'], 1)

        self.assertEqual(self.file.getvalue(), """

    .. toctree::
        :maxdepth: 1
        :glob:
        :hidden:

        *
""")

        self.assertSphinxter(sphinxter.Writer.toctree, transform=False)

    EXAMPLE = """
.. created by sphinxter
.. default-domain:: py

test.example
============

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    self
    *

.. module:: test.example

mod me

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

.. function:: func(a: int, b: 'str', *args, **kwargs)

    Some basic func

    :param a: The a More stuff
    :type a: int
    :param b: The b
    :type b: str
    :param args:
    :param kwargs:
    :return: things
    :rtype: str or None
    :raises Exception: if oh noes

    **Usage**

    Do some cool stuff::

        like this

    It's great

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

    .. staticmethod:: stat(a, b, *args, **kwargs) -> list

        Some static stat

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
        :rtype: list

    .. class:: Subber

        Sub class

    .. exception:: Excepter

        Sub exception

.. exception:: Basic

    Basic Exception
"""

    def test_dump(self):

        # actual

        self.writer.document = sphinxter.Document(None, "test.example", ['self', '*'], '    ')

        self.writer.document.add("test.example", "module", test.test_sphinxter.test_reader.TestReader.MODULE, 0)

        self.writer.document.add("test.example", "function", test.test_sphinxter.test_reader.TestReader.FUNCTION, 0)

        self.writer.document.add("test.example", "class", test.test_sphinxter.test_reader.TestReader.COMPLEX_CLASS, 0)

        self.writer.document.add("test.example", "exception", test.test_sphinxter.test_reader.TestReader.BASIC_EXCEPTION, 0)

        self.writer.dump()

        self.assertEqual(self.file.getvalue(), self.EXAMPLE)

        # modules

        document = sphinxter.Document(None, "test.example", False, '    ')
        file = io.StringIO()
        file.write("\n")

        writer = sphinxter.Writer(document, file)

        writer.document.add("people", "module", test.test_sphinxter.test_reader.TestReader.MODULE, 0)

        writer.document.add("stuff", "function", test.test_sphinxter.test_reader.TestReader.FUNCTION, 20)

        writer.document.add("things", "exception", test.test_sphinxter.test_reader.TestReader.BASIC_EXCEPTION, 10)

        writer.dump()

        self.assertEqual(file.getvalue(), """
.. created by sphinxter
.. default-domain:: py

test.example
============

.. module:: test.example

mod me

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

.. currentmodule:: things

.. exception:: Basic

    Basic Exception

.. currentmodule:: stuff

.. function:: func(a: int, b: 'str', *args, **kwargs)

    Some basic func

    :param a: The a More stuff
    :type a: int
    :param b: The b
    :type b: str
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

        self.assertSphinxter(sphinxter.Writer.dump, transform=[True, False])
