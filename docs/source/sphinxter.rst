.. created by sphinxter
.. default-domain:: py

sphinxter.Sphinxter
===================

.. currentmodule:: sphinxter

.. class:: Sphinxter(modules: 'module or list[module]', titles: dict = None, toctree: dict = None, base: str = 'docs/source', indent: str = '    ')

    Class for reading documentation and writing into documents

    :param modules: module or modules to read
    :type modules: module or list[module]
    :param titles: document titles to use
    :type titles: dict
    :param toctree: list of document names to use for the main toctree
    :type toctree: dict
    :param base: base directory to store generated documents
    :type base: str
    :param indent: string to use for indenting
    :type indent: str

    .. attribute:: base

        base directory to write documents

    .. attribute:: documents

        hash of documents, keyed by name

    .. attribute:: indent

        string to use for indenting

    .. attribute:: modules

        list of modules to read

    .. attribute:: titles

        hash of titles, keyed by document name

    .. attribute:: toctree

    .. method:: document(module: str, kind: str, parsed: dict, current: str = 'index')

        Adds a resource's documentation to its document

        :param module: resource's parent module's name
        :type module: str
        :param kind: resource's kind, module, function, or class
        :type kind: str
        :param parsed: resource's parsed documentation
        :type parsed: dict
        :param current: the last document named
        :type current: str

        **Usage**

        You can specify a resource's document and order in that document
        with a `document` directive in the YAML::

            def func():
                """
                document:
                    path: different
                    order: 10
                """

            # {
            #     "path": "different",
            #     "order": 10
            # }

        This would place the func function in the different.rst document with all
        the other resources at the 10 posiiton.

        If you only specify document as a `str`, it assume you meant path and
        that order is 0::

            def func():
                """
                document: different
                """

            # {
            #     "path": "different",
            #     "order": 0
            # }

        If you only specify document as an `int`, it assume you meant order and
        that the path hasn't changed::

            def func():
                """
                document: 10
                """

            # {
            #     "path": "index",
            #     "order": 10
            # }

    .. method:: process()

        Reads module(s) and writes document(s) end to end

    .. method:: read()

        Reads all the documentation into their document(s)

    .. method:: write()

        Writes all document(s)
