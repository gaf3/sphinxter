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

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "name": "small"
            }

            writer.attribute(parsed, 1)
            handle.getvalue()
            #
            #     .. attribute:: small
            #

        If there's a description and type::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "name": "big",
                "description": "stuff",
                "type": "int"
            }

            writer.attribute(parsed, 1)
            handle.getvalue()
            #
            #     .. attribute:: big
            #         :type: int
            #
            #         stuff
            #

    .. method:: attributes(parsed: dict, indent: int)

        Writes attributes content if present

        :param parsed: parsed documentation possibly containing attributes
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's attributes::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

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
            handle.getvalue()
            #
            #     .. attribute:: small
            #
            #     .. attribute:: big
            #         :type: int
            #
            #         stuff
            #

        If there's nothing, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.attributes(parsed, 1)
            handle.getvalue()
            #

    .. method:: cls(parsed: dict, indent: int = 0)

        Writes class content as from :any:`Reader.cls`

        :param parsed: entire parsed documentation for a class
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

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

        The documentation can be generated as such::

            import io
            import sphinxter
            import test.example

            parsed = sphinxter.Reader.cls(test.example.Complex)
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

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.cls(parsed, indent=1)
            handle.getvalue()
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
            #         :param args: args
            #         :param kwargs: kwargs
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
            #             :param args: args
            #             :param kwargs: kwargs
            #             :return: things
            #             :rtype: str
            #
            #         .. method:: meth(a, b, *args, **kwargs)
            #
            #             Some basic meth
            #
            #             :param a: The a More stuff
            #             :param b: The b
            #             :param args: args
            #             :param kwargs: kwargs
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
            #             :param args: args
            #             :param kwargs: kwargs
            #             :return: things
            #             :rtype: list
            #
            #         .. class:: Subber
            #
            #             Sub class
            #
            #         .. exception:: Excepter
            #
            #             Sub exception
            #

        Say the test.exmaple module has this Exception::

            class Basic(Exception):
                """
                Basic Exception
                """

        It's documentation is generated the same as any class::

            parsed = sphinxter.Reader.cls(test.example.Basic)
            # {
            #     "attributes": [],
            #     "classes": [],
            #     "description": "Basic Exception",
            #     "exceptions": [],
            #     "kind": "exception",
            #     "methods": [],
            #     "name": "Basic"
            # }

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.cls(parsed, indent=1)
            handle.getvalue()
            #
            #     .. exception:: Basic
            #
            #         Basic Exception
            #

    .. method:: definition(parsed: dict, indent: int)

        Writes a definition block if present, for describing how to define a class, ie models

        :param parsed: parsed documentation possibly keyed by definition
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's definition, write with a header and proper blank lines::

            import io
            import yaml
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            class Example():
                """
                definition: |
                    Try this::

                        class Example:
                            pass
                """

            parsed = yaml.safe_load(Example.__doc__)
            # {
            #     "definition": "Try this::\n\n    class Example:\n        pass\n"
            # }

            writer.definition(parsed, 1)
            handle.getvalue()
            #
            #     **Definition**
            #
            #     Try this::
            #
            #         class Example:
            #             pass
            #

        If there's nothing, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.definition(parsed, 1)
            handle.getvalue()
            #

    .. method:: description(parsed: dict, indent: int)

        Writes description if present, preceeding with a blank line

        :param parsed: parsed documentation
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**


        If there's a description in the documentation, it writes it out with a preceeding blank line::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "description": "It is what it is"
            }

            writer.description(parsed, indent=1)
            handle.getvalue()
            #
            #     It is what it is
            #

        If there's no description, it does nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.description(parsed, indent=1)
            handle.getvalue()
            #

    .. method:: dump()

        Writes out an entire document

        **Usage**

        Give the entire test.example module::

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

        Generatig the whole shebang::

            import io
            import sphinxter
            import test.example

            parsed = sphinxter.Reader.module(test.example)
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

            document = sphinxter.Document(None, "test.example", ['self', '*'], '    ')

            for function in parsed["functions"]:
                document.add("test.example", "function", function, 0)

            for cls in parsed["classes"]:
                document.add("test.example", "class", cls, 0)

            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.dump()
            handle.getvalue()
            # .. created by sphinxter
            # .. default-domain:: py
            #
            # test.example
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
            # .. currentmodule:: test.example
            #
            # .. function:: func(a: int, b: 'str', *args, **kwargs)
            #
            #     Some basic func
            #
            #     :param a: The a More stuff
            #     :type a: int
            #     :param b: The b
            #     :type b: str
            #     :param args: args
            #     :param kwargs: kwargs
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
            #     :param args: args
            #     :param kwargs: kwargs
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
            #         :param args: args
            #         :param kwargs: kwargs
            #         :return: things
            #         :rtype: str
            #
            #     .. method:: meth(a, b, *args, **kwargs)
            #
            #         Some basic meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args: args
            #         :param kwargs: kwargs
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
            #         :param args: args
            #         :param kwargs: kwargs
            #         :return: things
            #         :rtype: list
            #
            #     .. class:: Subber
            #
            #         Sub class
            #
            #     .. exception:: Excepter
            #
            #         Sub exception
            #

    .. method:: function(parsed: dict, indent: int = 0)

        Writes function content as from :any:`Reader.routine`

        :param parsed: entire parsed documentation for a function
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        Given the following function as part of the test.example module::

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

        Generating the docs is easy as::

            import io
            import inspect
            import sphinxter
            import test.example

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example, 'func'))
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

            writer.function(parsed, indent=1)
            handle.getvalue()
            #
            #     .. function:: func(a: int, b: 'str', *args, **kwargs)
            #
            #         Some basic func
            #
            #         :param a: The a More stuff
            #         :type a: int
            #         :param b: The b
            #         :type b: str
            #         :param args: args
            #         :param kwargs: kwargs
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

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.line("Hello, world!")
            handle.getvalue()
            # Hello, world!
            #

        It can indent::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.line("Hello, world!", indent=1)
            handle.getvalue()
            #     Hello, world!
            #

        And it can add lines (with no indent) before and after::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.line("Hello, world!", indent=1, before=True, after=True)
            handle.getvalue()
            #
            #     Hello, world!
            #
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

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.lines("Hello\nworld!", indent=0)
            handle.getvalue()
            # Hello
            # world!
            #

        It can indent::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.lines("Hello\nworld!", indent=1)
            handle.getvalue()
            #     Hello
            #     world!
            #

        And it can add lines (with no indent) before and after::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.lines("Hello\nworld!", indent=1, before=True, after=True)
            handle.getvalue()
            #
            #     Hello
            #     world!
            #
            #

    .. method:: method(parsed: dict, indent: int)

        Writes method content as from :any:`Reader.routine`

        :param parsed: entire parsed documentation for a method
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        For a regular method, assuming the Complex class as part of the test.example module::

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

        Generating docs for a static method::

            import io
            import inspect
            import sphinxter
            import test.example

            parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'stat'), method=True)
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

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.method(parsed, indent=1)
            handle.getvalue()
            #
            #     .. staticmethod:: stat(a, b, *args, **kwargs) -> list
            #
            #         Some static stat
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args: args
            #         :param kwargs: kwargs
            #         :return: things
            #         :rtype: list
            #

        For a class method::

            parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'classy'), method=True)
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

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.method(parsed, indent=1)
            handle.getvalue()
            #
            #     .. classmethod:: classy(a, b, *args, **kwargs)
            #
            #         Some class meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args: args
            #         :param kwargs: kwargs
            #         :return: things
            #         :rtype: str
            #

        And for a regular ol' method::

            parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'meth'), method=True)
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

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.method(parsed, indent=1)
            handle.getvalue()
            #
            #     .. method:: meth(a, b, *args, **kwargs)
            #
            #         Some basic meth
            #
            #         :param a: The a More stuff
            #         :param b: The b
            #         :param args: args
            #         :param kwargs: kwargs
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


        The documentation can be generated as such::

            import io
            import sphinxter
            import test.example

            parsed = sphinxter.Reader.module(test.example)
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

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.module(parsed, indent=1)
            handle.getvalue()
            #
            #     .. module:: test.example
            #
            #     mod me
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

        Notice how no functions or classes are written.

    .. method:: parameter(parsed: dict, indent: int)

        Writes parameter documentation

        :param parsed: parsed documentation for a parameter
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**


        If there's only a name::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "name": "arg"
            }

            writer.parameter(parsed, indent=1)
            handle.getvalue()
            #     :param arg: arg
            #

        If there's also a description::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "name": "arg",
                "description": "an argument"
            }

            writer.parameter(parsed, indent=1)
            handle.getvalue()
            #     :param arg: an argument
            #

        If there's also a type::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "name": "arg",
                "description": "an argument",
                "type": "bool"
            }

            writer.parameter(parsed, indent=1)
            handle.getvalue()
            #     :param arg: an argument
            #     :type arg: bool
            #

    .. method:: parameters(parsed: dict, indent: int)

        Writes parameters if present

        :param parsed: parsed documentation possibly keyed by parameters
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If parameters are present, write them::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

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
            handle.getvalue()
            #     :param small: small
            #     :param big: stuff
            #     :type big: int
            #

        If not, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.parameters(parsed, 1)
            handle.getvalue()
            #

    .. method:: raises(parsed: dict, indent: int)

        Writes raises information if present

        :param parsed: parsed documentation possibly keyed by raises
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's raises, write them (alphabetically)::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "raises": {
                    "Exception": "whoops",
                    "Error": "oh no"
                }
            }

            writer.raises(parsed, 1)
            handle.getvalue()
            #     :raises Error: oh no
            #     :raises Exception: whoops
            #

        If there's nothing, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.raises(parsed, 1)
            handle.getvalue()
            #

    .. method:: returns(parsed: dict, indent: int)

        Writes return information if present

        :param parsed: parsed documentation possibly keyed by return
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's a description::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "return": {
                    "description": "stuff"
                }
            }

            writer.returns(parsed, 1)
            handle.getvalue()
            #     :return: stuff
            #

        If there's also a type::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "return": {
                    "description": "stuff",
                    "type": "int"
                }
            }

            writer.returns(parsed, 1)
            handle.getvalue()
            #     :return: stuff
            #     :rtype: int
            #

        If there's only a type::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {
                "return": {
                    "type": "int"
                }
            }

            writer.returns(parsed, 1)
            handle.getvalue()
            #     :rtype: int
            #

        If there's nothing, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.returns(parsed, 1)
            handle.getvalue()
            #

    .. method:: routine(parsed: dict, indent: int)

        Writes documentation for that which can be excuted

        :param parsed: parsed documentation possibly keyed by parameters, return, and/or raises
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's parameters, return, and/or raises, write them, preceeding by a blank line::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

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
            handle.getvalue()
            #
            #     :param small: small
            #     :param big: stuff
            #     :type big: int
            #     :return: stuff
            #     :rtype: int
            #     :raises Error: oh no
            #     :raises Exception: whoops
            #

        If there's nothing, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.routine(parsed, 1)
            handle.getvalue()
            #

    .. method:: toctree(paths: 'list[str]', indent: int = 0)

        Writes a toctree to the index document, hiding it so it'll appear to the left.

        :param paths: paths for the toc
        :type paths: list[str]
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        Generating a toctree::

            import io
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            writer.toctree(['self', '*'], indent=1)
            handle.getvalue()
            #
            #     .. toctree::
            #         :maxdepth: 1
            #         :glob:
            #         :hidden:
            #
            #         self
            #         *
            #

    .. staticmethod:: types(types: 'str or list')

        Takes a str of type or list of str of type and returns a str

        :param types: Type(s) to write out
        :type types: str or list

        **Usage**

        If just a single type, it returns that::

            import sphinxter

            sphinxter.Writer.types("str")
            # "str"

        If a list of types, return types, concatenated with ' or '::

            sphinxter.Writer.types(["str", "list"])
            # "str or list"

    .. method:: usage(parsed: dict, indent: int)

        Writes a usage block if present

        :param parsed: parsed documentation possibly keyed by usage
        :type parsed: dict
        :param indent: amount to indent by
        :type indent: int

        **Usage**

        If there's usages, write with a header and proper blank lines::

            import io
            import yaml
            import sphinxter

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            def example():
                """
                usage: |
                    Here's a neat trick::

                        print("Hello, world!")

                    Cool, huh?
                """

            parsed = yaml.safe_load(example.__doc__)
            # {
            #     "usage": "Here's a neat trick::\n\n    print(\"Hello, world!\")\n\nCool, huh?\n"
            # }

            writer.usage(parsed, 1)
            handle.getvalue()
            #
            #     **Usage**
            #
            #     Here's a neat trick::
            #
            #         print("Hello, world!")
            #
            #     Cool, huh?
            #

        If there's nothing, do nothing::

            document = sphinxter.Document(None, "test.example", None, '    ')
            handle = io.StringIO()

            writer = sphinxter.Writer(document, handle)

            parsed = {}

            writer.usage(parsed, 1)
            handle.getvalue()
            #
