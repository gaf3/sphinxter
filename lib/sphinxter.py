"""
Converts YAML docstrings to sphinx documentation
"""

import io
import ast
import inspect
import token
import tokenize
import yaml

class Reader:
    """
    Class for crawling modules
    """

    @staticmethod
    def source(resource):

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
    def parse(string):

        if string:
            parsed = yaml.safe_load(string)
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
            elif name == "description" and "description" in primary:
                primary[name] += "\n\n" + value
            else:
                primary[name] = value

    @classmethod
    def parameters(cls, resource):

        parens = 0
        param = None
        params = False
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
            elif parsed.type == token.NAME:
                if params:
                    param = parsed.string
                    parseds[param] = {}
            elif parsed.type == token.COMMENT:
                if param is not None:
                    comment = parsed.string[2:].rstrip()
                    if not comment:
                        continue
                    if param not in comments:
                        comments[param] = comment
                    else:
                        comments[param] = f"{comments[param]}\n{comment}"

        for param in comments:
            parseds[param].update(cls.parse(comments[param]))

        return parseds

    @classmethod
    def function(cls, resource, method=False):

        if isinstance(resource, staticmethod):
            kind = "static"
            signature = inspect.signature(resource)
        elif isinstance(resource, classmethod):
            kind = "class"
            signature = inspect.signature(resource.__func__)
        else:
            kind = ""
            signature = inspect.signature(resource)

        if method and not isinstance(resource, (staticmethod, classmethod)):
            signature = signature.replace(parameters=list(signature.parameters.values())[1:])

        parsed = {
            "name": resource.__name__,
            "signature": str(signature),
            "parameters": []
        }

        if method:
            parsed["method"] = kind

        lookup = {}
        parameters = cls.parameters(resource)

        for name in signature.parameters:

            parameter = {
                "name": name
            }

            parameter.update(parameters[name])

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

            parsed["signature"] = ""
            parsed["parameters"] = []

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


class Content:

    module = None
    kind = None
    parsed = None

    def __init__(self, module, kind, parsed):

        self.module = module
        self.kind = kind
        self.parsed = parsed


class Doc:
    """
    Class for a documentation file
    """

    path = None
    indent = None
    contents = None

    def __init__(self, path, indent):

        self.path = path
        self.indent = indent
        self.contents = {}

    def add(self, module, kind, parsed, order):

        self.contents.setdefault(order, [])
        self.contents[order].append(Content(module, kind, parsed))


