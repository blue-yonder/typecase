from __future__ import print_function, division, absolute_import
from ._types import ProductType, _This


class Record(ProductType):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __argtypes(self, parent):
        def _type_representation_for_typechecker(k, typval):
            if isinstance(typval, type):
                return "{}: {}".format(repr(k), typval.__name__)
            elif isinstance(typval, _This):
                return "{}: parent".format(k)
            else:
                raise TypeError("Unexpected type supplied: {}".format(typval))

        type_lst = [_type_representation_for_typechecker(k, self.kwargs[k])
                    for k in self.kwargs]
        return "{" + ",".join(type_lst) + "}"

    def _make_variant_class(self, parent, typename):
        class_definition = _record_template.format(parent=parent.__name__,
                                                   typename=typename,
                                                   argtypes=self.__argtypes(parent))
        namespace = dict(parent=parent,
                         __name__='meta_{}'.format(typename))
        try:
            exec(class_definition, namespace)
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + class_definition)
        return namespace[typename]

_record_template = """
class {typename}(parent):
    def __init__(self, **kwargs):
        self._check_types(kwargs)
        self.kwargs = kwargs

    def __getitem__(self, rhs):
        return self.kwargs[rhs]

    def __getattr__(self, item):
        if item in self.kwargs:
            return self.kwargs[item]
        else:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        if item == "kwargs":
            super({typename}, self).__setattr__(item, value)
        elif item in self.kwargs:
            raise TypeError("TypeError: 'Record' object does not support item assignment")
        else:
            raise AttributeError(item)

    @staticmethod
    def _check_types(kwargs):
        argtypes = {argtypes}
        if len(kwargs) != len(argtypes):
            raise TypeError("Number of kwargs {{n_args}} does not match the number "
                            "of supplied type {{n_type_args}}".format(n_args=len(kwargs),
                                                                    n_type_args=len(argtypes)))
        for item, typ in zip(kwargs, argtypes):
            if isinstance(typ, str):
                pass
            elif not isinstance(item, typ):
                raise TypeError("In {typename}, expected instance of `{{typ}}`"
                                " but got {{item}} of type `{{itemtype}}`"\
                                .format(typ=typ.__name__,
                                        item=repr(item),
                                        itemtype=type(item).__name__))

    def __repr__(self):
        args = ", ".join(["{{}}={{}}".format(k, repr(v))
                          for k, v in self.kwargs.items()])
        return "{parent}.{typename}({{args}})".format(args=args)
"""


__all__ = []
