.. created by sphinxter
.. default-domain:: py

sphinxter.Reader
================

.. currentmodule:: sphinxter

.. class:: Reader

    Static class for reading doc strings and comments into dict's

    .. staticmethod:: annotations(resource)

        :param resource:

    .. classmethod:: attributes(cls, resource, body=False)

        :param cls:
        :param resource:
        :param body:

    .. classmethod:: cls(cls, resource)

        :param cls:
        :param resource:

    .. classmethod:: comments(cls, resource)

        :param cls:
        :param resource:

    .. classmethod:: function(cls, resource, method=False)

        :param cls:
        :param resource:
        :param method:

    .. classmethod:: module(cls, resource)

        Dude

        :param cls:
        :param resource:

    .. staticmethod:: parse(docstring)

        Parses a docstring into YAML, default to description

        :param docstring: the docstring (or string after an attribute)
        :return: The parsed doctring
        :rtype: dict

        **Usage**



    .. staticmethod:: source(resource)

        Extracts the source, removing any overall indent

        :param resource: what to extract the source from
        :type resource: module or function or class or method
        :return: The non-indented source
        :rtype: str

        **Usage**


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

    .. classmethod:: update(cls, primary, secondary, skip=None)

        :param cls:
        :param primary:
        :param secondary:
        :param skip:
