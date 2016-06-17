from __future__ import print_function, division, absolute_import

from six import iteritems

from ._types import ProductType


def variant(cls):
    variants = {name: getattr(cls, name)
                for name in cls.__dict__
                if isinstance(getattr(cls, name), ProductType)}

    variants_types = {k: v._make_variant_class(cls, k)
                      for k, v in iteritems(variants)}

    for name, typ in iteritems(variants_types):
        setattr(cls, name, typ)
    return cls


__all__ = []
