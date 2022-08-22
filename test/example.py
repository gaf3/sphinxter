"""
mod me
"""

a = None # The a team
b = None # The b team
"""
Not as good as the a team
"""
big = """
Stuff
""" # Bunch a
"""
a: 1
b: 2
"""

def func(
    a, # The a
    b, # The b
    *args,   #
    **kwargs # a: 1
             # b: 2
):
    """
    description: Some basic func
    parameters:
      a: More stuff
      b:
        more: stuff
    return:
        description: things
        type:
        - str
        - None
    raises:
        Exception: if oh noes
    usage: |
        Do some cool stuff::

            like this

        It's great
    """


class Basic:
    """
    Basic class
    """


class Complex:
    """
    description: Complex class
    definition: |
        make sure you do this::

            wowsa

        Ya sweet
    """

    a = None # The a team
    b = None # The b team
    """
    Not as good as the a team
    """
    big = """
    Stuff
    """ # Bunch a
    """
    a: 1
    b: 2
    """

    def __init__(
        self,
        a,       # The a
        b,       # The b
        *args,   #
        **kwargs # a: 1
                 # b: 2
    ):
        """
        description: call me
        parameters:
          a: More stuff
          b:
            more: stuff
        usage: |
            Do some cool stuff::

                like this

            It's great
        """

    @staticmethod
    def stat(
        a,       # The a
        b,       # The b
        *args,   #
        **kwargs # a: 1
                 # b: 2
    ):
        """
        description: Some static stat
        parameters:
          a: More stuff
          b:
            more: stuff
        return: things
        """

    @classmethod
    def classy(
        a,       # The a
        b,       # The b
        *args,   #
        **kwargs # a: 1
                 # b: 2
    ):
        """
        description: Some class meth
        parameters:
          a: More stuff
          b:
            more: stuff
        return:
            description: things
            type: str
        """

    def meth(
        self,
        a,       # The a
        b,       # The b
        *args,   #
        **kwargs # a: 1
                 # b: 2
    ):
        """
        description: Some basic meth
        parameters:
          a: More stuff
          b:
            more: stuff
        return:
            description: things
            type:
            - str
            - None
        raises:
            Exception: if oh noes
        usage: |
            Do some cool stuff::

                like this

            It's great
        """

    class Subber:
        """
        Sub class
        """
        pass
