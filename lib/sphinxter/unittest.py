"""
description: Module for testing examples
document: unittest
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

    def __init__(self, exception, code):

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
    description: Class for storing a block
    document: unittest
    """

    code = None     # The code of the block
    "type: str"
    value = None    # The value of the block
    valued = False  # Whether this block has a value

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
        Executes the code and returns the last value
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
        Evalucates the value and returns it. If it can't compile, assumes the value is a string
        """

        try:
            return eval(self.value, {}, locals)
        except Exception as exception:
            raise CodeException(exception, self.value)


class Section:
    """
    description: Class for verifying example code
    document: unittest
    """

    @staticmethod
    def parse(text):
        """
        Pulls all example code
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

    def __init__(self, text):

        self.code = self.parse(text)
        self.blocks = self.chunk(self.code)


class TestCase(unittest.TestCase):
    """
    description: Extended unittest.TestCase with asserts for testing examples
    document: unittest
    """

    def sphinxter(self,
        resource
    )->dict:
        """
        description: Reads documntation from any resource
        """

        if inspect.ismodule(resource):
            return sphinxter.Reader.module(resource)

        if inspect.isclass(resource):
            return sphinxter.Reader.cls(resource)

        if inspect.isroutine(resource):
            return sphinxter.Reader.routine(resource)

        raise Exception(f"Unknown resource: {resource}")

    def assertSphinxterBlock(self,
        block:Block,    # Block to evauluate
        comment=None,
        transform=True
    ):
        """
        Asserts a block of code matches it's value
        """

        locals = {}

        actual = block.exec(locals)

        if not block.valued:
            return

        if isinstance(transform, dict) and comment in transform:
            transform = transform[comment]

        if isinstance(transform, list):
            transform = transform.pop(0)

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

            comment = "\n".join(correction).replace("\\", "\\\\")

        self.assertEqual(expected, actual, comment)

    def assertSphinxterSection(self, section, comment=None, transform=True):
        """
        Asserts a section is valid
        """

        if isinstance(section, Section):

            for block in section.blocks:
                self.assertSphinxterBlock(block, comment=comment, transform=transform)

        elif isinstance(section, str) and "\n" in section and "::" in section:

            self.assertSphinxterSection(Section(section), comment=comment, transform=transform)

        elif isinstance(section, list):

            for index, item in enumerate(section):
                self.assertSphinxterSection(item, comment=f"{comment}[{index}]", transform=transform)

        elif isinstance(section, dict):

            for name, item in section.items():
                if name not in ["methods", "classes", "exceptions"]:
                    self.assertSphinxterSection(item, comment=f"{comment}.{name}", transform=transform)

    def assertSphinxter(self, resource, transform=True):
        """
        Asserts a block of code matches it's value
        """

        documentation = self.sphinxter(resource)

        self.assertSphinxterSection(documentation, resource.__name__, transform=transform)
