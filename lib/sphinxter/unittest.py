"""
description: Module for testing examples
document: unittest
"""

# pylint: disable=exec-used,eval-used

import re
import ast
import json
import yaml
import unittest


class Block:
    """
    description: Class for storing a block
    document: unittest
    """

    code = None     # The code of the block
    "type: str"
    value = None    # The value of the block

    def __init__(self,
        code:str, # The code of the block
        value:str # The value of the block
    ):

        if isinstance(code, list):
            code = "\n".join(code)

        if isinstance(value, list):
            value = "\n".join(value)

        self.code = code
        self.value = value

    def exec(self,
        locals:dict    # locals vars already set
    ):
        """
        Executes the code and returns the last value
        """

        statements = list(ast.iter_child_nodes(ast.parse(self.code)))

        last = statements.pop()

        if statements:
            exec(compile(ast.Module(body=statements, type_ignores=[]), filename="<ast>", mode="exec"), {}, locals)

        if isinstance(last, ast.Assign):
            last = last.value

        return eval(ast.unparse(last), {}, locals)

    def eval(self,
        locals:dict    # locals vars already set
    ):
        """
        Evalucates the value and returns it. If it can't compile, assumes the value is a string
        """

        return eval(self.value, {}, locals)


class Example:
    """
    description: Class for verifying example code
    document: unittest
    """

    @staticmethod
    def parse(name, docstring):
        """
        Pulls all example code
        """

        area = yaml.safe_load(docstring)[name]

        text = []
        indent = None
        code = False

        for line in area.split("\n"):

            if line.endswith("::"):
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
                text.append(line.replace(indent, '', 1))

        return "\n".join(text)

    @staticmethod
    def chunk(code):
        """
        Breaks code up into blocks
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

    def __init__(self, name, docstring):

        self.name = name
        self.docstring = docstring
        self.code = self.parse(name, self.docstring)
        self.blocks = self.chunk(self.code)


class TestCase(unittest.TestCase):
    """
    description: Extended unittest.TestCase with asserts for testing examples
    document: unittest
    """

    def assertBlock(self,
        block:Block,    # Block to evauluate
        comment=None,
        transform=True
    ):
        """
        Asserts a block of code matches it's value
        """

        locals = {}
        actual = block.exec(locals)
        expected = block.eval(locals) if transform else block.value

        if expected != actual:

            if isinstance(actual, bool):
                correct = str(actual)
            elif isinstance(actual, str) and not transform:
                correct = actual
            else:
                correct = json.dumps(actual, indent=4, sort_keys=True)

            correction = [comment] if comment is not None else []

            correction.append("Correct value:")

            for line in correct.split("\n"):
                correction.append(f"# {line}")

            comment = "\n".join(correction)

        self.assertEqual(expected, actual, comment)

    def assertExample(self, example, comment=None):
        """
        Asserts a block of code matches it's value
        """

        for block in example.blocks:
            self.assertBlock(block, comment)
