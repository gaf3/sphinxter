import unittest
import unittest.mock

import io

import sphinxter
import sphinxter.unittest
from test import example


class TestBlock(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        block = sphinxter.unittest.Block(["fee", "fie"], ["foe", "fum"])

        self.assertEqual(block.code, "fee\nfie")
        self.assertEqual(block.value, "foe\nfum")

    def test_exec(self):

        # single

        block = sphinxter.unittest.Block(["a = 1"], None)

        locals = {}

        self.assertEqual(block.exec(locals), 1)
        self.assertEqual(locals, {})

        # multiple

        block = sphinxter.unittest.Block(["a = 1", "b = a"], None)

        locals = {}

        self.assertEqual(block.exec(locals), 1)
        self.assertEqual(locals, {
            "a": 1
        })

    def test_eval(self):

        # bool

        block = sphinxter.unittest.Block(None, "True")
        self.assertEqual(block.eval({}), True)

        # str

        block = sphinxter.unittest.Block(None, "'yep'")
        self.assertEqual(block.eval({}), "yep")

        # int

        block = sphinxter.unittest.Block(None, "1")
        self.assertEqual(block.eval({}), 1)

        # list

        block = sphinxter.unittest.Block(None, "[1]")
        self.assertEqual(block.eval({}), [1])

        # dict

        block = sphinxter.unittest.Block(None, '{"a": b}')
        self.assertEqual(block.eval({"b": 2}), {"a": 2})


class TestExample(unittest.TestCase):

    DOCSTRING = """
description: Reads the source, removing any overall indent
parameters:
    resource:
        type:
        - module
        - function
        - class
        - method
return:
    description: The non-indented source
    type: str
usage: |
    If you have a subclass like::

        class Complex:

            class Subber:

                pass

    The source for Subber would be indented from inspect.getsource()
    which can't be parsed properly because of the initial indent::

        inspect.getsource(Complex.Subber)
        #     class Subber:
        #
        #         pass

    This prevents that problem::

        sphinxter.Reader.source(Complex.Subber)
        # class Subber:
        #
        #     pass
"""

    PARSE = """class Complex:

    class Subber:

        pass

inspect.getsource(Complex.Subber)
#     class Subber:
#
#         pass

sphinxter.Reader.source(Complex.Subber)
# class Subber:
#
#     pass
"""

    def test_parse(self):

        self.assertEqual(sphinxter.unittest.Example.parse("usage", self.DOCSTRING), self.PARSE)

    BLOCK_0_CODE = """class Complex:

    class Subber:

        pass

inspect.getsource(Complex.Subber)"""

    BLOCK_0_VALUE = """    class Subber:

        pass"""

    BLOCK_1_CODE = """class Complex:

    class Subber:

        pass

inspect.getsource(Complex.Subber)

sphinxter.Reader.source(Complex.Subber)"""

    BLOCK_1_VALUE = """class Subber:

    pass"""

    def test_chunk(self):

        blocks = sphinxter.unittest.Example.chunk(self.PARSE.rstrip())

        self.assertEqual(blocks[0].code, self.BLOCK_0_CODE)
        self.assertEqual(blocks[0].value, self.BLOCK_0_VALUE)
        self.assertEqual(blocks[1].code, self.BLOCK_1_CODE)
        self.assertEqual(blocks[1].value, self.BLOCK_1_VALUE)

    def test___init__(self):

        example = sphinxter.unittest.Example("usage", self.DOCSTRING)

        self.assertEqual(example.name, "usage")
        self.assertEqual(example.docstring, self.DOCSTRING)
        self.assertEqual(example.code, self.PARSE)
        self.assertEqual(len(example.blocks), 2)
        self.assertEqual(example.blocks[0].code, self.BLOCK_0_CODE)
        self.assertEqual(example.blocks[0].value, self.BLOCK_0_VALUE)
        self.assertEqual(example.blocks[1].code, self.BLOCK_1_CODE)
        self.assertEqual(example.blocks[1].value, self.BLOCK_1_VALUE)


class TestTestCase(sphinxter.unittest.TestCase):

    @unittest.mock.patch("unittest.TestCase.assertEqual")
    def test_assertBlock(self, mock_equal):

        # success

        block = sphinxter.unittest.Block("a = 1", "1")

        self.assertBlock(block)

        mock_equal.assert_called_once_with(1, 1, None)

        # fail

        block = sphinxter.unittest.Block("a = 1", "2")

        self.assertBlock(block)

        mock_equal.assert_called_with(2, 1, "Correct value:\n# 1")

        # bool

        block = sphinxter.unittest.Block("1 == 2", True)

        self.assertBlock(block, comment="nope", transform=False)

        mock_equal.assert_called_with(True, False, "nope\nCorrect value:\n# False")

        # str

        block = sphinxter.unittest.Block("a = 'yep'", "nope")

        self.assertBlock(block, transform=False)

        mock_equal.assert_called_with("nope", "yep", "Correct value:\n# yep")

    DOCSTRING = """
usage: |
    Yo yo yo::

        a = 1
        b = {
            "a": 1
        }

    Hoo boy::

        a
        # 1

    Tiki bar::

        b
        # {
        #     "a": 2
        # }
"""

    @unittest.mock.patch("unittest.TestCase.assertEqual")
    def test_assertExample(self, mock_equal):

        example = sphinxter.unittest.Example("usage", self.DOCSTRING)

        self.assertExample(example, "dude")

        mock_equal.assert_called_with({"a": 2}, {"a": 1}, 'dude\nCorrect value:\n# {\n#     "a": 1\n# }')
