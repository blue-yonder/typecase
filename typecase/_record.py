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
                return "'{}': parent".format(k)
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
                         on_same_keys=on_same_keys,
                         __name__='meta_{}'.format(typename))
        try:
            exec(class_definition, namespace)
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + class_definition)
        return namespace[typename]


def on_same_keys(d1, d2):
    for key in d1.keys():
        yield (d1[key], d2[key])


_record_template = """
class {typename}(parent):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self._check_types(kwargs)

    @staticmethod
    def _check_types(kwargs):
        argtypes = {argtypes}
        format_args = dict()
        format_args["typenames_def"] = argtypes.keys()
        format_args["typenames_constr"] = kwargs.keys()
        if set(kwargs.keys()) != set(argtypes.keys()):
            raise TypeError("Attribute names {{typenames_constr}}"
                            "differ from those given in the definition "
                            " {{typenames_def}}".format(**format_args))
        for item, typ in on_same_keys(kwargs, argtypes):
            if isinstance(typ, str):
                pass
            elif not isinstance(item, typ):
                raise TypeError("In {typename}, expected instance of `{{typ}}`"
                                " but got {{item}} of type `{{itemtype}}`"\
                                .format(typ=typ.__name__,
                                        item=repr(item),
                                        itemtype=type(item).__name__))

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


    def __repr__(self):
        args = ", ".join(["{{}}={{}}".format(k, repr(v))
                          for k, v in self.kwargs.items()])
        return "{parent}.{typename}({{args}})".format(args=args)
"""


__all__ = []
