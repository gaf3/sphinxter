.. created by sphinxter
.. default-domain:: py

sphinxter.Sphinxter
===================

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    self
    reader
    writer
    document

.. module:: sphinxter

Converts YAML docstrings and code comments to sphinx documentation

.. class:: Sphinxter(modules, titles=None, toctree=None, base='docs/source', indent='    ')

    Class for crawling code and generating documentation files

    :param modules: module or modules to crawl
    :param titles:
    :param toctree:
    :param base: where to store generated documents
    :param indent:

    .. attribute:: base

    .. attribute:: documents

        list of documents

    .. attribute:: indent

    .. attribute:: modules

    .. attribute:: titles

    .. attribute:: toctree

    .. method:: document(module, kind, parsed, current='index')

        :param module:
        :param kind:
        :param parsed:
        :param current:

    .. method:: process()

        Reads modules and writes documents

    .. method:: read()

    .. method:: write()
