.. created by sphinxter
.. default-domain:: py

sphinxter.Document
==================

.. currentmodule:: sphinxter

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
        :type: dict

        document contents

        If a resource's document block has an order (default zero) that
        order is used as the key in the contents dict, to a list of contents
        for that order. That way, if nothing is specified, everything is added
        alphabetically. However, if you want a more obscure resource to go last,
        you just need to set the order greater that zero. Two resources at the
        same order are displayed the order in which they were added.

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

    .. class:: Content(module: str, kind: str, parsed: dict)

        Content for a Document

        :param module: Name of module this content is for
        :type module: str
        :param kind: Kind of resource
        :type kind: str
        :param parsed: The parsed documentation
        :type parsed: dict

        .. attribute:: kind

            Name of module this content is for

        .. attribute:: module

        .. attribute:: parsed

            Kind of resource
