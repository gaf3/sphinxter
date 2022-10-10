.. created by sphinxter
.. default-domain:: py

sphinxter.unittest
==================

.. module:: sphinxter.unittest

Module for testing examples

.. class:: Block(code: str, value: str)

    Class for storing a block

    :param code: The code of the block
    :type code: str
    :param value: The value of the block
    :type value: str

    .. attribute:: code
        :type: str

        The code of the block

    .. attribute:: value

        The value of the block

    .. method:: eval(locals: dict)

        Evalucates the value and returns it. If it can't compile, assumes the value is a string

        :param locals: locals vars already set
        :type locals: dict

    .. method:: exec(locals: dict)

        Executes the code and returns the last value

        :param locals: locals vars already set
        :type locals: dict

.. class:: Example(name, docstring)

    Class for verifying example code

    :param name:
    :param docstring:

    .. staticmethod:: chunk(code)

        Breaks code up into blocks

        :param code:

    .. staticmethod:: parse(name, docstring)

        Pulls all example code

        :param name:
        :param docstring:

.. class:: TestCase

    Extended unittest.TestCase with asserts for testing examples

    .. method:: assertBlock(block: sphinxter.unittest.Block, comment=None, transform=True)

        Asserts a block of code matches it's value

        :param block: Block to evauluate
        :type block: Block
        :param comment:
        :param transform:

    .. method:: assertExample(example, comment=None)

        Asserts a block of code matches it's value

        :param example:
        :param comment:
