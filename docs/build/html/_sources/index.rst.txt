.. created by sphinxter
.. default-domain:: py

sphinxter
=========

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    *

.. module:: sphinxter

Converts YAML docstrings and code comments to sphinx documentation

.. class:: Sphinxter(modules, base='docs/source', indent='    ')

    Class for crawling code and generating documentation files

    :param modules: module or modules to crawl
    :param base: where to store generated documents
    :param indent:

    .. attribute:: base

    .. attribute:: documents

        list of documents

    .. attribute:: indent

    .. attribute:: modules

    .. method:: document(module, kind, parsed, current='index.rst')

        :param module:
        :param kind:
        :param parsed:
        :param current:

    .. method:: process()

        Reads modules and writes documents

    .. method:: read()

    .. method:: write()
