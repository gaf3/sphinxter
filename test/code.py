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


def dual():
    """
    definition: |
        Here is some code with an examples that need to be eval'd::

            2 + 2
            # 4
    usage: |
        Here is some code with an example that needs to not be eval'd:::

            "\\n".join(['1', '2', '3'])
            # 1
            # 2
            # 3
    """


def mixing():
    """
    evalme: |
        Here is some code with an examples that need to be eval'd::

            2 + 2
            # 4
    leaveme: |
        Here is some code with an example that needs to not be eval'd:::

            "\\n".join(['1', '2', '3'])
            # 1
            # 2
            # 3
    mixme: |
        Here's some code that has both eval no eval examples::

            2 + 2
            # 4

            "\\n".join(['1', '2', '3'])
            # 1
            # 2
            # 3
    """


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

                "\\n".join(['1', '2', '3'])
                # 1
                # 2
                # 3
    """
