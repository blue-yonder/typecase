from __future__ import print_function, division, absolute_import
import six

from ._types import ProductType, _This
from six.moves import map


def _type_representation_for_typechecker(typval):
    if isinstance(typval, type):
        return typval.__name__
    elif isinstance(typval, _This):
        return "parent"
    elif isinstance(typval, six.string_types):
        return repr(typval)
    else:
        raise TypeError("Unexpected type supplied: {}".format(typval))


class Tuple(ProductType):
    def __init__(self, *args):
        self.args = args

    def __argtypes(self, parent):
        type_lst = map(_type_representation_for_typechecker, self.args)
        return "[" + ",".join(type_lst) + "]"

    def _make_variant_class(self, parent, typename):
        class_definition = _tuple_template.format(parent=parent.__name__,
                                                  typename=typename,
                                                  argtypes=self.__argtypes(parent))
        namespace = dict(parent=parent,
                         _TupleMixin=_TupleMixin,
                         __name__='meta_{}'.format(typename))
        try:
            exec(class_definition, namespace)
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + class_definition)

        return namespace[typename]


# the more functionality is here instead of the _tuple_template variable, the
# better
class _TupleMixin(object):
    @classmethod
    def _check_types(cls, args):
        argtypes = cls._argtypes
        if len(args) != len(argtypes):
            raise TypeError("Number of args {n_args} does not match the number "
                            "of supplied type {n_type_args}".format(n_args=len(args),
                                                                    n_type_args=len(argtypes)))
        for item, typ in zip(args, argtypes):
            if isinstance(typ, str):
                pass
            elif not isinstance(item, typ):
                raise TypeError("In {typename}, expected instance of `{typ}`"
                                " but got {item} of type `{itemtype}`"
                                .format(typ=typ.__name__,
                                        item=repr(item),
                                        typename=cls.__name__,
                                        itemtype=type(item).__name__))


_tuple_template = """
class {typename}(parent, _TupleMixin):
    def __init__(self, *args):
        self._check_types(args)
        self.__values = tuple(args)
        super({typename}, self).__init__()

    _argtypes = {argtypes}

    def __getitem__(self, rhs):
        return self.__values[rhs]

    def __repr__(self):
        return "{parent}.{typename}" + repr(self.__values)
"""


class Empty(Tuple):
    def __init__(self):
        super(Empty, self).__init__()

__all__ = []
