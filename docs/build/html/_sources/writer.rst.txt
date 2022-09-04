.. created by sphinxter
.. default-domain:: py

sphinxter.Writer
================

.. currentmodule:: sphinxter

.. class:: Writer(document: 'sphinxter.Document', file)

    Class for writing out documents (rst)

    :param document: document object to write out
    :type document: sphinxter.Document
    :param file: file handle like object to write to

    .. attribute:: document

        document object to write out

    .. attribute:: file

        file handle to write out to

    .. method:: attribute(parsed: dict, indent: int)

        Writes attribute content, preceeded by a blank line

        :param parsed: parsed documentation for an attribute
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's just a name::

            parsed = {
                "name": "small"
            }

            writer.attribute(parsed, 1
            #
            #      .. attribute:: small

        If there's a description and type::

            parsed = {
                "name": "big",
                "description": "stuff",
                "type": "int"
            }

            writer.attribute(parsed, 1)
            #
            #     .. attribute:: big
            #         :type: int
            #
            #         stuff

    .. method:: attributes(parsed: dict, indent: int)

        Writes attributes content if present

        :param parsed: parsed documentation possibly containing attributes
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's attributes::

            parsed = {
                "attributes": [
                    {
                        "name": "small"
                    },
                    {
                        "name": "big",
                        "description": "stuff",
                        "type": "int"
                    }
                ]
            }

            writer.attributes(parsed, indent=1)
            #
            #     .. attribute:: small
            #
            #     .. attribute:: big
            #         :type: int
            #
            #         stuff

        If there's nothing, do nothing:

            parsed = {}

            writer.attributes(parsed, 1)

    .. method:: cls(parsed: dict, indent: int = 0)

        Writes class content as from :any:`Reader.cls`

        :param parsed: entire parsed documentation for a class
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

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

            parsed = sphinxter.Reader.cls(example.Complex)
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
            #         },
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

            writer.module(parsed, indent=1)
            #
            #     .. class:: Complex(a, b, *args, **kwargs)
            #
            #         Complex class
            #
            #         call me
            #
            #         **Definition**
            #
            #         make sure you do this::
            #
            #             wowsa
            #
            #         Ya sweet
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #
            #         **Usage**
            #
            #         Do some cool stuff::
            #
            #             like this
            #
            #         It's great
            #
            #         .. attribute:: a
            #
            #             The a team
            #
            #         .. attribute:: b
            #
            #             The b team
            #
            #             Not as good as the a team
            #
            #         .. attribute:: big
            #
            #             Bunch a
            #
            #         .. classmethod:: classy(a, b, *args, **kwargs)
            #
            #             Some class meth
            #
            #             :param a: The a More stuff
            #             :param b: The b
            #             :param args:
            #             :param kwargs:
            #             :return: things
            #             :rtype: str
            #
            #         .. method:: meth(a, b, *args, **kwargs)
            #
            #             Some basic meth
            #
            #             :param a: The a More stuff
            #             :param b: The b
            #             :param args:
            #             :param kwargs:
            #             :return: things
            #             :rtype: str or None
            #             :raises Exception: if oh noes
            #
            #             **Usage**
            #
            #             Do some cool stuff::
            #
            #                 like this
            #
            #             It's great
            #
            #         .. staticmethod:: stat(a, b, *args, **kwargs) -> list
            #
            #             Some static stat
            #
            #             :param a: The a More stuff
            #             :param b: The b
            #             :param args:
            #             :param kwargs:
            #             :return: things
            #             :rtype: list

    .. method:: definition(parsed: dict, indent: int)

        Writes a definition block if present, for describing how to define a class, ie models

        :param parsed: parsed documentation possibly keyed by definition
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's definition, write with a header and proper blank lines::

            class Example():
                """
                definition: |
                    Try this::

                        class Example:
                            pass
                """

            parsed = {
                "definition": "Try this::\n\n    class Example:\n        pass"
            }

            writer.definition(parsed, 1)
            #
            #     **Definition**
            #
            #     Try this::
            #
            #         class Example:
            #             pass

        If there's nothing, do nothing::

            parsed = {}

            writer.definition(parsed, 1)

    .. method:: description(parsed: dict, indent: int)

        Writes description if present, preceeding with a blank line

        :param parsed: parsed documentation
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**


        If there's a description in the documentation, it writes it out with a preceeding blank line::

            parsed = {
                "description": "It is what it is"
            }

            writer.description(parsed, indent=1)
            #
            #     It is what it is
            #

        If there's no description, it does nothing::

            parsed = {}

            writer.description(parsed, indent=1)

    .. method:: dump()

        Writes out an entire document

        **Usage**

        Give the entire example module::

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

            parsed = sphinxter.Reader.module(example)
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

            document = Document("docs/source/index.rst", "example", ['self', '*'], '    ')

            document.add("example", "module", parsed, 0)

            for function in parsed["functions"]:
                document.add("example", "function", function, 0)

            for cls in parsed["classes"]:
                document.add("example", "class", cls, 0)

            with open(document.path, "w", encoding="utf-8") as file:
                Writer(document, file).dump()

            # .. created by sphinxter
            # .. default-domain:: py
            #
            # example
            # ============
            #
            # .. toctree::
            #     :maxdepth: 1
            #     :glob:
            #     :hidden:
            #
            #     self
            #     *
            #
            # .. module:: example
            #
            # mod me
            #
            # **Usage**
            #
            # Do some cool stuff::
            #
            #     like this
            #
            # It's great
            #
            # .. attribute:: a
            #
            #     The a team
            #
            # .. attribute:: b
            #
            #     The b team
            #
            #     Not as good as the a team
            #
            # .. attribute:: big
            #
            #     Bunch a
            #
            # .. function:: func(a: int, b: 'str', *args, **kwargs)
            #
            #     Some basic func
            #
            #     :param a: The a More stuff
            #     :type a: int
            #     :param b: The b
            #     :type b: str
            #     :param args:
            #     :param kwargs:
            #     :return: things
            #     :rtype: str or None
            #     :raises Exception: if oh noes
            #
            #     **Usage**
            #
            #     Do some cool stuff::
            #
            #         like this
            #
            #     It's great
            #
            # .. class:: Basic
            #
            #     Basic class
            #
            # .. class:: Complex(a, b, *args, **kwargs)
            #
            #     Complex class
            #
            #     call me
            #
            #     **Definition**
            #
            #     make sure you do this::
            #
            #         wowsa
            #
            #     Ya sweet
            #
            #     :param a: The a More stuff
            #     :param b: The b
            #     :param args:
            #     :param kwargs:
            #
            #     **Usage**
            #
            #     Do some cool stuff::
            #
            #         like this
            #
            #     It's great
            #
            #     .. attribute:: a
            #
            #         The a team
            #
            #     .. attribute:: b
            #
            #         The b team
            #
            #         Not as good as the a team
            #
            #     .. attribute:: big
            #
            #         Bunch a
            #
            #     .. classmethod:: classy(a, b, *args, **kwargs)
            #
            #         Some class meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: str
            #
            #     .. method:: meth(a, b, *args, **kwargs)
            #
            #         Some basic meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: str or None
            #         :raises Exception: if oh noes
            #
            #         **Usage**
            #
            #         Do some cool stuff::
            #
            #             like this
            #
            #         It's great
            #
            #     .. staticmethod:: stat(a, b, *args, **kwargs) -> list
            #
            #         Some static stat
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: list

    .. method:: function(parsed: dict, indent: int = 0)

        Writes function content as from :any:`Reader.routine`

        :param parsed: entire parsed documentation for a function
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        Given the following function as part of the example module::

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

            parsed = sphinxter.Reader.routine(inspect.getattr_static(example, 'func'))
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

            writer.function(parsed, indent=1)
            #
            #     .. function:: func(a: int, b: 'str', *args, **kwargs)
            #
            #         Some basic func
            #
            #         :param a: The a More stuff
            #         :type a: int
            #         :param b: The b
            #         :type b: str
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: str or None
            #         :raises Exception: if oh noes
            #
            #         **Usage**
            #
            #         Do some cool stuff::
            #
            #             like this
            #
            #         It's great

    .. method:: line(line: str = '', indent: int = 0, before: bool = False, after: bool = False)

        Writes a line of text to the filehandle

        :param line: Text to write out
        :type line: str
        :param indent: How many times to indent
        :type indent: int
        :param before: Whether to put a blankline before
        :type before: bool
        :param after: Whether to put a blankline after
        :type after: bool

        **Usage**

        This can just write a line of text::

            writer.line("Hello, world!")
            # Hello world!

        It can indent::

            writer.line("Hello, world!", indent=1)
            #     Hello world!

        And it can add lines (with no indent) before and after::

            writer.line("Hello, world!", indent=1, before=True, after=True)
            #
            #     Hello world!
            #

    .. method:: lines(lines: str, indent: int, before: bool = False, after: bool = False)

        Writes lines of text to the filehandle

        :param lines: Multil\ine text to write out
        :type lines: str
        :param indent: How many times to indent
        :type indent: int
        :param before: Whether to put a blankline before
        :type before: bool
        :param after: Whether to put a blankline after
        :type after: bool

        **Usage**

        This can just write lines of text::

            writer.line("Hello\nworld!")
            # Hello
            # world!

        It can indent::

            writer.line("Hello\nworld!", indent=1)
            #     Hello
            #     world!

        And it can add lines (with no indent) before and after::

            writer.line("Hello\nworld!", indent=1, before=True, after=True)
            #
            #     Hello
            #     world!
            #

    .. method:: method(parsed: dict, indent: int)

        Writes method content as from :any:`Reader.routine`

        :param parsed: entire parsed documentation for a method
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        For a regular method, assuming the Complex class as part of the example module::

            class Complex:

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

            parsed = sphinxter.Reader.routine(inspect.getattr_static(example.Complex, 'stat'))
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

            writer.method(parsed, indent=1)
            #
            #     .. staticmethod:: stat(a, b, *args, **kwargs) -> list
            #
            #         Some static stat
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: list

            parsed = sphinxter.Reader.routine(inspect.getattr_static(example.Complex, 'classy'))
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

            writer.method(parsed, indent=1)
            #
            #     .. classmethod:: classy(a, b, *args, **kwargs)
            #
            #         Some class meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: str

            parsed = sphinxter.Reader.routine(inspect.getattr_static(example.Complex, 'meth'))
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

            writer.method(parsed, indent=1)
            #
            #     .. method:: meth(a, b, *args, **kwargs)
            #
            #         Some basic meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args:
            #         :param kwargs:
            #         :return: things
            #         :rtype: str or None
            #         :raises Exception: if oh noes
            #
            #         **Usage**
            #
            #         Do some cool stuff::
            #
            #             like this
            #
            #         It's great

    .. method:: module(parsed: dict, indent: int = 0)

        Writes module content as from :any:`Reader.module` but with a slight difference.

        Reading a module reads all the classes and functions for that module. Writing a module
        only writes documentation for that module because classes and functions don't have to
        be part of the same document as their parent module.

        :param parsed: entire parsed documentation for a class
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

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

            parsed = sphinxter.Reader.module(example)
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

            writer.module(parsed, indent=1)
            #
            #     .. module:: example
            #
            #     **Usage**
            #
            #     Do some cool stuff::
            #
            #         like this
            #
            #     It's great
            #
            #     .. attribute:: a
            #
            #         The a team
            #
            #     .. attribute:: b
            #
            #         The b team
            #
            #         Not as good as the a team
            #
            #     .. attribute:: big
            #
            #         Bunch a

        Notice how no functions or classes are written.

    .. method:: parameter(parsed: dict, indent: int)

        Writes parameter documentation

        :param parsed: parsed documentation for a parameter
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**


        If there's only a name::

            parsed = {
                "name": "arg"
            }

            writer.parameter(parsed, indent=1)
            #     :param arg:

        If there's also a description::

            parsed = {
                "name": "arg",
                "description": "an argument"
            }

            writer.parameter(parsed, indent=1)
            #     :param arg: an argument

        If there's also a type::

            parsed = {
                "name": "arg",
                "description": "an argument",
                "type": "bool"
            }

            writer.parameter(parsed, indent=1)
            #     :param arg: an argument
            #     :type arg: bool

    .. method:: parameters(parsed: dict, indent: int)

        Writes parameters if present

        :param parsed: parsed documentation possibly keyed by parameters
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If parameters are present, write them::

            parsed = {
                "parameters": [
                    {
                        "name": "small"
                    },
                    {
                        "name": "big",
                        "description": "stuff",
                        "type": "int"
                    }
                ]
            }

            writer.parameters(parsed, 1)
            #     :param small:
            #     :param big: stuff
            #     :type big: int

        If not, do nothing::

            parsed = {}

            writer.parameters(parsed, 1)

    .. method:: raises(parsed: dict, indent: int)

        Writes raises information if present

        :param parsed: parsed documentation possibly keyed by raises
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's raises, write them (alphabetically)::

            parsed = {
                "raises": {
                    "Exception": "whoops",
                    "Error": "oh no"
                }
            }

            writer.raises(parsed, 1)
            #     :raises Error: oh no
            #     :raises Exception: whoops

        If there's nothing, do nothing::

            parsed = {}

            writer.raises(parsed, 1)

    .. method:: returns(parsed: dict, indent: int)

        Writes return information if present

        :param parsed: parsed documentation possibly keyed by return
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's a description::

            parsed = {
                "return": {
                    "description": "stuff"
                }
            }

            writer.returns(parsed, 1)
            #     :return: stuff

        If there's also a type::

            parsed = {
                "return": {
                    "description": "stuff",
                    "type": "int"
                }
            }

            writer.returns(parsed, 1)
            #     :return: stuff
            #     :rtype: int

        If there's only a type::

            parsed = {
                "return": {
                    "type": "int"
                }
            }

            writer.returns(parsed, 1)
            #     :rtype: int

        If there's nothing, do nothing::

            parsed = {}

            writer.returns(parsed, 1)

    .. method:: routine(parsed: dict, indent: int)

        Writes documentation for that which can be excuted

        :param parsed: parsed documentation possibly keyed by parameters, return, and/or raises
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's parameters, return, and/or raises, write them, preceeding by a blank line::

            parsed = {
                "parameters": [
                    {
                        "name": "small"
                    },
                    {
                        "name": "big",
                        "description": "stuff",
                        "type": "int"
                    }
                ],
                "return": {
                    "description": "stuff",
                    "type": "int"
                },
                "raises": {
                    "Exception": "whoops",
                    "Error": "oh no"
                }
            }

            writer.routine(parsed, 1)
            #
            #     :param small:
            #     :param big: stuff
            #     :type big: int
            #     :return: stuff
            #     :rtype: int
            #     :raises Error: oh no
            #     :raises Exception: whoops

        If there's nothing, do nothing::

            parsed = {}

            writer.routine(parsed, 1)

    .. method:: toctree(paths: 'list[str]', indent: int = 0)

        Writes a toctree to the index document, hiding it so it'll appear to the left.

        :param paths: paths for the toc
        :type paths: list[str]
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        writer.toctree(['self', '*'], indent=1)
        #     .. toctree::
        #         :maxdepth: 1
        #         :glob:
        #         :hidden:
        #
        #         *
        #         self

    .. staticmethod:: types(types: 'str or list')

        Takes a str of type or list of str of type and returns a str

        :param types: Type(s) to write out
        :type types: str or list

        **Usage**

        If just a single type, it returns that::

            spinxter.Writer.types("str")
            # "str"

        If a list of types, return types, concatenated with ' or '::

            spinxter.Writer.types(["str", "list"])
            # "str or list"

    .. method:: usage(parsed: dict, indent: int)

        Writes a usage block if present

        :param parsed: parsed documentation possibly keyed by usage
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's usages, write with a header and proper blank lines::

            def example():
                """
                usage: |
                    Here's a neat trick::

                        print("Hello, world!")

                    Cool, huh?
                """

            parsed = {
                "usage": "Here's a neat trick::\n\n    print("Hello, world!")\n\nCool, huh?"
            }

            writer.usage(parsed, 1)
            #
            #     **Usage**
            #
            #     Here's a neat trick::
            #
            #         print("Hello, world!")
            #
            #     Cool, huh?

        If there's nothing, do nothing::

            parsed = {}

            writer.usage(parsed, 1)
