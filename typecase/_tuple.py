from __future__ import print_function, division, absolute_import
import six

from ._types import ProductType, _This
from six.moves import map


class Tuple(ProductType):
    def __init__(self, *args):
        self.args = args

    def __argtypes(self, parent):
        def _type_representation_for_typechecker(typval):
            if isinstance(typval, type):
                return typval.__name__
            elif isinstance(typval, six.string_types):
                return repr(typval)
            elif isinstance(typval, _This):
                return "parent"

        type_lst = list(map(_type_representation_for_typechecker, self.args))
        return "[" + ",".join(type_lst) + "]"

    def _make_variant_class(self, parent, typename):
        class_definition = _tuple_template.format(parent=parent.__name__,
                                                  typename=typename,
                                                  argtypes=self.__argtypes(parent))
        namespace = dict(parent=parent,
                         __name__='meta_{}'.format(typename))
        try:
            exec(class_definition, namespace)
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + class_definition)
        dynamic_classname = namespace[typename]
        assert issubclass(dynamic_classname, tuple)
        assert type(dynamic_classname) != tuple
        return dynamic_classname

_tuple_template = """
class {typename}(tuple, parent):
    def __new__(cls, *args):
        cls._check_types(args)
        return super({typename}, cls).__new__(cls, args)

    @staticmethod
    def _check_types(args):
        argtypes = {argtypes}
        for item, typ in zip(args, argtypes):
            if isinstance(typ, str):
                pass
            elif not isinstance(item, typ):
                raise TypeError("In {typename}, expected instance of `{{typ}}`"
                                " but got {{item}} of type `{{itemtype}}`"\
                                .format(typ=typ.__name__,
                                        item=repr(item),
                                        itemtype=type(item).__name__))

    def __repr__(self):
        return "{parent}.{typename}" + repr(tuple(self))
"""


class Empty(Tuple):
    def __init__(self):
        super(Empty, self).__init__()

    def __argtypes(self, parent):
        return "[]"

__all__ = []