class Writer:

    doc = None
    file = None

    def __init__(self, doc, file):

        self.doc = doc
        self.file = file

    def line(self, indent, line, extra=False):

        self.file.write(f"{self.doc.indent * indent}{line}\n")

        if extra:
            self.file.write("\n")

    def lines(self, indent, lines, extra=False):

        for line in lines.split("\n"):
            self.line(indent, line)

        if extra:
            self.file.write("\n")

    def types(zelf, types):

        if not isinstance(types, list):
            types = [types]

        return " or ".join(types)

    def description(self, indent, parsed):

        if "description" in parsed:
            self.lines(indent, parsed["description"], True)

    def parameter(self, indent, parsed):

        self.line(indent, f":param {parsed['name']}: {parsed.get('description', '')}")

        if "type" in parsed:
            self.line(indent, f":type: {self.types(parsed['type'])}")

    def parameters(self, indent, parsed):

        if not parsed["parameters"]:
            return

        for parameter in parsed["parameters"]:
            self.parameter(indent, parameter)

        self.line(0,"")

    def returns(self, indent, parsed):

        if "return" not in parsed:
            return

        self.line(indent, f":return: {parsed['return'].get('description', '')}")

        if "type" in parsed['return']:
            self.line(indent, f":rtype: {self.types(parsed['return']['type'])}")

    def raises(self, indent, parsed):

        if "raises" not in parsed:
            return

        for exception in sorted(parsed["raises"].keys()):
            self.line(indent, f":raises {exception}: {parsed['raises'][exception]}")

    def usage(self, indent, parsed):

        if "usage" not in parsed:
            return

        self.line(0,"")
        self.line(indent,"**Usage**", True)
        self.lines(indent, parsed["usage"], True)

    def function(self, indent, parsed):

        self.line(indent, f".. function:: {parsed['name']}{parsed['signature']}", True)

        self.description(indent+1, parsed)
        self.parameters(indent+1, parsed)
        self.returns(indent+1, parsed)
        self.raises(indent+1, parsed)
        self.usage(indent+1, parsed)

    def attribute(self, indent, parsed):

        self.line(indent, f".. attribute:: {parsed['name']}")

        if "type" in parsed:
            self.line(indent+1, f":type: {self.types(parsed['type'])}")

        self.line(0,"")

        self.description(indent+1, parsed)

    def attributes(self, indent, parsed):

        if not parsed["attributes"]:
            return

        for attribute in parsed["attributes"]:
            self.attribute(indent, attribute)

        self.line(0,"")

    def method(self, indent, parsed):

        self.line(indent, f".. {parsed['method']}method:: {parsed['name']}{parsed['signature']}")

        self.line(0,"")

        self.description(indent+1, parsed)
        self.parameters(indent+1, parsed)
        self.returns(indent+1, parsed)
        self.raises(indent+1, parsed)
        self.usage(indent+1, parsed)

    def definition(self, indent, parsed):

        if "definition" not in parsed:
            return

        self.line(0,"")
        self.line(indent,"**Definition**", True)
        self.lines(indent, parsed["definition"], True)

    def cls(self, indent, parsed):

        self.line(indent, f".. class:: {parsed['name']}{parsed['signature']}", True)

        self.description(indent+1, parsed)
        self.definition(indent+1, parsed)
        self.parameters(indent+1, parsed)
        self.raises(indent+1, parsed)
        self.usage(indent+1, parsed)
        self.attributes(indent+1, parsed)

        for method in parsed["methods"]:
            self.method(indent+1, method)

    def module(self, indent, parsed):

        self.line(indent, f".. module:: {parsed['name']}", True)

        self.line(indent, parsed['name'])
        self.line(indent, '=' * len(parsed['name']), True)

        self.description(indent, parsed)
        self.attributes(indent, parsed)

    def dump(self):

        self.line(0, ".. created by sphinxter")
        self.line(0, ".. default-domain:: py", True)

        module = None

        for index in sorted(self.doc.contents.keys()):
            for content in self.doc.contents[index]:

                if content.kind == "module":
                    self.module(0, content.parsed)
                    module = content.parsed['name']
                elif module != content.module['name']:
                    module = content.module['name']
                    self.line(0, f".. currentmodule:: {module}", True)

                if content.kind == "function":
                    self.function(0, content.parsed)

                if content.kind == "class":
                    self.cls(0, content.parsed)


class Sphinxter:
    """
    Class for crawling code and generating documentation files
    """

    modules = None
    base = None
    indent = None
    docs = None # list of documents

    def __init__(
        self,
        modules,           # module or modules to crawl
        base="docs/source", # where to store generated documents
        indent='    '
    ):

        if not isinstance(modules, list):
            modules = [modules]

        self.modules = modules
        self.base = base
        self.indent = indent
        self.docs = {}

    def doc(self, module, kind, parsed, current='index.rst'):

        sphinx = parsed.get("sphinx", {})

        if isinstance(sphinx, bool) and not sphinx:
            return

        location = sphinx.get("location", current)
        order = sphinx.get("order", 0)

        if location not in self.docs:
            self.docs[location] = Doc(f"{self.base}/{location}", indent=self.indent)

        self.docs[location].add(module, kind, parsed, order)

        return location

    def read(self):

        for module in self.modules:

            parsed = Reader.module(module)

            location = self.doc(parsed, "module", parsed)

            for function in parsed["functions"]:
                self.doc(parsed, "function", function, location)

            for cls in parsed["classes"]:
                self.doc(parsed, "class", cls, location)

    def write(self):

        for doc in self.docs.values():
            with open(doc.path, "w") as file:
                Writer(doc, file).dump()

    def process(self):
        """
        Crawls modules and generates docs
        """

        self.read()
        self.write()
