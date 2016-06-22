from __future__ import print_function, division, absolute_import

from typecase import variant, Tuple, Empty, This

import pytest


def test_declare_variant():

    @variant
    class Maybe(object):
        Nothing = Empty()
        Just = Tuple(object)

    a = Maybe.Nothing()
    b = Maybe.Just(4)

    assert b == b
    assert a != b

    assert b[0] == 4

    assert repr(b) == "Maybe.Just(4,)"
    assert repr(a) == "Maybe.Nothing()"

    assert isinstance(a, Maybe)
    assert isinstance(b, Maybe)


def test_tuple_cannot_be_instantiated_with_wrong_type():

    @variant
    class Maybe(object):
        Nothing = Empty
        Just = Tuple(int)

    with pytest.raises(TypeError):
        Maybe.Just("a")


def test_simple_ast():
    @variant
    class Expr(object):
        Add = Tuple(This, This)
        Int = Tuple(int)
        Flt = Tuple(float)

    with pytest.raises(TypeError):
        Expr.Add(Expr.Int(5), Expr.Flt(5))

    with pytest.raises(TypeError):
        Expr.Add(4, 3)


def test_simple_ast_where_number_of_arguments_does_not_match():
    @variant
    class Expr(object):
        Add = Tuple(This, This, This)
        Int = Tuple(int)
        Flt = Tuple(int)

    with pytest.raises(TypeError):
        Expr.Add(Expr.Int(5), Expr.Flt(5))


def test_parametric_datatypes():
    @variant
    class Tree(object):
        A = "A"
        Branch = Tuple(This, This)
        Leaf = Tuple(A)

    Branch = Tree.Branch
    Leaf = Tree.Leaf
    Branch(Branch(Leaf(1), Leaf(2)), Leaf(1))


def test_parametric_datatypes_violated():
    @variant
    class Tree(object):
        A = "A"
        Branch = Tuple(This, This)
        Leaf = Tuple(A)

    Branch = Tree.Branch
    Leaf = Tree.Leaf
    with pytest.raises(TypeError):
        Branch("54", Leaf(1))


def test_invalid_type_constraint_supplied_to_tuple():
    with pytest.raises(TypeError):
        @variant
        class Tree(object):
            Branch = Tuple(3, This)
            Leaf = Tuple(object)
