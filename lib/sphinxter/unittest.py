"""
document: unittest
description: |
    Module for testing examples.

    If you have code examples in your documentation yourresource, like so::

        2 + 2
        # 4

    You want to make sure they're accurate. This module does exactly that. In your unittests,
    you can verify that the code will execute and even verify the values put in comments
    after a line match the value returned by that line.

    All you need to do is extend the sphinxter.unittest.TestCase and use assertSphinxter::

        import sphinxter.unittest

        import yourmodule

        class TestYourModule(sphinxter.unittest.TestCase):

            maxDiff = None

            def test_yourresource(self):

                self.assertSphinxter(yourmodule.yourresource)

    That'll look throughthe documentation, find execution example, and run them, compiling
    even the comments directly on the next line and verifying the match the line before.
"""

# pylint: disable=exec-used,eval-used

import re
import ast
import json
import inspect
import traceback
import unittest
import sphinxter

class CodeException(Exception):
    """
    description: |
        Exception for failed code.

        Creates a message based on the full trace of the original exception plus
        the code that failed to execute, including line numbers.

        This is to make it very clear when verifying examples what went wrong and
        where.
    document: 30
    """

    def __init__(self,
        exception:Exception,    # the original exception
        code:str                # the code that failed
    ):


        trace = "".join(traceback.format_exception(exception))

        lines = []
        number = 0

        for line in code.split("\n"):
            number += 1
            lines.append(f"{number}: {line}")

        lined = "\n".join(lines)

        super().__init__(f"{trace}{lined}")


class Block:
    """
    description: Class for storing a block, a pair for code to execute and (optional) value to compare to
    document: 20
    """

    code = None     # The code of the block
    "type: str"
    value = None    # The value of the block
    "type: str"
    valued = False  # Whether this block has a value
    """
        description: Only blocks with values in # are valued
        type: bool
    """

    def __init__(self,
        code:str, # The code of the block
        value:str # The value of the block
    ):

        self.code = "\n".join(code)

        if value:

            self.value = "\n".join(value)
            self.valued = True

    def exec(self,
        locals:dict    # locals vars already set
    ):
        """
        description: Executes the code and returns the last value if valued
        raises:
            CodeException: If any part of the code can't be compiled or executed
        """

        try:
            statements = list(ast.iter_child_nodes(ast.parse(self.code)))
        except Exception as exception:
            raise CodeException(exception, self.code)

        last = None

        if self.valued:
            last = statements.pop()

        if statements:

            code = ast.Module(body=statements, type_ignores=[])
            try:
                exec(compile(code, filename="<ast>", mode="exec"), {}, locals)
            except Exception as exception:
                raise CodeException(exception, ast.unparse(code))

        if last is not None:

            if isinstance(last, ast.Assign):
                last = last.value

            code = ast.unparse(last)

            try:
                return eval(code, {}, locals)
            except Exception as exception:
                raise CodeException(exception, code)

    def eval(self,
        locals:dict    # locals vars already set
    ):
        """
        description: Evaluates the value and returns it.
        raises:
            CodeException: If any part of the value can't be compiled or executed
        """

        try:
            return eval(self.value, {}, locals)
        except Exception as exception:
            raise CodeException(exception, self.value)


