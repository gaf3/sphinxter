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
        themelves::

            def example(
                a:int,
                b:str
            )->list:
                pass

            sphinxter.Reader.annotations(example)
            # {
            #     "parameters": {
            #         "a": {
            #             "type": "int"
            #         },
            #         "b": {
            #             "type": "str"
            #         }
            #     },
            #     "return": {
            #         "type": "list"
            #     }
            # }

    .. classmethod:: attributes(resource) -> dict

        Read attributes from a module or class, including their comments and docstrings

        :param resource: what to extract attributes from
        :type resource: function or method
        :rtype: dict

        **Usage**

        If you have attributes on a module, say the example module::

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

            sphinxter.Reader.attributes(example)
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
            # })

        This works the same for a class, say the Complex class in the example module::

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

            sphinxter.Reader.attributes(example.Complex)
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
            # })

    .. classmethod:: cls(resource) -> dict

        Reads all the documentation from a class for :any:`Writer.cls`

        :param resource: what to extract documentation from
        :type resource: class
        :rtype: dict

        **Usage**

        Given this class is part of the example module::

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

        Reading all the documentation is as easy as::

            sphinxter.Reader.cls(example.Complex)
            # {
            #     "name": "Complex",
            #     "description": "Complex class\n\ncall me",
            #     "signature": "(a, b, *args, **kwargs)",
            #     "definition": "make sure you do this::\n\n    wowsa\n\nYa sweet\n",
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
            #     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n",
            #     "attributes": [
            #         {
            #             "name": "a",
            #             "description": "The a team"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b team\n\nNot as good as the a team"
            #         },
            #         {
            #             "name": "big",
            #             "a": 1,
            #             "b": 2,
            #             "description": "Bunch a"
            #         }
            #     ],
            #     "methods": [
            #         {
            #             "name": "stat",
            #             "method": "static",
            #             "description": "Some static stat",
            #             "signature": "(a, b, *args, **kwargs) -> list",
            #             "parameters": [
            #                 {
            #                     "name": "a",
            #                     "description": "The a More stuff"
            #                 },
            #                 {
            #                     "name": "b",
            #                     "description": "The b",
            #                     "more": "stuff"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "name": "kwargs",
            #                     "a": 1,
            #                     "b": 2
            #                 }
            #             ],
            #             "return": {
            #                 "description": "things",
            #                 "type": "list"
            #             }
            #         },
            #         {
            #             "name": "classy",
            #             "method": "class",
            #             "description": "Some class meth",
            #             "signature": "(a, b, *args, **kwargs)",
            #             "parameters": [
            #                 {
            #                     "name": "a",
            #                     "description": "The a More stuff"
            #                 },
            #                 {
            #                     "name": "b",
            #                     "description": "The b",
            #                     "more": "stuff"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "name": "kwargs",
            #                     "a": 1,
            #                     "b": 2
            #                 }
            #             ],
            #             "return": {
            #                 "description": "things",
            #                 "type": 'str'
            #             }
            #         },
            #         {
            #             "name": "meth",
            #             "method": "",
            #             "description": "Some basic meth",
            #             "signature": "(a, b, *args, **kwargs)",
            #             "parameters": [
            #                 {
            #                     "name": "a",
            #                     "description": "The a More stuff"
            #                 },
            #                 {
            #                     "name": "b",
            #                     "description": "The b",
            #                     "more": "stuff"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "name": "kwargs",
            #                     "a": 1,
            #                     "b": 2
            #                 }
            #             ],
            #             "return": {
            #                 "description": "things",
            #                 "type": [
            #                     'str',
            #                     'None'
            #                 ]
            #             },
            #             "raises": {
            #                 "Exception": "if oh noes"
            #             },
            #             "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #         }
            #     ],
            #     "classes": [
            #         {
            #             "name": "Subber",
            #             "description": "Sub class",
            #             "methods": [],
            #             "attributes": [],
            #             "classes": []
            #         }
            #     ]
            # }

        Notfice that the __init__ method documentation has been super imposed over the class documentation.

    .. classmethod:: comments(resource) -> dict

        Reads parameters comments from a function or method

        :param resource: what to read the parameter comments from
        :type resource: function or method
        :return: dict of parsed comments, keyed by parameter
        :rtype: dict

        **Usage**

        You can put comments after parameters in a function or method and they
        can be parsed as YAML, just like a docstring)::

            def example(
                a, # The a
                b  # description: The b
                   # type: str
            ):
                pass

            sphinxter.Reader.comments(example)
            # {
            #     "a": {
            #         "description": "The a"
            #     },
            #     "b": {
            #         "description: "The b",
            #         "type": "str"
            #     }
            # }

    .. classmethod:: module(resource) -> dict

        Reads all the documentation from a module for :any:`Writer.module`

        :param resource: what to extract documentation from
        :type resource: module
        :rtype: dict

        **Usage**

        Say the following is the example module::

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

            class Basic:
                """
                Basic class
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

                class Subber:
                    """
                    Sub class
                    """
                    pass

        Reading all the documentation is as easy as::

            sphinxter.Reader.cls(example)
            # {
            #     "name": "example",
            #     "description": "mod me",
            #     "attributes": [
            #         {
            #             "name": "a",
            #             "description": "The a team"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b team\n\nNot as good as the a team"
            #         },
            #         {
            #             "name": "big",
            #             "a": 1,
            #             "b": 2,
            #             "description": "Bunch a"
            #         }
            #     ],
            #     "functions": [
            #         {
            #             "name": "func",
            #             "description": "Some basic func",
            #             "signature": "(a: int, b: 'str', *args, **kwargs)",
            #             "parameters": [
            #                 {
            #                     "name": "a",
            #                     "description": "The a More stuff",
            #                     "type": "int"
            #                 },
            #                 {
            #                     "name": "b",
            #                     "description": "The b",
            #                     "more": "stuff",
            #                     "type": "str"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "name": "kwargs",
            #                     "a": 1,
            #                     "b": 2
            #                 }
            #             ],
            #             "return": {
            #                 "description": "things",
            #                 "type": [
            #                     'str',
            #                     'None'
            #                 ]
            #             },
            #             "raises": {
            #                 "Exception": "if oh noes"
            #             },
            #             "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #         }
            #     ],
            #     "classes": [
            #         {
            #             "name": "Basic",
            #             "description": "Basic class",
            #             "methods": [],
            #             "attributes": [],
            #             "classes": []
            #         },
            #         {
            #             "name": "Complex",
            #             "description": "Complex class\n\ncall me",
            #             "signature": "(a, b, *args, **kwargs)",
            #             "definition": "make sure you do this::\n\n    wowsa\n\nYa sweet\n",
            #             "parameters": [
            #                 {
            #                     "name": "a",
            #                     "description": "The a More stuff"
            #                 },
            #                 {
            #                     "name": "b",
            #                     "description": "The b",
            #                     "more": "stuff"
            #                 },
            #                 {
            #                     "name": "args"
            #                 },
            #                 {
            #                     "name": "kwargs",
            #                     "a": 1,
            #                     "b": 2
            #                 }
            #             ],
            #             "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n",
            #             "attributes": [
            #                 {
            #                     "name": "a",
            #                     "description": "The a team"
            #                 },
            #                 {
            #                     "name": "b",
            #                     "description": "The b team\n\nNot as good as the a team"
            #                 },
            #                 {
            #                     "name": "big",
            #                     "a": 1,
            #                     "b": 2,
            #                     "description": "Bunch a"
            #                 }
            #             ],
            #             "methods": [
            #                 {
            #                     "name": "classy",
            #                     "method": "class",
            #                     "description": "Some class meth",
            #                     "signature": "(a, b, *args, **kwargs)",
            #                     "parameters": [
            #                         {
            #                             "name": "a",
            #                             "description": "The a More stuff"
            #                         },
            #                         {
            #                             "name": "b",
            #                             "description": "The b",
            #                             "more": "stuff"
            #                         },
            #                         {
            #                             "name": "args"
            #                         },
            #                         {
            #                             "name": "kwargs",
            #                             "a": 1,
            #                             "b": 2
            #                         }
            #                     ],
            #                     "return": {
            #                         "description": "things",
            #                         "type": 'str'
            #                     }
            #                 },
            #                 {
            #                     "name": "meth",
            #                     "method": "",
            #                     "description": "Some basic meth",
            #                     "signature": "(a, b, *args, **kwargs)",
            #                     "parameters": [
            #                         {
            #                             "name": "a",
            #                             "description": "The a More stuff"
            #                         },
            #                         {
            #                             "name": "b",
            #                             "description": "The b",
            #                             "more": "stuff"
            #                         },
            #                         {
            #                             "name": "args"
            #                         },
            #                         {
            #                             "name": "kwargs",
            #                             "a": 1,
            #                             "b": 2
            #                         }
            #                     ],
            #                     "return": {
            #                         "description": "things",
            #                         "type": [
            #                             'str',
            #                             'None'
            #                         ]
            #                     },
            #                     "raises": {
            #                         "Exception": "if oh noes"
            #                     },
            #                     "usage": "Do some cool stuff::\n\n    like this\n\nIt's great\n"
            #                 },
            #                 {
            #                     "name": "stat",
            #                     "method": "static",
            #                     "description": "Some static stat",
            #                     "signature": "(a, b, *args, **kwargs) -> list",
            #                     "parameters": [
            #                         {
            #                             "name": "a",
            #                             "description": "The a More stuff"
            #                         },
            #                         {
            #                             "name": "b",
            #                             "description": "The b",
            #                             "more": "stuff"
            #                         },
            #                         {
            #                             "name": "args"
            #                         },
            #                         {
            #                             "name": "kwargs",
            #                             "a": 1,
            #                             "b": 2
            #                         }
            #                     ],
            #                     "return": {
            #                         "description": "things",
            #                         "type": "list"
            #                     }
            #                 }
            #             ],
            #             "classes": [
            #                 {
            #                     "name": "Subber",
            #                     "description": "Sub class",
            #                     "methods": [],
            #                     "attributes": [],
            #                     "classes": []
            #                 }
            #             ]
            #         }
            #     ],
            #     "attributes": [
            #         {
            #             "name": "a",
            #             "description": "The a team"
            #         },
            #         {
            #             "name": "b",
            #             "description": "The b team\n\nNot as good as the a team"
            #         },
            #         {
            #             "name": "big",
            #             "a": 1,
            #             "b": 2,
            #             "description": "Bunch a"
            #         }
            #     ],
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

            def function plain():
                """
                A plain function
                """

            sphinxter.Reader.parse(plain.__doc__)
            # {
            #     "description": "A plain function"
            # }

        If you have straight YAML it's return that as is::

            def function exact():
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

        Reading all the documentation for a function is as easy as::

            # Assume this is part of a module named example

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

                pass

            sphinxter.Reader.routine(inspect.getattr_static(example, 'func'))
            # {
            #     "name": "func",
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

        Methods aren't much different, and include a method key, that's either '', 'class', or 'static'::

            # Assume we're still in the example module

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

            sphinxter.Reader.routine(inspect.getattr_static(example.Complex, 'stat'))
            # {
            #     "name": "stat",
            #     "method": "static",
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

            sphinxter.Reader.routine(inspect.getattr_static(example.Complex, 'classy'))
            # {
            #     "name": "classy",
            #     "method": "class",
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

            sphinxter.Reader.routine(inspect.getattr_static(example.Complex, 'meth'))
            # {
            #     "name": "meth",
            #     "method": "",
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

        If you have a subclass like::

            class Complex:

                class Subber:

                    pass

        The source for Subber would be indented from inspect.getsource()
        which can't be parsed properly because of the initial indent::

            inpsect.getsource(Complex.Subber)
            #     class Subber:
            #
            #          pass

        This prevents that problem::

            sphinxter.Reader.source(Complex.Subber)
            # class Subber:
            #
            #  pass

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
