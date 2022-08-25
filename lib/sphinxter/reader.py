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
    sphinx: reader
    """

    @staticmethod
    def source(
        resource # what to extract the source from
    ):
        """
        description: Extracts the source, removing any overall indent
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
            docstring # the docstring (or string after an attribute)
        ):
        """
        description: Parses a docstring into YAML, default to description
        return:
            description: The parsed doctring
            type: dict
        usage: |

        """

        if docstring:
            parsed = yaml.safe_load(docstring)
            if isinstance(parsed, str):
                parsed = {"description": parsed}
        else:
            parsed = {}

        return parsed

    @classmethod
    def update(cls, primary, secondary, skip=None):

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
    def comments(cls, resource):

        parens = 0
        param = None
        params = False
        annotation = False
        comments = {}
        parseds = {}

        source = io.StringIO(cls.source(resource))

        for parsed in tokenize.generate_tokens(source.readline):

            if parsed.type == token.OP:
                if parsed.string == '(':
                    if parens == 0:
                        params = True
                    parens += 1
                elif parsed.string == ')':
                    parens -= 1
                    if parens == 0:
                        break
                elif parsed.string == ',':
                    annotation = False
            elif parsed.type == token.NAME:
                if params:
                    if not annotation:
                        param = parsed.string
                        parseds[param] = {}
                        annotation = True
                    else:
                        annotation = False
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
    def annotations(resource):

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
    def function(cls, resource, method=False):

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

        if method and not isinstance(resource, (staticmethod, classmethod)):
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

            parameter.update(comments[name])
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
    def attributes(cls, resource, body=False):

        parseds = {}
        targets = []

        nodes = ast.parse(cls.source(resource))

        if body:
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
    def cls(cls, resource):

        parsed = {
            "name": resource.__name__,
            "attributes": [],
            "methods": [],
            "classes": []
        }

        parsed.update(cls.parse(resource.__doc__))

        try:

            cls.update(parsed, cls.function(resource.__init__, method=True), skip=["name", "method"])

        except TypeError:

            pass

        attributes = cls.attributes(resource, body=True)

        for name, attr in {name: inspect.getattr_static(resource, name) for name in dir(resource)}.items():

            if (inspect.isfunction(attr) or isinstance(attr, (staticmethod, classmethod))):

                if name != "__init__":
                    parsed["methods"].append(cls.function(attr, method=True))

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
    def module(cls, resource):
        """
        Dude
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

                parsed["functions"].append(cls.function(attr))

            elif inspect.isclass(attr):

                parsed["classes"].append(cls.cls(attr))

            elif name in attributes:

                attribute = {
                    "name": name
                }

                cls.update(attribute, attributes[name])

                parsed["attributes"].append(attribute)

        return parsed
