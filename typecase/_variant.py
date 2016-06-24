from __future__ import print_function, division, absolute_import

from six import iteritems

from ._types import ProductType


def is_valid_typename(name):
    if name[0].islower():
        return False
    elif "_" in name:
        return False
    return True


def check_type_names(variants_types):
    for name, typ in iteritems(variants_types):
        if not is_valid_typename(name):
            raise NameError("Given type name {name} does not adhere to the naming constraint:"
                            " CamelCase without underscores.".format(name=name))


def variant(cls):
    variants = {name: getattr(cls, name)
                for name in cls.__dict__
                if isinstance(getattr(cls, name), ProductType)}

    variants_types = {k: v._make_variant_class(cls, k)
                      for k, v in iteritems(variants)}

    check_type_names(variants_types)

    for name, typ in iteritems(variants_types):
        setattr(cls, name, typ)
    return cls


__all__ = []
