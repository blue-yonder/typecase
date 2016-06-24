from __future__ import print_function, division, absolute_import

from typecase import variant, Record, Empty, Tuple, This
import pytest


def test_use_record_in_variant():
    @variant
    class Maybe(object):
        Nothing = Empty()
        Just = Record(element=object)

    just_4 = Maybe.Just(element=4)

    assert just_4.element == 4

    assert repr(just_4) == "Maybe.Just(element=4)"
    assert isinstance(just_4, Maybe)


def test_use_record_in_variant_dict_style_access():
    @variant
    class Maybe(object):
        Nothing = Empty()
        Just = Record(element=object)

    just_4 = Maybe.Just(element=4)

    assert just_4["element"] == 4

    assert repr(just_4) == "Maybe.Just(element=4)"
    assert isinstance(just_4, Maybe)


def test_record_does_not_support_assignment():
    @variant
    class Maybe(object):
        Nothing = Empty()
        Just = Record(element=object)

    just_4 = Maybe.Just(element=4)

    with pytest.raises(TypeError) as excinfo:
        just_4["element"] = 10
    assert "TypeError: 'Just' object does not support item assignment" in str(excinfo)


def test_record_does_not_support_assignments_by_attribute():
    @variant
    class Maybe(object):
        Nothing = Empty()
        Just = Record(element=object)

    just_4 = Maybe.Just(element=4)

    with pytest.raises(TypeError) as excinfo:
        just_4.element = 10
    assert "TypeError: 'Record' object does not support item assignment" in str(excinfo)


def test_multiple_keys_work_in_record():
    @variant
    class Color(object):
        RGB = Record(r=float, g=float, b=float)
        RGBA = Record(r=float, g=float, b=float, a=float)

    r0, g0, b0, a0 = 1.0, 0.5, 0.2, 0.3

    c1 = Color.RGBA(r=r0, g=g0, b=b0, a=a0)
    assert (c1.r, c1.g, c1.b, c1.a) == (r0, g0, b0, a0)

    c2 = Color.RGB(r=r0, g=g0, b=b0)
    assert (c2.r, c2.g, c2.b) == (r0, g0, b0)

    assert c1 != c2
    assert c1 == c1
    assert c2 == c2


@variant
class Expr(object):
    Plus = Record(rhs=This, lhs=This)
    Literal = Tuple(int)


def test_records_can_refer_to_variants_using_this():
    op = Expr.Plus(rhs=Expr.Literal(1),
                   lhs=Expr.Literal(2))

    assert op.rhs[0] == 1
    assert op.lhs[0] == 2