class Section:
    """
    description: Class for verifying example code
    document: 10
    """

    @staticmethod
    def parse(text):
        """
        description: Pulls all example code into a single block.
        usage: |
            Given the source function in sphinxter.Reader::

                class Reader:
                    \"""
                    description: Static class for reading doc strings and comments into dict's
                    document: reader
                    \"""

                    @staticmethod
                    def source(
                        resource # what to extract the source from
                    ):
                        \"""
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
                            Consider the sub class in a test.example module::

                                class Complex:

                                    class Subber:
                                        \\\"""
                                        Sub class
                                        \\\"""

                                        pass

                            The source for Subber would be indented from inspect.getsource()
                            which can't be parsed properly because of the initial indent::

                                import inspect
                                import test.example

                                inspect.getsource(test.example.Complex.Subber)
                                #     class Subber:
                                #         \\\"""
                                #         Sub class
                                #         \\\"""
                                #         pass
                                #

                            This prevents that problem::

                                import sphinxter
                                import test.example

                                sphinxter.Reader.source(test.example.Complex.Subber)
                                # class Subber:
                                #     \\\"""
                                #     Sub class
                                #     \\\"""
                                #     pass
                                #
                        \"""

            This will just pull out the executable code from the usage secton::

                import yaml
                import sphinxter
                import sphinxter.unittest

                documentation = yaml.safe_load(sphinxter.Reader.source.__doc__)
                sphinxter.unittest.Section.parse(documentation['usage'])
                # class Complex:
                #
                #     class Subber:
                #         \"""
                #         Sub class
                #         \"""
                #
                #         pass
                #
                # import inspect
                # import test.example
                #
                # inspect.getsource(test.example.Complex.Subber)
                # #     class Subber:
                # #         \"""
                # #         Sub class
                # #         \"""
                # #         pass
                # #
                #
                # import sphinxter
                # import test.example
                #
                # sphinxter.Reader.source(test.example.Complex.Subber)
                # # class Subber:
                # #     \"""
                # #     Sub class
                # #     \"""
                # #     pass
                # #
                #
        """

        lines = []
        indent = None
        code = False

        for line in text.split("\n"):

            if line.endswith("::") and not line.endswith(".. note::") and not line.startswith(" "):
                code = True
                indent = None
                continue

            if code and line and indent is None:
                indent = re.split(r'\S', line, 1)[0]

            if code and line and indent is not None and not line.startswith(indent):
                code = False
                indent = None
                continue

            if code and indent:
                lines.append(line.replace(indent, '', 1))

        return "\n".join(lines)

    @staticmethod
    def chunk(code):
        """
        description: Breaks code up into blocks by commented values to compare.
        usage: |
            Given the source function in sphinxter.Reader::

                class Reader:
                    \"""
                    description: Static class for reading doc strings and comments into dict's
                    document: reader
                    \"""

                    @staticmethod
                    def source(
                        resource # what to extract the source from
                    ):
                        \"""
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
                            Consider the sub class in a test.example module::

                                class Complex:

                                    class Subber:
                                        \\\"""
                                        Sub class
                                        \\\"""

                                        pass

                            The source for Subber would be indented from inspect.getsource()
                            which can't be parsed properly because of the initial indent::

                                import inspect
                                import test.example

                                inspect.getsource(test.example.Complex.Subber)
                                #     class Subber:
                                #         \\\"""
                                #         Sub class
                                #         \\\"""
                                #         pass
                                #

                            This prevents that problem::

                                import sphinxter
                                import test.example

                                sphinxter.Reader.source(test.example.Complex.Subber)
                                # class Subber:
                                #     \\\"""
                                #     Sub class
                                #     \\\"""
                                #     pass
                                #
                        \"""

            This pulls out the code::

                import yaml
                import sphinxter
                import sphinxter.unittest

                documentation = yaml.safe_load(sphinxter.Reader.source.__doc__)
                usage = sphinxter.unittest.Section.parse(documentation['usage'])
                # class Complex:
                #
                #     class Subber:
                #         \"""
                #         Sub class
                #         \"""
                #
                #         pass
                #
                # import inspect
                # import test.example
                #
                # inspect.getsource(test.example.Complex.Subber)
                # #     class Subber:
                # #         \"""
                # #         Sub class
                # #         \"""
                # #         pass
                # #
                #
                # import sphinxter
                # import test.example
                #
                # sphinxter.Reader.source(test.example.Complex.Subber)
                # # class Subber:
                # #     \"""
                # #     Sub class
                # #     \"""
                # #     pass
                # #
                #

            And this breaks it up into Blocks, that can each be evaluated::

                blocks = sphinxter.unittest.Section.chunk(usage)

            The first block is up to the inspect value::

                blocks[0].code
                # class Complex:
                #
                #     class Subber:
                #         \"""
                #         Sub class
                #         \"""
                #
                #         pass
                #
                # import inspect
                # import test.example
                #
                # inspect.getsource(test.example.Complex.Subber)

                blocks[0].value
                #     class Subber:
                #         \"""
                #         Sub class
                #         \"""
                #         pass
                #

            The second block includes the first, plus the sphinxter value::

                blocks[1].code
                # class Complex:
                #
                #     class Subber:
                #         \"""
                #         Sub class
                #         \"""
                #
                #         pass
                #
                # import inspect
                # import test.example
                #
                # inspect.getsource(test.example.Complex.Subber)
                #
                # import sphinxter
                # import test.example
                #
                # sphinxter.Reader.source(test.example.Complex.Subber)

                blocks[1].value
                # class Subber:
                #     \"""
                #     Sub class
                #     \"""
                #     pass
                #

            In both cases, to validate usage, we can execuate the code and compare it to the value.
        """

        state = "block"
        block = []
        value = []
        blocks = []

        for line in code.split("\n"):

            if state == "blank" and line.strip():
                state = "block"

            if state == "block":
                if line.startswith("#"):
                    state = "value"
                elif not line.strip():
                    state = "blank"
            elif state == "value" and not line.startswith("#"):
                blocks.append(Block(block, value))
                state = "block"
                value = []

            if state in ["block", "blank"]:
                block.append(line)
            elif state == "value":
                value.append(line[2:])

        if value:
            blocks.append(Block(block, value))

        return blocks

    code = None     # The extraced executable postion of the section
    blocks = None   # Comparable blocks in the code
    "type: list[aphinxter.unittest.Block]"

    def __init__(self,
        text:str    # The full section to parse and chunk
    ):

        self.code = self.parse(text)
        self.blocks = self.chunk(self.code)


