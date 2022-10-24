.. created by sphinxter
.. default-domain:: py

sphinxter.unittest
==================

.. module:: sphinxter.unittest

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

.. class:: TestCase

    Extends unittest.TestCase with asserts for testing examples

    .. method:: assertSphinxter(resource, evaluate=True)

        Recurseivly asserts all Sections in documentation match their values using assertSphinxterSection and adding to the comment to show where.

        If the values in the comments are all the exact code, evaulate should be True.

        If the values in the comment are all text, evaulate should be False.

        If the values in the comments, vary, you can send a list or a dict.

        If evaulate is a list, each call to assertSphinxterBlock, pops the next value to use off the front.

        If evaulate is a dict, each call to assertSphinxterBlock will use the current location as the key to the comment

        .. warning::

            This method pops values off the evaluate list. That means the evaluate value will be modified by this method.

        :param resource: Resource to assert has valid code exanmples
        :type resource: module or class or function or method
        :param evaluate: Whether values are to be eval'd
        :type evaluate: bool or list or dict

    .. method:: assertSphinxterBlock(block: sphinxter.unittest.Block, comment: str = None, evaluate=True)

        Asserts a Block of code matches its value using assertEqual and adding to the comment to show where.

        If the value in the comments are the exact code, evaulate should be True.

        If the value in the comment are text, evaulate should be False.

        The evaluate argument can also be a list, where the next evaluate value will be popped off.

        The evaluate argument can also be a dict, where the evaluate value will be extracted use the comment as a the key.

        This is done to work with assertSphinxterSection and assertSphinxter.

        .. warning::

            This method pops values off the evaluate list. That means the evaluate value will be modified by this method.

        :param block: Block to assert has valid code
        :type block: Block
        :param comment: Comment to use with assertEqual, will be appended to with bad code location
        :type comment: str
        :param evaluate: Whether values are to be eval'd
        :type evaluate: bool or list or dict

    .. method:: assertSphinxterSection(section, comment: str = None, evaluate=True)

        Recurseivly asserts all Blocks in a Section match their values using assertSphinxterBlock and adding to the comment to show where.

        If the values in the comments are all the exact code, evaulate should be True.

        If the values in the comment are all text, evaulate should be False.

        If the values in the comments, vary, you can send a list or a dict.

        If evaulate is a list, each call to assertSphinxterBlock, pops the next value to use off the front.

        If evaulate is a dict, each call to assertSphinxterBlock will use the current location as the key to the comment

        .. warning::

            This method pops values off the evaluate list. That means the evaluate value will be modified by this method.

        :param section: Section to assert has valid code
        :type section: Section or str or list or dict
        :param comment: Comment to use with assertEqual, will be appended to with bad code location
        :type comment: str
        :param evaluate: Whether values are to be eval'd
        :type evaluate: bool or list or dict

    .. staticmethod:: sphinxter(resource) -> dict

        Reads approximate documntation from any resource.

        .. warning::

            Do not use this method to generate documentation. The documentation is
            approximate since methods don't know they're part of a class but this
            is sufficient to make sure all executable code can be found and checked.

        :param resource: Resource to parse documentation for
        :type resource: module or class or function or method
        :rtype: dict

        **Usage**

        Given the following function is in the test.example module::

            def func(
                a:int,   # The a
                b:'str', # The b
                *args,   #
                **kwargs # a: 1
                        # b: 2
            ):
                """
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
                """

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
            #     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            # }

