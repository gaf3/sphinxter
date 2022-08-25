"""
Converts YAML docstrings and code comments to sphinx documentation
"""

from sphinxter.reader import Reader
from sphinxter.writer import Writer

class Content:
    """
    sphinx: document
    """

    module = None
    kind = None
    parsed = None

    def __init__(self, module, kind, parsed):

        self.module = module
        self.kind = kind
        self.parsed = parsed


class Document:
    """
    sphinx: document
    """

    path = None
    title = None
    indent = None
    toctree = None
    contents = None

    def __init__(self, path, title, toctree, indent):

        self.path = path
        self.title = title
        self.toctree = toctree
        self.indent = indent
        self.contents = {}

    def add(self, module, kind, parsed, order):

        self.contents.setdefault(order, [])
        self.contents[order].append(Content(module, kind, parsed))


class Sphinxter:
    """
    Class for crawling code and generating documentation files
    """

    modules = None
    base = None
    indent = None
    documents = None # list of documents
    titles = None
    toctree = None

    def __init__(
        self,
        modules,           # module or modules to crawl
        titles=None,
        toctree=None,
        base="docs/source", # where to store generated documents
        indent='    '
    ):

        if not isinstance(modules, list):
            modules = [modules]

        self.modules = modules
        self.base = base
        self.titles = titles if titles is not None else {}
        self.toctree = toctree if toctree is not None else ['self', '*']
        self.indent = indent
        self.documents = {}

    def document(self, module, kind, parsed, current='index'):

        sphinx = parsed.get("sphinx", {})

        if isinstance(sphinx, bool) and not sphinx:
            return current

        if isinstance(sphinx, str):
            sphinx = {"path": sphinx}

        if isinstance(sphinx, int):
            sphinx = {"order": sphinx}

        path = sphinx.get("path", current)
        order = sphinx.get("order", 0)

        if path not in self.documents:

            if path != 'index':
                title = self.titles.get(path, path)
                toctree = False
            else:
                title = self.titles.get(path, module)
                toctree = self.toctree

            self.documents[path] = Document(f"{self.base}/{path}.rst", title, toctree, self.indent)

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
            with open(document.path, "w", encoding="utf-8") as file:
                Writer(document, file).dump()

    def process(self):
        """
        Reads modules and writes documents
        """

        self.read()
        self.write()