class TestCase(unittest.TestCase):
    """
    description: Extends unittest.TestCase with asserts for testing examples
    document: 0
    """

    @staticmethod
    def sphinxter(
        resource    # Resource to parse documentation for
    )->dict:
        """
        description: |
            Reads approximate documntation from any resource.

            .. warning::

                Do not use this method to generate documentation. The documentation is
                approximate since methods don't know they're part of a class but this
                is sufficient to make sure all executable code can be found and checked.
        parameters:
            resource:
                type:
                - module
                - class
                - function
                - method
        usage: |
            Given the following function is in the test.example module::

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    \"""
                    description: Some basic func
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type:
                        - str
                        - None
                    raises:
                        Exception: if oh noes
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    \"""

            We can get the approximate documentation like so::

                import sphinxter.unittest

                import test.example

                sphinxter.unittest.TestCase.sphinxter(test.example.func)
                # {
                #     "description": "Some basic func",
                #     "kind": "function",
                #     "name": "func",
                #     "parameters": [
                #         {
                #             "description": "The a More stuff",
                #             "name": "a",
                #             "type": "int"
                #         },
                #         {
                #             "description": "The b",
                #             "more": "stuff",
                #             "name": "b",
                #             "type": "str"
                #         },
                #         {
                #             "name": "args"
                #         },
                #         {
                #             "a": 1,
                #             "b": 2,
                #             "name": "kwargs"
                #         }
                #     ],
                #     "raises": {
                #         "Exception": "if oh noes"
                #     },
                #     "return": {
                #         "description": "things",
                #         "type": [
                #             "str",
                #             "None"
                #         ]
                #     },
                #     "signature": "(a: int, b: 'str', *args, **kwargs)",
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }
        """

        if inspect.ismodule(resource):
            return sphinxter.Reader.module(resource)

        if inspect.isclass(resource):
            return sphinxter.Reader.cls(resource)

        if inspect.isroutine(resource):
            return sphinxter.Reader.routine(resource)

        raise Exception(f"Unknown resource: {resource}")

    def assertSphinxterBlock(self,
        block:Block,        # Block to assert has valid code
        comment:str=None,   # Comment to use with assertEqual, will be appended to with bad code location
        evaluate=True       # Whether values are to be eval'd
    ):
        """
        description: |
            Asserts a Block of code matches its value using assertEqual and adding to the comment to show where.

            If the value in the comments are the exact code, evaulate should be True.

            If the value in the comment are text, evaulate should be False.

            The evaluate argument can also be a list, where the next evaluate value will be popped off.

            The evaluate argument can also be a dict, where the evaluate value will be extracted use the comment as a the key.

            This is done to work with assertSphinxterSection and assertSphinxter.

            .. warning::

                This method pops values off the evaluate list. That means the evaluate value will be modified by this method.
        parameters:
            evaluate:
                type:
                - bool
                - list
                - dict
        """

        locals = {}

        actual = block.exec(locals)

        if not block.valued:
            return

        if isinstance(evaluate, dict) and comment in evaluate:
            evaluate = evaluate[comment]

        if isinstance(evaluate, list):
            evaluate = evaluate.pop(0)

        expected = block.eval(locals) if evaluate else block.value

        if expected != actual:

            if isinstance(actual, bool):
                correct = str(actual)
            elif isinstance(actual, str) and not evaluate:
                correct = actual
            else:
                correct = json.dumps(actual, indent=4, sort_keys=True)

            correction = [comment] if comment is not None else []

            correction.append("Correct value:")

            for line in correct.split("\n"):
                correction.append(f"# {line}")

            comment = "\n".join(correction).replace("\\", "\\\\").replace('"""', '\\"""')

        self.assertEqual(expected, actual, comment)

    def assertSphinxterSection(self,
        section,            # Section to assert has valid code
        comment:str=None,   # Comment to use with assertEqual, will be appended to with bad code location
        evaluate=True       # Whether values are to be eval'd
    ):
        """
        description: |
            Recurseivly asserts all Blocks in a Section match their values using assertSphinxterBlock and adding to the comment to show where.

            If the values in the comments are all the exact code, evaulate should be True.

            If the values in the comment are all text, evaulate should be False.

            If the values in the comments, vary, you can send a list or a dict.

            If evaulate is a list, each call to assertSphinxterBlock, pops the next value to use off the front.

            If evaulate is a dict, each call to assertSphinxterBlock will use the current location as the key to the comment

            .. warning::

                This method pops values off the evaluate list. That means the evaluate value will be modified by this method.
        parameters:
            section:
                type:
                - Section
                - str
                - list
                - dict
            evaluate:
                type:
                - bool
                - list
                - dict
        """

        if isinstance(section, Section):

            for block in section.blocks:
                self.assertSphinxterBlock(block, comment=comment, evaluate=evaluate)

        elif isinstance(section, str) and "\n" in section and "::" in section:

            self.assertSphinxterSection(Section(section), comment=comment, evaluate=evaluate)

        elif isinstance(section, list):

            for index, item in enumerate(section):
                self.assertSphinxterSection(item, comment=f"{comment}[{index}]", evaluate=evaluate)

        elif isinstance(section, dict):

            for name, item in section.items():
                if name not in ["methods", "classes", "exceptions"]:
                    self.assertSphinxterSection(item, comment=f"{comment}.{name}", evaluate=evaluate)

    def assertSphinxter(self,
        resource,       # Resource to assert has valid code exanmples
        evaluate=True   # Whether values are to be eval'd
    ):
        """
        description: |
            Recurseivly asserts all Sections in documentation match their values using assertSphinxterSection and adding to the comment to show where.

            If the values in the comments are all the exact code, evaulate should be True.

            If the values in the comment are all text, evaulate should be False.

            If the values in the comments, vary, you can send a list or a dict.

            If evaulate is a list, each call to assertSphinxterBlock, pops the next value to use off the front.

            If evaulate is a dict, each call to assertSphinxterBlock will use the current location as the key to the comment

            .. warning::

                This method pops values off the evaluate list. That means the evaluate value will be modified by this method.
        parameters:
            resource:
                type:
                - module
                - class
                - function
                - method
            evaluate:
                type:
                - bool
                - list
                - dict
        """

        documentation = self.sphinxter(resource)

        self.assertSphinxterSection(documentation, resource.__name__, evaluate=evaluate)