.. class:: Section(text: str)

    Class for verifying example code

    :param text: The full section to parse and chunk
    :type text: str

    .. attribute:: blocks
        :type: list[aphinxter.unittest.Block]

        Comparable blocks in the code

    .. attribute:: code

        The extraced executable postion of the section

    .. staticmethod:: chunk(code)

        Breaks code up into blocks by commented values to compare.

        :param code:

        **Usage**

        Given the source function in sphinxter.Reader::

            class Reader:
                """
                description: Static class for reading doc strings and comments into dict's
                document: reader
                """

                @staticmethod
                def source(
                    resource # what to extract the source from
                ):
                    """
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
                                    \"""
                                    Sub class
                                    \"""

                                    pass

                        The source for Subber would be indented from inspect.getsource()
                        which can't be parsed properly because of the initial indent::

                            import inspect
                            import test.example

                            inspect.getsource(test.example.Complex.Subber)
                            #     class Subber:
                            #         \"""
                            #         Sub class
                            #         \"""
                            #         pass
                            #

                        This prevents that problem::

                            import sphinxter
                            import test.example

                            sphinxter.Reader.source(test.example.Complex.Subber)
                            # class Subber:
                            #     \"""
                            #     Sub class
                            #     \"""
                            #     pass
                            #
                    """

        This pulls out the code::

            import yaml
            import sphinxter
            import sphinxter.unittest

            documentation = yaml.safe_load(sphinxter.Reader.source.__doc__)
            usage = sphinxter.unittest.Section.parse(documentation['usage'])
            # class Complex:
            #
            #     class Subber:
            #         """
            #         Sub class
            #         """
            #
            #         pass
            #
            # import inspect
            # import test.example
            #
            # inspect.getsource(test.example.Complex.Subber)
            # #     class Subber:
            # #         """
            # #         Sub class
            # #         """
            # #         pass
            # #
            #
            # import sphinxter
            # import test.example
            #
            # sphinxter.Reader.source(test.example.Complex.Subber)
            # # class Subber:
            # #     """
            # #     Sub class
            # #     """
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
            #         """
            #         Sub class
            #         """
            #
            #         pass
            #
            # import inspect
            # import test.example
            #
            # inspect.getsource(test.example.Complex.Subber)

            blocks[0].value
            #     class Subber:
            #         """
            #         Sub class
            #         """
            #         pass
            #

        The second block includes the first, plus the sphinxter value::

            blocks[1].code
            # class Complex:
            #
            #     class Subber:
            #         """
            #         Sub class
            #         """
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
            #     """
            #     Sub class
            #     """
            #     pass
            #

        In both cases, to validate usage, we can execuate the code and compare it to the value.

    .. staticmethod:: parse(text)

        Pulls all example code into a single block.

        :param text:

        **Usage**

        Given the source function in sphinxter.Reader::

            class Reader:
                """
                description: Static class for reading doc strings and comments into dict's
                document: reader
                """

                @staticmethod
                def source(
                    resource # what to extract the source from
                ):
                    """
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
                                    \"""
                                    Sub class
                                    \"""

                                    pass

                        The source for Subber would be indented from inspect.getsource()
                        which can't be parsed properly because of the initial indent::

                            import inspect
                            import test.example

                            inspect.getsource(test.example.Complex.Subber)
                            #     class Subber:
                            #         \"""
                            #         Sub class
                            #         \"""
                            #         pass
                            #

                        This prevents that problem::

                            import sphinxter
                            import test.example

                            sphinxter.Reader.source(test.example.Complex.Subber)
                            # class Subber:
                            #     \"""
                            #     Sub class
                            #     \"""
                            #     pass
                            #
                    """

        This will just pull out the executable code from the usage secton::

            import yaml
            import sphinxter
            import sphinxter.unittest

            documentation = yaml.safe_load(sphinxter.Reader.source.__doc__)
            sphinxter.unittest.Section.parse(documentation['usage'])
            # class Complex:
            #
            #     class Subber:
            #         """
            #         Sub class
            #         """
            #
            #         pass
            #
            # import inspect
            # import test.example
            #
            # inspect.getsource(test.example.Complex.Subber)
            # #     class Subber:
            # #         """
            # #         Sub class
            # #         """
            # #         pass
            # #
            #
            # import sphinxter
            # import test.example
            #
            # sphinxter.Reader.source(test.example.Complex.Subber)
            # # class Subber:
            # #     """
            # #     Sub class
            # #     """
            # #     pass
            # #
            #

.. class:: Block(code: str, value: str)

    Class for storing a block, a pair for code to execute and (optional) value to compare to

    :param code: The code of the block
    :type code: str
    :param value: The value of the block
    :type value: str

    .. attribute:: code
        :type: str

        The code of the block

    .. attribute:: value
        :type: str

        The value of the block

    .. attribute:: valued
        :type: bool

        Whether this block has a value

        Only blocks with values in

    .. method:: eval(locals: dict)

        Evaluates the value and returns it.

        :param locals: locals vars already set
        :type locals: dict
        :raises CodeException: If any part of the value can't be compiled or executed

    .. method:: exec(locals: dict)

        Executes the code and returns the last value if valued

        :param locals: locals vars already set
        :type locals: dict
        :raises CodeException: If any part of the code can't be compiled or executed

.. exception:: CodeException(exception: Exception, code: str)

    Exception for failed code.

    Creates a message based on the full trace of the original exception plus
    the code that failed to execute, including line numbers.

    This is to make it very clear when verifying examples what went wrong and
    where.

    :param exception: the original exception
    :type exception: Exception
    :param code: the code that failed
    :type code: str
