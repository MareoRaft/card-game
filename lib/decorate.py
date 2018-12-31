""" Useful decorators.  The `transparent` decorator is taken from https://wiki.python.org/moin/PythonDecoratorLibrary.
"""


def transparent(decorator):
    """ Decorators have a few unwanted side effects.  This decorator, when used on a decorator, reverses those side-effects!

    Longer explanation: This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @transparent to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied.
    """
    def new_decorator(func, *args, **kwargs):
        g = decorator(func, *args, **kwargs)
        g.__name__ = func.__name__
        g.__doc__ = func.__doc__
        g.__dict__.update(func.__dict__)
        return g
    # Now a few lines needed to make transparent *itself*
    # be a well-behaved decorator!
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


@transparent
def read_only(func):
    """ Allows a property to only be set ONCE.  After that, it cannot be set again.  Usage:

    class BlaBla:
        def __init__(self, value):
            self.v = value
        @property
        def v(self):
            return self._v
        @v.setter
        @read_only
        def v(self, new_value):
            self._v = new_value
    """

    def new_func(self, *args, **kwargs):
        secret_attr_name = func.__name__ + "_read_only_property_set"
        if hasattr(self, secret_attr_name):
            raise Exception(
                'This property is read-only.  It can only be set ONCE, and has already been set.')
        else:
            out = func(self, *args, **kwargs)
            setattr(self, secret_attr_name, True)
            return out
    return new_func
