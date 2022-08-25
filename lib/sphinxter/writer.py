"""
Module for writing out documents
"""

class Writer:
    """
    description: Class for writing out documents
    sphinx: writer.rst
    """

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

        self.line(f".. module:: {parsed['name']}", indent, before=True)

        self.description(parsed, indent)
        self.attributes(parsed, indent)

    def toctree(self, indent=0):

        self.line(".. toctree::", indent, before=True)
        self.line(":maxdepth: 1", indent+1)
        self.line(":glob:", indent+1)
        self.line(":hidden:", indent+1)
        self.line("*", indent+1, before=True)

    def dump(self):

        self.line(".. created by sphinxter")
        self.line(".. default-domain:: py")

        self.line(self.document.title, before=True)
        self.line('=' * len(self.document.title))

        if self.document.toctree:
            self.toctree()

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
