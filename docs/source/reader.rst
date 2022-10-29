.. created by sphinxter
.. default-domain:: py

sphinxter.Reader
================

.. currentmodule:: sphinxter

.. class:: Reader

    Static class for reading doc strings and comments into dict's

    .. staticmethod:: annotations(resource) -> dict

        Read annotations in a format better for updating

        :param resource: what to extract annotations from
        :type resource: function or method
        :return: dict of annotations, with parameters and return keys
        :rtype: dict

        **Usage**

        You can use regular annotations and they can be extracted to
        update information about parameters and functions/methods
        themelves.

        Say this code is in the test.example module::

            def func(
                a:int,   # The a
                b:'str', # The b
                *args,   #
                **kwargs # a: 1
                         # b: 2
            ):
                pass

        You can extra the annotations like so::

            import sphinxter
            import test.example

            sphinxter.Reader.annotations(test.example.func)
            # {
            #     "parameters": {
            #         "a": {
            #             "type": "int"
            #         },
            #         "b": {
            #             "type": "str"
            #         }
            #     },
            #     "return": {}
            # }

    .. classmethod:: attributes(resource) -> dict

        Read attributes from a module or class, including their comments and docstrings

        :param resource: what to extract attributes from
        :type resource: function or method
        :rtype: dict

        **Usage**

        If you have attributes on a module, say the test.example module::

            a = None # The a team
            b = None # The b team
            """
            Not as good as the a team
            """
            big = """
            Stuff
            """ # Bunch a
            """
            a: 1
            b: 2
            """

        You can extract/combime the descriptions and/or YAML like so::

            import sphinxter
            import test.example

            sphinxter.Reader.attributes(test.example)
            # {
            #     "a": {
            #         "description": "The a team"
            #     },
            #     "b": {
            #         "description": "The b team\n\nNot as good as the a team"
            #     },
            #     "big": {
            #         "a": 1,
            #         "b": 2,
            #         "description": "Bunch a"
            #     }
            # }

        This works the same for a class, say the Complex class in the test.example module::

            class Complex:

                a = None # The a team
                b = None # The b team
                """
                Not as good as the a team
                """
                big = """
                Stuff
                """ # Bunch a
                """
                a: 1
                b: 2
                """

        Extracting is just as easy::

            import sphinxter
            import test.example

            sphinxter.Reader.attributes(test.example.Complex)
            # {
            #     "a": {
            #         "description": "The a team"
            #     },
            #     "b": {
            #         "description": "The b team\n\nNot as good as the a team"
            #     },
            #     "big": {
            #         "a": 1,
            #         "b": 2,
            #         "description": "Bunch a"
            #     }
            # }

    .. classmethod:: cls(resource) -> dict

        Reads all the documentation from a class for :any:`Writer.cls`

        :param resource: what to extract documentation from
        :type resource: class
        :rtype: dict

        **Usage**

        Given this class is part of the test.example module::

            class Complex:
                """
                description: Complex class
                definition: |
                    make sure you do this::

                        wowsa

                    Ya sweet
                """

                a = None # The a team
                b = None # The b team
                """
                Not as good as the a team
                """
                big = """
                Stuff
                """ # Bunch a
                """
                a: 1
                b: 2
                """

                def __init__(
                    self,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: call me
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    """

                @staticmethod
                def stat(
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                )->list:
                    """
                    description: Some static stat
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return: things
                    """

                @classmethod
                def classy(
                    cls,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: Some class meth
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type: str
                    """

                def meth(
                    self,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: Some basic meth
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

                class Subber:
                    """
                    Sub class
                    """
                    pass

                class Excepter(Exception):
                    """
                    Sub exception
                    """
                    pass

        Reading all the documentation is as easy as::

            import sphinxter
            import test.example

            sphinxter.Reader.cls(test.example.Complex)
            # {
            #     "attributes": [
            #         {
            #             "description": "The a team",
            #             "name": "a"
            #         },
            #         {
            #             "description": "The b team\n\nNot as good as the a team",
            #             "name": "b"
            #         },
            #         {
            #             "a": 1,
            #             "b": 2,
            #             "description": "Bunch a",
            #             "name": "big"
            #         }
            #     ],
            #     "classes": [
            #         {
            #             "attributes": [],
            #             "classes": [],
            #             "description": "Sub class",
            #             "exceptions": [],
            #             "kind": "class",
            #             "methods": [],
            #             "name": "Subber"
            #         }
            #     ],
            #     "definition": "make sure you do this::\n\n    wowsa\n\nYa sweet\n",
            #     "description": "Complex class\n\ncall me",
            #     "exceptions": [
            #         {
            #             "attributes": [],
            #             "classes": [],
            #             "description": "Sub exception",
            #             "exceptions": [],
            #             "kind": "exception",
            #             "methods": [],
            #             "name": "Excepter"
            #         }
            #     ],
            #     "kind": "class",
            #     "methods": [
            #         {
            #             "description": "Some class meth",
            #             "kind": "classmethod",
            #             "name": "classy",
            #             "parameters": [
            #                 {
            #                     "description": "The a More stuff",
            #                     "name": "a"
            #                 },
            #                 {
            #                     "description": "The b",
            #                     "more": "stuff",
            #                     "name": "b"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "a": 1,
            #                     "b": 2,
            #                     "name": "kwargs"
            #                 }
            #             ],
            #             "return": {
            #                 "description": "things",
            #                 "type": "str"
            #             },
            #             "signature": "(a, b, *args, **kwargs)"
            #         },
            #         {
            #             "description": "Some basic meth",
            #             "kind": "method",
            #             "name": "meth",
            #             "parameters": [
            #                 {
            #                     "description": "The a More stuff",
            #                     "name": "a"
            #                 },
            #                 {
            #                     "description": "The b",
            #                     "more": "stuff",
            #                     "name": "b"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "a": 1,
            #                     "b": 2,
            #                     "name": "kwargs"
            #                 }
            #             ],
            #             "raises": {
            #                 "Exception": "if oh noes"
            #             },
            #             "return": {
            #                 "description": "things",
            #                 "type": [
            #                     "str",
            #                     "None"
            #                 ]
            #             },
            #             "signature": "(a, b, *args, **kwargs)",
            #             "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #         },
            #         {
            #             "description": "Some static stat",
            #             "kind": "staticmethod",
            #             "name": "stat",
            #             "parameters": [
            #                 {
            #                     "description": "The a More stuff",
            #                     "name": "a"
            #                 },
            #                 {
            #                     "description": "The b",
            #                     "more": "stuff",
            #                     "name": "b"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "a": 1,
            #                     "b": 2,
            #                     "name": "kwargs"
            #                 }
            #             ],
            #             "return": {
            #                 "description": "things",
            #                 "type": "list"
            #             },
            #             "signature": "(a, b, *args, **kwargs) -> list"
            #         }
            #     ],
            #     "name": "Complex",
            #     "parameters": [
            #         {
            #             "description": "The a More stuff",
            #             "name": "a"
            #         },
            #         {
            #             "description": "The b",
            #             "more": "stuff",
            #             "name": "b"
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
            #     "signature": "(a, b, *args, **kwargs)",
            #     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            # }

        Notfice that the __init__ method documentation has been super imposed over the class documentation.

        Say we're still inthe test.example module::

            class Basic(Exception):
                """
                Basic Exception
                """

        If a class is exception, it'll capture that::

            import sphinxter
            import test.example

            sphinxter.Reader.cls(test.example.Basic)
            # {
            #     "attributes": [],
            #     "classes": [],
            #     "description": "Basic Exception",
            #     "exceptions": [],
            #     "kind": "exception",
            #     "methods": [],
            #     "name": "Basic"
            # }

    .. classmethod:: comments(resource) -> dict

        Reads parameters comments from a function or method

        :param resource: what to read the parameter comments from
        :type resource: function or method
        :return: dict of parsed comments, keyed by parameter
        :rtype: dict

        **Usage**

        You can put comments after parameters in a function or method and they
        can be parsed as YAML, just like a docstring.

        Say this code is in the test.example module::

            def func(
                a:int,   # The a
                b:'str', # The b
                *args,   #
                **kwargs # a: 1
                         # b: 2
            ):
                pass

        You can extra the comments like so::

            import sphinxter
            import test.example

            sphinxter.Reader.comments(test.example.func)
            # {
            #     "a": {
            #         "description": "The a"
            #     },
            #     "args": {},
            #     "b": {
            #         "description": "The b"
            #     },
            #     "kwargs": {
            #         "a": 1,
            #         "b": 2
            #     }
            # }

    .. classmethod:: module(resource) -> dict

        Reads all the documentation from a module for :any:`Writer.module`

        :param resource: what to extract documentation from
        :type resource: module
        :rtype: dict

        **Usage**

        Say the following is the test.example module::

            """
            description: mod me
            usage: |
                Do some cool stuff::

                    like this

                It's great
            """

            a = None # The a team
            b = None # The b team
            """
            Not as good as the a team
            """
            big = """
            Stuff
            """ # Bunch a
            """
            a: 1
            b: 2
            """

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


            class Basic(Exception):
                """
                Basic Exception
                """


            class Complex:
                """
                description: Complex class
                definition: |
                    make sure you do this::

                        wowsa

                    Ya sweet
                """

                a = None # The a team
                b = None # The b team
                """
                Not as good as the a team
                """
                big = """
                Stuff
                """ # Bunch a
                """
                a: 1
                b: 2
                """

                def __init__(
                    self,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: call me
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    """

                @staticmethod
                def stat(
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                )->list:
                    """
                    description: Some static stat
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return: things
                    """

                @classmethod
                def classy(
                    cls,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: Some class meth
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type: str
                    """

                def meth(
                    self,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: Some basic meth
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

                class Subber:
                    """
                    Sub class
                    """
                    pass

                class Excepter(Exception):
                    """
                    Sub exception
                    """
                    pass

        Reading all the documentation is as easy as::

            import sphinxter
            import test.example

            sphinxter.Reader.module(test.example)
            # {
            #     "attributes": [
            #         {
            #             "description": "The a team",
            #             "name": "a"
            #         },
            #         {
            #             "description": "The b team\n\nNot as good as the a team",
            #             "name": "b"
            #         },
            #         {
            #             "a": 1,
            #             "b": 2,
            #             "description": "Bunch a",
            #             "name": "big"
            #         }
            #     ],
            #     "classes": [
            #         {
            #             "attributes": [
            #                 {
            #                     "description": "The a team",
            #                     "name": "a"
            #                 },
            #                 {
            #                     "description": "The b team\n\nNot as good as the a team",
            #                     "name": "b"
            #                 },
            #                 {
            #                     "a": 1,
            #                     "b": 2,
            #                     "description": "Bunch a",
            #                     "name": "big"
            #                 }
            #             ],
            #             "classes": [
            #                 {
            #                     "attributes": [],
            #                     "classes": [],
            #                     "description": "Sub class",
            #                     "exceptions": [],
            #                     "kind": "class",
            #                     "methods": [],
            #                     "name": "Subber"
            #                 }
            #             ],
            #             "definition": "make sure you do this::\n\n    wowsa\n\nYa sweet\n",
            #             "description": "Complex class\n\ncall me",
            #             "exceptions": [
            #                 {
            #                     "attributes": [],
            #                     "classes": [],
            #                     "description": "Sub exception",
            #                     "exceptions": [],
            #                     "kind": "exception",
            #                     "methods": [],
            #                     "name": "Excepter"
            #                 }
            #             ],
            #             "kind": "class",
            #             "methods": [
            #                 {
            #                     "description": "Some class meth",
            #                     "kind": "classmethod",
            #                     "name": "classy",
            #                     "parameters": [
            #                         {
            #                             "description": "The a More stuff",
            #                             "name": "a"
            #                         },
            #                         {
            #                             "description": "The b",
            #                             "more": "stuff",
            #                             "name": "b"
            #                         },
            #                         {
            #                             "name": "args"
            #                         },
            #                         {
            #                             "a": 1,
            #                             "b": 2,
            #                             "name": "kwargs"
            #                         }
            #                     ],
            #                     "return": {
            #                         "description": "things",
            #                         "type": "str"
            #                     },
            #                     "signature": "(a, b, *args, **kwargs)"
            #                 },
            #                 {
            #                     "description": "Some basic meth",
            #                     "kind": "method",
            #                     "name": "meth",
            #                     "parameters": [
            #                         {
            #                             "description": "The a More stuff",
            #                             "name": "a"
            #                         },
            #                         {
            #                             "description": "The b",
            #                             "more": "stuff",
            #                             "name": "b"
            #                         },
            #                         {
            #                             "name": "args"
            #                         },
            #                         {
            #                             "a": 1,
            #                             "b": 2,
            #                             "name": "kwargs"
            #                         }
            #                     ],
            #                     "raises": {
            #                         "Exception": "if oh noes"
            #                     },
            #                     "return": {
            #                         "description": "things",
            #                         "type": [
            #                             "str",
            #                             "None"
            #                         ]
            #                     },
            #                     "signature": "(a, b, *args, **kwargs)",
            #                     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #                 },
            #                 {
            #                     "description": "Some static stat",
            #                     "kind": "staticmethod",
            #                     "name": "stat",
            #                     "parameters": [
            #                         {
            #                             "description": "The a More stuff",
            #                             "name": "a"
            #                         },
            #                         {
            #                             "description": "The b",
            #                             "more": "stuff",
            #                             "name": "b"
            #                         },
            #                         {
            #                             "name": "args"
            #                         },
            #                         {
            #                             "a": 1,
            #                             "b": 2,
            #                             "name": "kwargs"
            #                         }
            #                     ],
            #                     "return": {
            #                         "description": "things",
            #                         "type": "list"
            #                     },
            #                     "signature": "(a, b, *args, **kwargs) -> list"
            #                 }
            #             ],
            #             "name": "Complex",
            #             "parameters": [
            #                 {
            #                     "description": "The a More stuff",
            #                     "name": "a"
            #                 },
            #                 {
            #                     "description": "The b",
            #                     "more": "stuff",
            #                     "name": "b"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "a": 1,
            #                     "b": 2,
            #                     "name": "kwargs"
            #                 }
            #             ],
            #             "signature": "(a, b, *args, **kwargs)",
            #             "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #         }
            #     ],
            #     "description": "mod me",
            #     "exceptions": [
            #         {
            #             "attributes": [],
            #             "classes": [],
            #             "description": "Basic Exception",
            #             "exceptions": [],
            #             "kind": "exception",
            #             "methods": [],
            #             "name": "Basic"
            #         }
            #     ],
            #     "functions": [
            #         {
            #             "description": "Some basic func",
            #             "kind": "function",
            #             "name": "func",
            #             "parameters": [
            #                 {
            #                     "description": "The a More stuff",
            #                     "name": "a",
            #                     "type": "int"
            #                 },
            #                 {
            #                     "description": "The b",
            #                     "more": "stuff",
            #                     "name": "b",
            #                     "type": "str"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "a": 1,
            #                     "b": 2,
            #                     "name": "kwargs"
            #                 }
            #             ],
            #             "raises": {
            #                 "Exception": "if oh noes"
            #             },
            #             "return": {
            #                 "description": "things",
            #                 "type": [
            #                     "str",
            #                     "None"
            #                 ]
            #             },
            #             "signature": "(a: int, b: 'str', *args, **kwargs)",
            #             "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #         }
            #     ],
            #     "name": "test.example",
            #     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            # }

    .. staticmethod:: parse(docstring: str) -> dict

        Parses a docstring into YAML, defaulting to description

        :param docstring: the docstring (or string after an attribute)
        :type docstring: str
        :return: The parsed doctring
        :rtype: dict

        **Usage**

        If you just have a plain docstring, it'll return a dict
        with that docstring as the description::

            import sphinxter

            def plain():
                """
                A plain function
                """

            sphinxter.Reader.parse(plain.__doc__)
            # {
            #     "description": "A plain function"
            # }

        If you have straight YAML it's return that as is::

            def exact():
                """
                description: An exact function
                """

            sphinxter.Reader.parse(exact.__doc__)
            # {
            #     "description": "An exact function"
            # }

        If the string is blank, it'll return an empty dict::

            sphinxter.Reader.parse("")
            # {}

    .. classmethod:: routine(resource, method: bool = False) -> dict

        Reads all the documentation from a function or method for :any:`Writer.function` or :any:`Writer.method`

        Of special note is parameters. What's returned at the key of "parameters" is a list of dictionaries. But
        when specifiying parameter in the YAML, use a dict keyed by parameter name. The signature information
        is updated from the parameter comments and then from the dict in the YAML. If descriptions are specified
        in both areas, they'll be joined witha space, the signature comment going first.

        :param resource: what to read from
        :type resource: function or method
        :param method: whether this is a method
        :type method: bool
        :return: dict of routine documentation
        :rtype: dict

        **Usage**

        .. note::

            This expects resources from inspect.getattr_static(), not getattr() and
            not directly off modules or classes or instances.

        Say this function is part of the test.example module::

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

        Reading all the documentation for a function is as easy as::

            import inspect
            import sphinxter
            import test.example

            sphinxter.Reader.routine(inspect.getattr_static(test.example, 'func'))
            # {
            #     "name": "func",
            #     "kind": "function",
            #     "description": "Some basic func",
            #     "signature": "(a: int, b: 'str', *args, **kwargs)",
            #     "parameters": [
            #         {
            #             "name": "a",
            #             "description": "The a More stuff",
            #             "type": "int"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b",
            #             "more": "stuff",
            #             "type": "str"
            #         },
            #         {
            #             "name": "args"
            #         },
            #         {
            #             "name": "kwargs",
            #             "a": 1,
            #             "b": 2
            #         }
            #     ],
            #     "return": {
            #         "description": "things",
            #         "type": [
            #             'str',
            #             'None'
            #         ]
            #     },
            #     "raises": {
            #         "Exception": "if oh noes"
            #     },
            #     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            # }

        Methods aren't much different, and include a method key, that's either '', 'class', or 'static'.

        Assume we're still in the test.example module and have this class::

            class Complex:

                def __init__(
                    self,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: call me
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    """

                @staticmethod
                def stat(
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                             # b: 2
                )->list:
                    """
                    description: Some static stat
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return: things
                    """

                @classmethod
                def classy(
                    cls,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                             # b: 2
                ):
                    """
                    description: Some class meth
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type: str
                    """

                def meth(
                    self,
                    a,       # The a
                    b,       # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    """
                    description: Some basic meth
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

        Extract the documentation for each like so::

            import inspect
            import sphinxter
            import test.example

            sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'stat'), method=True)
            # {
            #     "name": "stat",
            #     "kind": "staticmethod",
            #     "description": "Some static stat",
            #     "signature": "(a, b, *args, **kwargs) -> list",
            #     "parameters": [
            #         {
            #             "name": "a",
            #             "description": "The a More stuff"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b",
            #             "more": "stuff"
            #         },
            #         {
            #             "name": "args"
            #         },
            #         {
            #             "name": "kwargs",
            #             "a": 1,
            #             "b": 2
            #         }
            #     ],
            #     "return": {
            #         "description": "things",
            #         "type": "list"
            #     }
            # }

            sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'classy'), method=True)
            # {
            #     "name": "classy",
            #     "kind": "classmethod",
            #     "description": "Some class meth",
            #     "signature": "(a, b, *args, **kwargs)",
            #     "parameters": [
            #         {
            #             "name": "a",
            #             "description": "The a More stuff"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b",
            #             "more": "stuff"
            #         },
            #         {
            #             "name": "args"
            #         },
            #         {
            #             "name": "kwargs",
            #             "a": 1,
            #             "b": 2
            #         }
            #     ],
            #     "return": {
            #         "description": "things",
            #         "type": 'str'
            #     }
            # }

            sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'meth'), method=True)
            # {
            #     "name": "meth",
            #     "kind": "method",
            #     "description": "Some basic meth",
            #     "signature": "(a, b, *args, **kwargs)",
            #     "parameters": [
            #         {
            #             "name": "a",
            #             "description": "The a More stuff"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b",
            #             "more": "stuff"
            #         },
            #         {
            #             "name": "args"
            #         },
            #         {
            #             "name": "kwargs",
            #             "a": 1,
            #             "b": 2
            #         }
            #     ],
            #     "return": {
            #         "description": "things",
            #         "type": [
            #             'str',
            #             'None'
            #         ]
            #     },
            #     "raises": {
            #         "Exception": "if oh noes"
            #     },
            #     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            # }

    .. staticmethod:: source(resource)

        Reads the source, removing any overall indent

        :param resource: what to extract the source from
        :type resource: module or function or class or method
        :return: The non-indented source
        :rtype: str

        **Usage**

        Consider the sub class in a test.example module::

            class Complex:

                class Subber:
                    """
                    Sub class
                    """

                    pass

        The source for Subber would be indented from inspect.getsource()
        which can't be parsed properly because of the initial indent::

            import inspect
            import test.example

            inspect.getsource(test.example.Complex.Subber)
            #     class Subber:
            #         """
            #         Sub class
            #         """
            #         pass
            #

        This prevents that problem::

            import sphinxter
            import test.example

            sphinxter.Reader.source(test.example.Complex.Subber)
            # class Subber:
            #     """
            #     Sub class
            #     """
            #     pass
            #

    .. classmethod:: update(primary: dict, secondary: dict, skip=None)

        Updates an existing parsed dict with another, concatenating the descriptions

        :param primary: The parsed dict to update
        :type primary: dict
        :param secondary: The parsed dict to update with
        :type secondary: dict
        :param skip: What dict keys to skip for updating
        :type skip: None or str or list(str)

        **Usage**

        This is used mainly to combine short and long descriptions::

            import sphinxter

            class Example:

                attribute = None # This is an attribute
                """
                description: It's one of my favorites
                type: str
                """

            primary = {
                "description": "This is an attribute"
            }

            secondary = {
                "description": "It's one of my favorites",
                "type": "str"
            }

            sphinxter.Reader.update(primary, secondary)
            primary
            # {
            #     "description": "This is an attribute\n\nIt's one of my favorites",
            #     "type": "str"
            # }

        It's also used to inject __init___ into a class, but not overwriting what matters::

            class Example:
                """
                An example class
                """

                def __init__(self,
                    foo:str # The foo arg
                ):

                    return True

            primary = {
                "name": "Example",
                "description": "An example class"
            }

            secondary = {
                "name": "Example.__init__",
                "signature": "(foo: str)",
                "parameters": [
                    {
                        "name": "foo",
                        "description": "The foo arg",
                        "type": "str"
                    }
                ]
            }

            sphinxter.Reader.update(primary, secondary, "name")
            primary
            # {
            #     "name": "Example",
            #     "description": "An example class",
            #     "signature": "(foo: str)",
            #     "parameters": [
            #         {
            #             "name": "foo",
            #             "description": "The foo arg",
            #             "type": "str"
            #         }
            #     ]
            # }
