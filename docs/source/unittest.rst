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

That'll look through the documentation, find execution example, and run them, compiling
even the comments directly on the next line and verifying the match the line before.

.. class:: TestCase

    Extends unittest.TestCase with asserts for testing examples

    .. method:: assertSphinxter(resource, evaluate=True)

        Recurseivly asserts all Sections in documentation match their values using assertSphinxterSection and adding to the location to show where.

        If the values in the comments are all the exact code, evaulate should be True.

        If the values in the comments are all text, evaulate should be False.

        If the values in the comments, vary, you can send a list or a dict.

        If evaulate is a list, each call to assertSphinxterBlock, pops the next value to use off the front.

        If evaulate is a dict, each call to assertSphinxterBlock will use the current location as the key to the location

        .. warning::

            This method pops values off the evaluate list. That means the evaluate value will be modified by this method.

        :param resource: Resource to assert has valid code exanmples
        :type resource: module or class or function or method
        :param evaluate: Whether values are to be eval'd
        :type evaluate: bool or list or dict

        **Usage**

        Given the follwing function is in the test.code module::

            def depth():
                """
                deepme:
                    evalme: |
                        All eval'd::

                            2 + 2
                            # 4

                            "Hello" + " " + "world"
                            # "Hello world"
                    mixme: |
                        Lil of both::
                            2 + 2
                            # 4

                            "\n".join(['1', '2', '3'])
                            # 1
                            # 2
                            # 3
                """

        You would test the whole thing like so::

            import sphinxter.unittest

            import test.code

            class TestDepth(sphinxter.unittest.TestCase):

                def test_all(self):

                    self.assertSphinxter(test.code.depth, evaluate={
                        "deepme.evalme": True,
                        "deepme.mixme": [True, False]
                    })

        Notice the evaluate argument. All off evalme is to be eval'd, so we just set that section to True.

        In the mixme section, the first is tobe eval'd, the second not, so we just set that section to [True, False].

        And we can see that it works::

            import unittest

            import test.test_code

            unittest.TextTestRunner().run(unittest.makeSuite(test.test_code.TestDepth)).wasSuccessful()
            # True

    .. method:: assertSphinxterBlock(block: sphinxter.unittest.Block, location: str = None, evaluate=True)

        Asserts a Block of code matches its value using assertEqual and adding to the location to show where.

        If the value in the comments are the exact code, evaulate should be True.

        If the value in the comments are text, evaulate should be False.

        The evaluate argument can also be a list, where the next evaluate value will be popped off.

        The evaluate argument can also be a dict, where the evaluate value will be extracted use the location as a the key.

        This is done to work with assertSphinxterSection and assertSphinxter.

        .. warning::

            This method pops values off the evaluate list. That means the evaluate value will be modified by this method.

        :param block: Block to assert has valid code
        :type block: Block
        :param location: Comment to use with assertEqual, will be appended to with bad code location
        :type location: str
        :param evaluate: Whether values are to be eval'd
        :type evaluate: bool or list or dict

        **Usage**

        Give the follwing function is in the test.code module::

            def dual():
                """
                definition: |
                    Here is some code with an examples that need to be eval'd::

                        2 + 2
                        # 4
                usage: |
                    Here is some code with an example that needs to not be eval'd:::

                        "\n".join(['1', '2', '3'])
                        # 1
                        # 2
                        # 3
                """

        You would test the blocka individually like so in the test.test_code module::

            import sphinxter.unittest

            import test.code

            class TestDual(sphinxter.unittest.TestCase):

                maxDiff = None

                def test_definition(self):

                    text = self.sphinxter(test.code.dual)["definition"]
                    section = sphinxter.unittest.Section(text)
                    self.assertSphinxterBlock(section.blocks[0])

                def test_usage(self):

                    text = self.sphinxter(test.code.dual)["usage"]
                    section = sphinxter.unittest.Section(text)
                    self.assertSphinxterBlock(section.blocks[0], evaluate=False)

        And we can see that it works::

            import unittest

            import test.test_code

            unittest.TextTestRunner().run(unittest.makeSuite(test.test_code.TestDual)).wasSuccessful()
            # True

    .. method:: assertSphinxterSection(section, location: str = None, evaluate=True)

        Recurseivly asserts all Blocks in a Section match their values using assertSphinxterBlock and adding to the location to show where.

        If the values in the comments are all the exact code, evaulate should be True.

        If the values in the comments are all text, evaulate should be False.

        If the values in the comments, vary, you can send a list or a dict.

        If evaulate is a list, each call to assertSphinxterBlock, pops the next value to use off the front.

        If evaulate is a dict, each call to assertSphinxterBlock will use the current location as the key to the location

        .. warning::

            This method pops values off the evaluate list. That means the evaluate value will be modified by this method.

        :param section: Section to assert has valid code
        :type section: Section or str or list or dict
        :param location: Comment to use with assertEqual, will be appended to with bad code location
        :type location: str
        :param evaluate: Whether values are to be eval'd
        :type evaluate: bool or list or dict

        **Usage**

        Give the follwing function is in the test.code module::

            def mixing():
                """
                evalme: |
                    Here is some code with an examples that need to be eval'd::

                        2 + 2
                        # 4
                leaveme: |
                    Here is some code with an example that needs to not be eval'd:::

                        "\n".join([1, 2, 3])
                        # 1
                        # 2
                        # 3
                mixme: |
                    Here's some code that has both eval no eval examples::

                        2 + 2
                        # 4

                        "\n".join([1, 2, 3])
                        # 1
                        # 2
                        # 3
                """

        You would test each section individually like so::

            import sphinxter.unittest

            import test.code

            class TestMixing(sphinxter.unittest.TestCase):

                maxDiff = None

                def test_evalme(self):

                    text = self.sphinxter(test.code.mixing)["evalme"]
                    section = sphinxter.unittest.Section(text)
                    self.assertSphinxterSection(section)

                def test_leaveme(self):

                    text = self.sphinxter(test.code.mixing)["leaveme"]
                    section = sphinxter.unittest.Section(text)
                    self.assertSphinxterSection(section, evaluate=False)

                def test_mixme(self):

                    text = self.sphinxter(test.code.mixing)["mixme"]
                    section = sphinxter.unittest.Section(text)
                    self.assertSphinxterSection(section, evaluate=[True, False])

        Notice the evaluate argument for mixme. The first block is to be evaluated, the second, not.

        And we can see that it works::

            import unittest

            import test.test_code

            unittest.TextTestRunner().run(unittest.makeSuite(test.test_code.TestMixing)).wasSuccessful()
            # True

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

        Given the following function is in the test.code module::

            def basic():
                """
                usage: |
                    Here is some code with an examples that need to be eval'd::

                        2 + 2
                        # 4

                    Even strings::

                        "Hello" + " " + "world"
                        # "Hello world"
                """

        We can get the approximate documentation like so::

            import sphinxter.unittest

            import test.code

            sphinxter.unittest.TestCase.sphinxter(test.code.basic)
            # {
            #     "kind": "function",
            #     "name": "basic",
            #     "signature": "()",
            #     "usage": "Here is some code with an examples that need to be eval'd::\n\n    2 + 2\n    # 4\n\nEven strings::\n\n    \"Hello\" + \" \" + \"world\"\n    # \"Hello world\"\n"
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

        Given the function in test.code::

            def basic():
                """
                usage: |
                    Here is some code with an examples that need to be eval'd::

                        2 + 2
                        # 4

                    Even strings::

                        "Hello" + " " + "world"
                        # "Hello world"
                """

        This will just pull out the executable code from the usage secton::

            import yaml
            import sphinxter.unittest

            import test.code

            documentation = yaml.safe_load(test.code.basic.__doc__)
            usage = sphinxter.unittest.Section.parse(documentation['usage'])
            # 2 + 2
            # # 4
            #
            # "Hello" + " " + "world"
            # # "Hello world"
            #

        And this breaks it up into Blocks, that can each be evaluated::

            blocks = sphinxter.unittest.Section.chunk(usage)

        The first block is up to the equation value::

            blocks[0].code
            # 2 + 2

            blocks[0].value
            # 4

        The second block includes the first, plus the concatenation::

            blocks[1].code
            # 2 + 2
            #
            # "Hello" + " " + "world"

            blocks[1].value
            # "Hello world"

        In both cases, to validate usage, we can execuate the code and compare it to the value.

    .. staticmethod:: parse(text)

        Pulls all example code into a single block.

        :param text:

        **Usage**

        Given the function in test.code::

            def basic():
                """
                usage: |
                    Here is some code with an examples that need to be eval'd::

                        2 + 2
                        # 4

                    Even strings::

                        "Hello" + " " + "world"
                        # "Hello world"
                """

        This will just pull out the executable code from the usage secton::

            import yaml
            import sphinxter.unittest

            import test.code

            documentation = yaml.safe_load(test.code.basic.__doc__)
            sphinxter.unittest.Section.parse(documentation['usage'])
            # 2 + 2
            # # 4
            #
            # "Hello" + " " + "world"
            # # "Hello world"
            #

.. class:: Block(code: list, value: list)

    Class for storing a block, a pair for code to execute and (optional) value to compare to

    :param code: The code of the block
    :type code: list
    :param value: The value of the block
    :type value: list

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
