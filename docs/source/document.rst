.. created by sphinxter
.. default-domain:: py

sphinxter.Document
==================

.. currentmodule:: sphinxter

.. class:: Content(module: str, kind: str, parsed: dict)

    Content for a document

    :param module: Name of module this content is for
    :type module: str
    :param kind: Kind of resource
    :type kind: str
    :param parsed: The parsed documentation
    :type parsed: dict

    .. attribute:: kind

        Kind of resource

    .. attribute:: module

        Name of module this content is for

    .. attribute:: parsed

        The parsed documentation

.. class:: Document(path: str, title: str, toctree, indent: str)

    Document (rst) to write out

    :param path: where to store the
    :type path: str
    :param title: title of the document
    :type title: str
    :param toctree: list of documents for toctree or False if none
    :type toctree: bool or list
    :param indent: string to use for indenting
    :type indent: str

    .. attribute:: contents

        document contents, keyed by order to list of contents

    .. attribute:: indent

        string to use for indenting

    .. attribute:: path

        where to store the document

    .. attribute:: title

        title of the document

    .. attribute:: toctree

        list of documents for toctree or False if none

    .. method:: add(module: str, kind: str, parsed: dict, order: int)

        Adds content to a document

        :param module: Name of module this content is for
        :type module: str
        :param kind: Kind of resource
        :type kind: str
        :param parsed: The parsed documentation
        :type parsed: dict
        :param order: Where to place this content
        :type order: int
