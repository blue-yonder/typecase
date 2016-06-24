from __future__ import print_function, division, absolute_import
from ._types import ProductType, _This


class Record(ProductType):
    def __init__(self, **type_mappings):
        self.__type_mappings = type_mappings

    def __argtypes(self, parent):
        def _type_representation_for_typechecker(k, typval):
            if isinstance(typval, type):
                return "{}: {}".format(repr(k), typval.__name__)
            elif isinstance(typval, _This):
                return "'{}': parent".format(k)
            else:
                raise TypeError("Unexpected type supplied: {}".format(typval))

        type_lst = [_type_representation_for_typechecker(k, self.__type_mappings[k])
                    for k in self.__type_mappings]
        return "{" + ",".join(type_lst) + "}"

    def _make_variant_class(self, parent, typename):
        class_definition = _record_template.format(parent=parent.__name__,
                                                   typename=typename,
                                                   type_mappings=self.__argtypes(parent))
        namespace = dict(parent=parent,
                         on_same_keys=on_same_keys,
                         __name__='meta_{}'.format(typename))
        try:
            exec(class_definition, namespace)
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + class_definition)
        return namespace[typename]


def on_same_keys(d1, d2):
    if set(d1.keys()) != set(d2.keys()):
        raise KeyError("on_same_keys expects that both dictionaries share the same key")
    for key in d1.keys():
        yield (d1[key], d2[key])


_record_template = """
class {typename}(parent):
    def __init__(self, **mappings):
        self.__mappings = mappings
        self._check_types(mappings)

    @staticmethod
    def _check_types(mappings):
        type_mappings = {type_mappings}
        format_args = dict()
        format_args["typenames_def"] = type_mappings.keys()
        format_args["typenames_constr"] = mappings.keys()
        if set(mappings.keys()) != set(type_mappings.keys()):
            raise TypeError("Attribute names {{typenames_constr}}"
                            "differ from those given in the definition "
                            " {{typenames_def}}".format(**format_args))
        for item, typ in on_same_keys(mappings, type_mappings):
            if isinstance(typ, str):
                pass
            elif not isinstance(item, typ):
                raise TypeError("In {typename}, expected instance of `{{typ}}`"
                                " but got {{item}} of type `{{itemtype}}`"\
                                .format(typ=typ.__name__,
                                        item=repr(item),
                                        itemtype=type(item).__name__))

    def __getitem__(self, rhs):
        return self.__mappings[rhs]

    def __getattr__(self, item):
        if item in self.__mappings:
            return self.__mappings[item]
        else:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        if item == "_{typename}__mappings":
            super({typename}, self).__setattr__(item, value)
        elif item in self.__mappings:
            raise TypeError("TypeError: 'Record' object does not support item assignment")
        else:
            raise AttributeError(item)


    def __repr__(self):
        args = ", ".join(["{{}}={{}}".format(k, repr(v))
                          for k, v in self.__mappings.items()])
        return "{parent}.{typename}({{args}})".format(args=args)
"""


__all__ = []
