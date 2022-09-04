"""
Module for reading documentation from resources
"""

# pylint: disable=too-many-branches, too-many-locals, too-few-public-methods

import io
import ast
import inspect
import token
import tokenize
import yaml

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
        """

        indent = None
        lines = []

        for line in inspect.getsourcelines(resource)[0]:

            if indent is None:
                indent = 0
                for letter in line:
                    if letter in [' ', "\t"]:
                        indent += 1
                    else:
                        break

            lines.append(line[indent:])

        return "".join(lines)

    @staticmethod
    def parse(
            docstring:str # the docstring (or string after an attribute)
        )->dict:
        """
        description: Parses a docstring into YAML, defaulting to description
        return:
            description: The parsed doctring
        usage: |
            If you just have a plain docstring, it'll return a dict
            with that docstring as the description::

                def function plain():
                    \"""
                    A plain function
                    \"""

                sphinxter.Reader.parse(plain.__doc__)
                # {
                #     "description": "A plain function"
                # }

            If you have straight YAML it's return that as is::

                def function exact():
                    \"""
                    description: An exact function
                    \"""

                sphinxter.Reader.parse(exact.__doc__)
                # {
                #     "description": "An exact function"
                # }

            If the string is blank, it'll return an empty dict::

                sphinxter.Reader.parse("")
                # {}
        """

        if docstring:
            parsed = yaml.safe_load(docstring)
            if isinstance(parsed, str):
                parsed = {"description": parsed}
        else:
            parsed = {}

        return parsed

    @classmethod
    def update(cls,
        primary:dict,   # The parsed dict to update
        secondary:dict, # The parsed dict to update with
        skip=None       # What dict keys to skip for updating
    ):
        """
        description: Updates an existing parsed dict with another, concatenating the descriptions
        parameters:
            skip:
                type:
                - None
                - str
                - list(str)
        usage: |
            This is used mainly to combine short and long descriptions::

                class Example:

                    attribute = None # This is an attribute
                    \"""
                    description: It's one of my favorites
                    type: str
                    \"""

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
                #     "description": "This is an attribute\\n\\nIt's one of my favorites",
                #     "type": "str"
                # }

            It's also used to inject __init___ into a class, but not overwriting what matters::

                class Example:
                    \"""
                    An example class
                    \"""

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
        """

        if skip is None:
            skip = []

        if not isinstance(skip, list):
            skip = [skip]

        for name, value in secondary.items():

            if name in skip:
                continue

            if name == "description" and "description" in primary:
                primary[name] += "\n\n" + value
            else:
                primary[name] = value

    @classmethod
    def comments(cls,
        resource # what to read the parameter comments from
    )->dict:
        """
        description: Reads parameters comments from a function or method
        return: dict of parsed comments, keyed by parameter
        parameters:
            resource:
                type:
                - function
                - method
        usage: |
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
        """

        parens = 0
        param = None
        params = False
        name = False
        comments = {}
        parseds = {}

        source = io.StringIO(cls.source(resource))

        for parsed in tokenize.generate_tokens(source.readline):
            if parsed.type == token.OP:
                if parsed.string == '(':
                    if parens == 0:
                        params = True
                        name = True
                    parens += 1
                elif parsed.string == ')':
                    parens -= 1
                    if parens == 0:
                        break
            elif parsed.type == token.NL:
                name = True
            elif parsed.type == token.NAME and name:
                if params:
                    param = parsed.string
                    parseds[param] = {}
                    name = False
            elif parsed.type == token.COMMENT:
                if param is not None:
                    comment = parsed.string[2:].rstrip()
                    if not comment:
                        continue
                    if param not in comments:
                        comments[param] = comment
                    else:
                        comments[param] = f"{comments[param]}\n{comment}"

        for param, comment in comments.items():
            parseds[param].update(cls.parse(comment))

        return parseds

    @staticmethod
    def annotations(
        resource # what to extract annotations from
    )->dict:
        """
        description: Read annotations in a format better for updating
        parameters:
            resource:
                type:
                - function
                - method
        return: dict of annotations, with parameters and return keys
        usage: |
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
        """

        parseds = {
            "parameters": {},
            "return": {}
        }

        for name, annotation in inspect.get_annotations(resource).items():

            if not isinstance(annotation, str):
                annotation = annotation.__name__

            if name == "return":
                parseds["return"] = {"type": annotation}
            else:
                parseds["parameters"][name] = {"type": annotation}

        return parseds

    @classmethod
    def routine(cls,
        resource,            # what to read from
        method:bool=False    # whether this is a method
    )->dict:
        """
        description: |
            Reads all the documentation from a function or method for :any:`Writer.function` or :any:`Writer.method`

            Of special note is parameters. What's returned at the key of "parameters" is a list of dictionaries. But
            when specifiying parameter in the YAML, use a dict keyed by parameter name. The signature information
            is updated from the parameter comments and then from the dict in the YAML. If descriptions are specified
            in both areas, they'll be joined witha space, the signature comment going first.
        parameters:
            resource:
                type:
                - function
                - method
        return: dict of routine documentation
        usage: |
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
                    \"""
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
                    \"""

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
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
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
                        \"""
                        description: call me
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    @classmethod
                    def classy(
                        cls,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some class meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type: str
                        \"""

                    def meth(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
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
                        \"""

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
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }
        """

        if isinstance(resource, staticmethod):
            kind = "static"
            signature = inspect.signature(resource)
            annotations = cls.annotations(resource)
        elif isinstance(resource, classmethod):
            kind = "class"
            signature = inspect.signature(resource.__func__)
            annotations = cls.annotations(resource.__func__)
        else:
            kind = ""
            signature = inspect.signature(resource)
            annotations = cls.annotations(resource)

        if method and not isinstance(resource, (staticmethod)):
            signature = signature.replace(parameters=list(signature.parameters.values())[1:])

        parsed = {
            "name": resource.__name__,
            "signature": str(signature)
        }

        if method:
            parsed["method"] = kind

        lookup = {}
        comments = cls.comments(resource)

        for name in signature.parameters:

            parsed.setdefault("parameters", [])

            parameter = {
                "name": name
            }

            parameter.update(comments.get(name, {}))
            parameter.update(annotations["parameters"].get(name, {}))

            parsed["parameters"].append(parameter)
            lookup[name] = parameter

        for parsed_name, parsed_value in cls.parse(resource.__doc__).items():
            if parsed_name == "parameters":
                for parameter_name, parameter_value in parsed_value.items():
                    parameter_parsed = {"description": parameter_value} if isinstance(parameter_value, str) else parameter_value
                    for parameter_parsed_name, parameter_parsed_value in parameter_parsed.items():
                        if parameter_parsed_name == "description" and "description" in lookup[parameter_name]:
                            lookup[parameter_name]["description"] += " " + parameter_parsed_value
                        else:
                            lookup[parameter_name][parameter_parsed_name] = parameter_parsed_value
            else:
                parsed[parsed_name] = parsed_value

        if "return" in parsed:
            if isinstance(parsed["return"], str):
                parsed["return"] = {"description": parsed["return"]}

        if annotations["return"] and "type" not in parsed.get("return", {}):
            parsed.setdefault("return", {})
            parsed["return"].update(annotations["return"])

        return parsed

    @classmethod
    def attributes(cls,
        resource # what to extract attributes from
    )->dict:
        """
        description: Read attributes from a module or class, including their comments and docstrings
        parameters:
            resource:
                type:
                - function
                - method
        usage: |
            If you have attributes on a module, say the example module::

                a = None # The a team

                b = None # The b team
                \"""
                Not as good as the a team
                \"""

                big = \"""
                Stuff
                \""" # Bunch a
                \"""
                a: 1
                b: 2
                \"""

            You can extract/combime the descriptions and/or YAML like so::

                sphinxter.Reader.attributes(example)
                # {
                #     "a": {
                #         "description": "The a team"
                #     },
                #     "b": {
                #         "description": "The b team\\n\\nNot as good as the a team"
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
                    \"""
                    Not as good as the a team
                    \"""

                    big = \"""
                    Stuff
                    \""" # Bunch a
                    \"""
                    a: 1
                    b: 2
                    \"""

                sphinxter.Reader.attributes(example.Complex)
                # {
                #     "a": {
                #         "description": "The a team"
                #     },
                #     "b": {
                #         "description": "The b team\\n\\nNot as good as the a team"
                #     },
                #     "big": {
                #         "a": 1,
                #         "b": 2,
                #         "description": "Bunch a"
                #     }
                # })
        """

        parseds = {}
        targets = []

        nodes = ast.parse(cls.source(resource))

        if inspect.isclass(resource):
            nodes = nodes.body[0]

        for node in nodes.body:

            if targets and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):

                parsed = cls.parse(node.value.value)
                for target in targets:
                    cls.update(parseds[target], parsed)

            elif isinstance(node, ast.Assign):

                targets = [target.id for target in node.targets]

                for target in targets:
                    parseds.setdefault(target, {})

                source = io.StringIO(inspect.getsourcelines(resource)[0][node.end_lineno - 1][node.end_col_offset + 1:])

                for parsed in tokenize.generate_tokens(source.readline):
                    if parsed.type == token.COMMENT:
                        comment = parsed.string[2:].rstrip()
                        for target in targets:
                            parseds[target] = cls.parse(comment)

            else:

                targets = []

        return parseds

    @classmethod
    def cls(cls,
        resource # what to extract documentation from
    )->dict:
        """
        description: Reads all the documentation from a class for :any:`Writer.cls`
        parameters:
            resource:
                type: class
        usage: |
            Given this class is part of the example module::

                class Complex:
                    \"""
                    description: Complex class
                    definition: |
                        make sure you do this::

                            wowsa

                        Ya sweet
                    \"""

                    a = None # The a team
                    b = None # The b team
                    \"""
                    Not as good as the a team
                    \"""
                    big = \"""
                    Stuff
                    \""" # Bunch a
                    \"""
                    a: 1
                    b: 2
                    \"""

                    def __init__(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: call me
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    @classmethod
                    def classy(
                        cls,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some class meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type: str
                        \"""

                    def meth(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
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
                        \"""

                    class Subber:
                        \"""
                        Sub class
                        \"""
                        pass

            Reading all the documentation is as easy as::

                sphinxter.Reader.cls(example.Complex)
                # {
                #     "name": "Complex",
                #     "description": "Complex class\\n\\ncall me",
                #     "signature": "(a, b, *args, **kwargs)",
                #     "definition": "make sure you do this::\\n\\n    wowsa\\n\\nYa sweet\\n",
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
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n",
                #     "attributes": [
                #         {
                #             "name": "a",
                #             "description": "The a team"
                #         },
                #         {
                #             "name": "b",
                #             "description": "The b team\\n\\nNot as good as the a team"
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
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
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
        """

        parsed = {
            "name": resource.__name__,
            "attributes": [],
            "methods": [],
            "classes": []
        }

        parsed.update(cls.parse(resource.__doc__))

        try:

            cls.update(parsed, cls.routine(resource.__init__, method=True), skip=["name", "method"])

        except TypeError:

            pass

        attributes = cls.attributes(resource)

        for name, attr in {name: inspect.getattr_static(resource, name) for name in dir(resource)}.items():

            if (inspect.isfunction(attr) or isinstance(attr, (staticmethod, classmethod))):

                if name != "__init__":
                    parsed["methods"].append(cls.routine(attr, method=True))

            elif inspect.isclass(attr):

                parsed["classes"].append(cls.cls(attr))

            elif name in resource.__dict__ and not name.startswith('__') and not name.endswith('__'):

                attribute = {
                    "name": name
                }

                cls.update(attribute, attributes[name])

                parsed["attributes"].append(attribute)

        return parsed

    @classmethod
    def module(cls,
        resource # what to extract documentation from
    )->dict:
        """
        description: Reads all the documentation from a module for :any:`Writer.module`
        parameters:
            resource:
                type: module
        usage: |
            Say the following is the example module::

                \"""
                description: mod me
                usage: |
                    Do some cool stuff::

                        like this

                    It's great
                \"""

                a = None # The a team
                b = None # The b team
                \"""
                Not as good as the a team
                \"""
                big = \"""
                Stuff
                \""" # Bunch a
                \"""
                a: 1
                b: 2
                \"""

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    \"""
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
                    \"""

                class Basic:
                    \"""
                    Basic class
                    \"""

                class Complex:
                    \"""
                    description: Complex class
                    definition: |
                        make sure you do this::

                            wowsa

                        Ya sweet
                    \"""

                    a = None # The a team
                    b = None # The b team
                    \"""
                    Not as good as the a team
                    \"""
                    big = \"""
                    Stuff
                    \""" # Bunch a
                    \"""
                    a: 1
                    b: 2
                    \"""

                    def __init__(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: call me
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    class Subber:
                        \"""
                        Sub class
                        \"""
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
                #             "description": "The b team\\n\\nNot as good as the a team"
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
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
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
                #             "description": "Complex class\\n\\ncall me",
                #             "signature": "(a, b, *args, **kwargs)",
                #             "definition": "make sure you do this::\\n\\n    wowsa\\n\\nYa sweet\\n",
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
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n",
                #             "attributes": [
                #                 {
                #                     "name": "a",
                #                     "description": "The a team"
                #                 },
                #                 {
                #                     "name": "b",
                #                     "description": "The b team\\n\\nNot as good as the a team"
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
                #                     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
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
                #             "description": "The b team\\n\\nNot as good as the a team"
                #         },
                #         {
                #             "name": "big",
                #             "a": 1,
                #             "b": 2,
                #             "description": "Bunch a"
                #         }
                #     ],
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }
        """

        parsed = {
            "name": resource.__name__,
            "attributes": [],
            "functions": [],
            "classes": []
        }

        parsed.update(cls.parse(resource.__doc__))

        attributes = cls.attributes(resource)

        for name, attr in {name: inspect.getattr_static(resource, name) for name in dir(resource)}.items():

            if inspect.isfunction(attr):

                parsed["functions"].append(cls.routine(attr))

            elif inspect.isclass(attr):

                parsed["classes"].append(cls.cls(attr))

            elif name in attributes:

                attribute = {
                    "name": name
                }

                cls.update(attribute, attributes[name])

                parsed["attributes"].append(attribute)

        return parsed
