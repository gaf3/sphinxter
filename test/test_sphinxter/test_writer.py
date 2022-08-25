import unittest
import unittest.mock

import io

import sphinxter
from test import example
from test.test_sphinxter.test_reader import TestReader

class TestWriter(unittest.TestCase):

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

        .. staticmethod:: stat(a, b, *args, **kwargs) -> list

            Some static stat

            :param a: The a More stuff
            :param b: The b
            :param args:
            :param kwargs:
            :return: things
            :rtype: list
""")

    def test_module(self):

        self.writer.module(TestReader.MODULE, 1)
        self.assertEqual(self.file.getvalue(), """

    .. module:: test.example

    mod me

    .. attribute:: a

        The a team

    .. attribute:: b

        The b team

        Not as good as the a team

    .. attribute:: big

        Bunch a
""")

    def test_toctree(self):

        self.writer.toctree(['*'], 1)

        self.assertEqual(self.file.getvalue(), """

    .. toctree::
        :maxdepth: 1
        :glob:
        :hidden:

        *
""")

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

    .. staticmethod:: stat(a, b, *args, **kwargs) -> list

        Some static stat

        :param a: The a More stuff
        :param b: The b
        :param args:
        :param kwargs:
        :return: things
        :rtype: list
"""

    def test_dump(self):

        # actual

        self.writer.document = sphinxter.Document(None, "test.example", ['self', '*'], '    ')

        self.writer.document.add("test.example", "module", TestReader.MODULE, 0)

        self.writer.document.add("test.example", "function", TestReader.FUNCTION, 0)

        self.writer.document.add("test.example", "class", TestReader.BASIC_CLASS, 0)

        self.writer.document.add("test.example", "class", TestReader.COMPLEX_CLASS, 0)

        self.writer.dump()

        self.assertEqual(self.file.getvalue(), self.EXAMPLE)

        # modules

        document = sphinxter.Document(None, "test.example", False, '    ')
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

test.example
============

.. module:: test.example

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
