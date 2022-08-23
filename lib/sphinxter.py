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
            "signature": str(signature)
        }

        if method:
            parsed["method"] = kind

        lookup = {}
        parameters = cls.parameters(resource)

        for name in signature.parameters:

            parsed.setdefault("parameters", [])

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


class Content:

    module = None
    kind = None
    parsed = None

    def __init__(self, module, kind, parsed):

        self.module = module
        self.kind = kind
        self.parsed = parsed


class Document:
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

    document = None
    file = None

    def __init__(self, document, file):

        self.document = document
        self.file = file

    def line(self, line='', indent=0, before=False, after=False):

        if before:
            self.file.write("\n")

        self.file.write(f"{self.document.indent * indent}{line}".rstrip())

        self.file.write("\n")

        if after:
            self.file.write("\n")

    def lines(self, lines, indent, before=False, after=False):

        if before:
            self.file.write("\n")

        for line in lines.split("\n"):
            self.line(line, indent)

        if after:
            self.file.write("\n")

    @staticmethod
    def types(types):

        if not isinstance(types, list):
            types = [types]

        return " or ".join(types)

    def description(self, parsed, indent):

        if "description" not in parsed:
            return

        self.lines(parsed["description"].rstrip(), indent, before=True)

    def parameter(self, parsed, indent):

        if "description" in parsed:
            self.line(f":param {parsed['name']}: {parsed['description']}", indent)
        else:
            self.line(f":param {parsed['name']}:", indent)

        if "type" in parsed:
            self.line(f":type {parsed['name']}: {self.types(parsed['type'])}", indent)

    def parameters(self, parsed, indent):

        if "parameters" not in parsed:
            return

        for parameter in parsed["parameters"]:
            self.parameter(parameter, indent)

    def returns(self, parsed, indent):

        if "return" not in parsed:
            return

        if "description" in parsed['return']:
            self.line(f":return: {parsed['return']['description']}", indent)

        if "type" in parsed['return']:
            self.line(f":rtype: {self.types(parsed['return']['type'])}", indent)

    def raises(self, parsed, indent):

        if "raises" not in parsed:
            return

        for exception in sorted(parsed["raises"].keys()):
            self.line(f":raises {exception}: {parsed['raises'][exception]}", indent)

    def execution(self, parsed, indent):

        if (
            "parameters" not in parsed and
            "return" not in parsed and
            "raises" not in parsed
        ):
            return

        self.line()
        self.parameters(parsed, indent)
        self.returns(parsed, indent)
        self.raises(parsed, indent)

    def usage(self, parsed, indent):

        if "usage" not in parsed:
            return

        self.line("**Usage**", indent, before=True, after=True)
        self.lines(parsed["usage"].rstrip(), indent)

    def function(self, parsed, indent=0):

        self.line(f".. function:: {parsed['name']}{parsed['signature']}", indent, before=True)

        self.description(parsed, indent+1)
        self.execution(parsed, indent+1)
        self.usage(parsed, indent+1)

    def attribute(self, parsed, indent):

        self.line(f".. attribute:: {parsed['name']}", indent, before=True)

        if "type" in parsed:
            self.line(f":type: {self.types(parsed['type'])}", indent+1)

        self.description(parsed, indent+1)

    def attributes(self, parsed, indent):

        if "attributes" not in parsed:
            return

        for attribute in parsed["attributes"]:
            self.attribute(attribute, indent)

    def method(self, parsed, indent):

        self.line()
        self.line(f".. {parsed['method']}method:: {parsed['name']}{parsed['signature']}", indent)

        self.description(parsed, indent+1)
        self.execution(parsed, indent+1)
        self.usage(parsed, indent+1)

    def definition(self, parsed, indent):

        if "definition" not in parsed:
            return

        self.line("**Definition**", indent, before=True, after=True)
        self.lines(parsed["definition"].rstrip(), indent)

    def cls(self, parsed, indent=0):

        self.line(f".. class:: {parsed['name']}{parsed.get('signature', '')}", indent, before=True)

        self.description(parsed, indent+1)
        self.definition(parsed, indent+1)
        self.execution(parsed, indent+1)
        self.usage(parsed, indent+1)
        self.attributes(parsed, indent+1)

        for method in parsed["methods"]:
            self.method(method, indent+1)

    def module(self, parsed, indent=0):

        self.line(f".. module:: {parsed['name']}", indent, before=True, after=True)

        self.line(parsed['name'], indent)
        self.line('=' * len(parsed['name']), indent)

        self.description(parsed, indent)
        self.attributes(parsed, indent)

    def dump(self):

        self.line(".. created by sphinxter")
        self.line(".. default-domain:: py")

        module = None

        for index in sorted(self.document.contents.keys()):
            for content in self.document.contents[index]:

                if content.kind == "module":
                    self.module(content.parsed)
                    module = content.module
                elif module != content.module:
                    module = content.module
                    self.line(f".. currentmodule:: {module}", before=True)

                if content.kind == "function":
                    self.function(content.parsed)

                if content.kind == "class":
                    self.cls(content.parsed)


class Sphinxter:
    """
    Class for crawling code and generating documentation files
    """

    modules = None
    base = None
    indent = None
    documents = None # list of documents

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
        self.documents = {}

    def document(self, module, kind, parsed, current='index.rst'):

        sphinx = parsed.get("sphinx", {})

        if isinstance(sphinx, bool) and not sphinx:
            return

        path = sphinx.get("path", current)
        order = sphinx.get("order", 0)

        if path not in self.documents:
            self.documents[path] = Document(f"{self.base}/{path}", indent=self.indent)

        self.documents[path].add(module, kind, parsed, order)

        return path

    def read(self):

        for module in self.modules:

            parsed = Reader.module(module)

            path = self.document(parsed['name'], "module", parsed)

            for function in parsed["functions"]:
                self.document(parsed['name'], "function", function, path)

            for cls in parsed["classes"]:
                self.document(parsed['name'], "class", cls, path)

    def write(self):

        for document in self.documents.values():
            with open(document.path, "w") as file:
                Writer(document, file).dump()

    def process(self):
        """
        Reads modules and writes documents
        """

        self.read()
        self.write()
