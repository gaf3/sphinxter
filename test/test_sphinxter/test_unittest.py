import unittest
import unittest.mock

import yaml

import sphinxter
import sphinxter.unittest
import test.example
import test.test_sphinxter.test_reader


class TestCodeException(unittest.TestCase):

    maxDiff = None

    @unittest.mock.patch("traceback.format_exception")
    def test___init__(self, mock_trace):

        mock_trace.return_value = ["ya\n", "sure\n"]

        exception = sphinxter.unittest.CodeException("oops", "people\nstuff\nthings")

        self.assertEqual(str(exception), "ya\nsure\n1: people\n2: stuff\n3: things")


class TestBlock(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        block = sphinxter.unittest.Block(["fee", "fie"], [])

        self.assertEqual(block.code, "fee\nfie")
        self.assertIsNone(block.value)
        self.assertFalse(block.valued)

        block = sphinxter.unittest.Block(["fee", "fie"], ["foe", "fum"])

        self.assertEqual(block.code, "fee\nfie")
        self.assertEqual(block.value, "foe\nfum")

    def test_exec(self):

        # single

        block = sphinxter.unittest.Block(["a = 1"], ["1"])

        locals = {}

        self.assertEqual(block.exec(locals), 1)
        self.assertEqual(locals, {})

        # multiple

        block = sphinxter.unittest.Block(["a = 1", "b = a"], ["1"])

        locals = {}

        self.assertEqual(block.exec(locals), 1)
        self.assertEqual(locals, {
            "a": 1
        })

        # bad parse

        block = sphinxter.unittest.Block(["a ="], [""])

        self.assertRaisesRegex(sphinxter.unittest.CodeException, "SyntaxError", block.exec, {})

        # bad exec

        block = sphinxter.unittest.Block(["a = b", "b"], ["c"])

        self.assertRaisesRegex(sphinxter.unittest.CodeException, "NameError", block.exec, {})

        # bad eval

        block = sphinxter.unittest.Block(["b"], ["c"])

        self.assertRaisesRegex(sphinxter.unittest.CodeException, "NameError", block.exec, {})

    def test_eval(self):

        # bool

        block = sphinxter.unittest.Block([], ["True"])
        self.assertEqual(block.eval({}), True)

        # str

        block = sphinxter.unittest.Block([], ["'yep'"])
        self.assertEqual(block.eval({}), "yep")

        # int

        block = sphinxter.unittest.Block([], ["1"])
        self.assertEqual(block.eval({}), 1)

        # list

        block = sphinxter.unittest.Block([], ["[1]"])
        self.assertEqual(block.eval({}), [1])

        # dict

        block = sphinxter.unittest.Block([], ['{"a": b}'])
        self.assertEqual(block.eval({"b": 2}), {"a": 2})

        # bad eval

        block = sphinxter.unittest.Block(["b"], ["c"])

        self.assertRaisesRegex(sphinxter.unittest.CodeException, "NameError", block.eval, {})

class TestSection(sphinxter.unittest.TestCase):

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

        docstring = yaml.safe_load(self.DOCSTRING)

        self.assertEqual(sphinxter.unittest.Section.parse(docstring["usage"]), self.PARSE)

        self.assertSphinxter(sphinxter.unittest.Section.parse, evaluate=False)

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

        blocks = sphinxter.unittest.Section.chunk(self.PARSE.rstrip())

        self.assertEqual(blocks[0].code, self.BLOCK_0_CODE)
        self.assertEqual(blocks[0].value, self.BLOCK_0_VALUE)
        self.assertEqual(blocks[1].code, self.BLOCK_1_CODE)
        self.assertEqual(blocks[1].value, self.BLOCK_1_VALUE)

        self.assertSphinxter(sphinxter.unittest.Section.chunk, evaluate=False)

    def test___init__(self):

        section = sphinxter.unittest.Section(yaml.safe_load(self.DOCSTRING)["usage"])

        self.assertEqual(section.code, self.PARSE)
        self.assertEqual(len(section.blocks), 2)
        self.assertEqual(section.blocks[0].code, self.BLOCK_0_CODE)
        self.assertEqual(section.blocks[0].value, self.BLOCK_0_VALUE)
        self.assertEqual(section.blocks[1].code, self.BLOCK_1_CODE)
        self.assertEqual(section.blocks[1].value, self.BLOCK_1_VALUE)


class TestTestCase(sphinxter.unittest.TestCase):

    def test_sphinxter(self):

        self.assertEqual(self.sphinxter(test.example), test.test_sphinxter.test_reader.TestReader.MODULE)

        self.assertEqual(self.sphinxter(test.example.Basic), test.test_sphinxter.test_reader.TestReader.BASIC_EXCEPTION)

        self.assertEqual(self.sphinxter(test.example.Complex), test.test_sphinxter.test_reader.TestReader.COMPLEX_CLASS)

        self.assertEqual(self.sphinxter(test.example.func)["description"], test.test_sphinxter.test_reader.TestReader.FUNCTION["description"])

        self.assertEqual(self.sphinxter(test.example.Complex.stat)["description"], test.test_sphinxter.test_reader.TestReader.STATICMETHOD["description"])

        self.assertEqual(self.sphinxter(test.example.Complex.classy)["description"], test.test_sphinxter.test_reader.TestReader.CLASSMETHOD["description"])

        self.assertEqual(self.sphinxter(test.example.Complex.meth)["description"], test.test_sphinxter.test_reader.TestReader.METHOD["description"])

        self.assertRaisesRegex(Exception, "Unknown resource: False", self.sphinxter, False)

        self.assertSphinxter(sphinxter.unittest.TestCase.sphinxter)

    def test_assertSphinxterBlock(self):

        with unittest.mock.patch("unittest.TestCase.assertEqual") as mock_equal:

            # not valued

            block = sphinxter.unittest.Block(["a = 1"], [])

            self.assertSphinxterBlock(block)

            mock_equal.assert_not_called()

            # success

            block = sphinxter.unittest.Block(["a = 1"], ["1"])

            self.assertSphinxterBlock(block)

            mock_equal.assert_called_once_with(1, 1, None)

            # fail

            block = sphinxter.unittest.Block(["a = 1"], ["2"])

            self.assertSphinxterBlock(block)

            mock_equal.assert_called_with(2, 1, "Correct value:\n# 1")

            # bool

            block = sphinxter.unittest.Block(["1 == 2"], [])
            block.value = True
            block.valued = True

            self.assertSphinxterBlock(block, comment="nope", evaluate=False)

            mock_equal.assert_called_with(True, False, "nope\nCorrect value:\n# False")

            # str

            block = sphinxter.unittest.Block(["a = 'yep'"], ["nope"])

            self.assertSphinxterBlock(block, evaluate=False)

            mock_equal.assert_called_with("nope", "yep", "Correct value:\n# yep")

            # evaluate

            evaluate = {
                "yep": [False]
            }

            self.assertSphinxterBlock(block, comment="yep", evaluate=evaluate)

            mock_equal.assert_called_with("nope", "yep", "yep\nCorrect value:\n# yep")

        self.assertEqual(evaluate, {
            "yep": []
        })


    class Convert:
        """
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

    class Leave:
        """
        usage: |
            Yo yo yo::

                a = "yep"

            Hoo boy::

                a
                # nope
        """

    @unittest.mock.patch("unittest.TestCase.assertEqual")
    def test_assertSphinxterSection(self, mock_equal):

        # as is

        section = sphinxter.unittest.Section(yaml.safe_load(self.Leave.__doc__)["usage"])

        self.assertSphinxterSection(section, "dude", evaluate=False)

        mock_equal.assert_called_with("nope", "yep", 'dude\nCorrect value:\n# yep')

        # section

        section = sphinxter.unittest.Section(yaml.safe_load(self.Convert.__doc__)["usage"])

        self.assertSphinxterSection(section, "dude")

        mock_equal.assert_called_with({"a": 2}, {"a": 1}, 'dude\nCorrect value:\n# {\n#     "a": 1\n# }')

        # str

        mock_equal.reset_mock()

        self.assertSphinxterSection(yaml.safe_load(self.Convert.__doc__)["usage"], "dude")

        mock_equal.assert_called_with({"a": 2}, {"a": 1}, 'dude\nCorrect value:\n# {\n#     "a": 1\n# }')

        # list

        self.assertSphinxterSection([yaml.safe_load(self.Convert.__doc__)["usage"]], "dude")

        mock_equal.assert_called_with({"a": 2}, {"a": 1}, 'dude[0]\nCorrect value:\n# {\n#     "a": 1\n# }')

        # dict

        self.assertSphinxterSection({"a": yaml.safe_load(self.Convert.__doc__)["usage"]}, "dude")

        mock_equal.assert_called_with({"a": 2}, {"a": 1}, 'dude.a\nCorrect value:\n# {\n#     "a": 1\n# }')

    @unittest.mock.patch("unittest.TestCase.assertEqual")
    def test_assertSphinxter(self, mock_equal):

        self.assertSphinxter(self.Convert)

        mock_equal.assert_has_calls([
            unittest.mock.call(1, 1, 'Convert.usage'),
            unittest.mock.call({"a": 2}, {"a": 1}, 'Convert.usage\nCorrect value:\n# {\n#     "a": 1\n# }')
        ])
