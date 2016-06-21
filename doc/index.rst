=========================================
Typecase - Algebraic Data Types In Python
=========================================

.. toctree::

   license

Introduction
============

A common problem when modelling a problem with Python classes is, that often
object variables (attributes) separate into two or more states. So when you
define one of these properties, the others are unnecessary / don't make much
sense to keep around and vice versa.

For example, consider a recursively defined binary tree.

>>> class Tree:
...     def __init__(self, leaf_val=None, left=None, right=None):
...         if self.left is None and self.right is None and self.leaf_value is None:
...             raise ValueError("You must either pass `left` and `right`, or `leaf`, not all three")
...         self.left = None
...         self.right = None
...         self.leaf_value = val

Such code (and there is much more complicated code of this kind in the wild) is
not very easy to read and understand. An alternative would be to refactor
``Tree`` into two classes: ``Leaf`` and ``Branch``.

>>> class Leaf:
...     def __init__(self, val):
...         self.leaf_value = val
>>> class Branch:
...     def __init__(self, left, right):
...         self.left = left
...         self.right = right

While this is fine, good Python, this library offers a similar approach
borrowing the idea of `Algebraic Data Types
<http://en.wikipedia.org/wiki/Algebraic_data_type>`_ from functional and
functional-inspired programming languages such as Rust, Haskell and Ocaml.

>>> from typecase import variant, Tuple, This
>>> @variant
... class Tree(object):
...     Branch = Tuple(This, This)
...     Leaf = Tuple(object)
>>> Tree.Leaf(10)
Tree.Leaf(10,)
>>> Tree.Branch(Tree.Leaf(10), Tree.Leaf(20))
Tree.Branch(Tree.Leaf(10,), Tree.Leaf(20,))

State of the Current Implementation
===================================

As :mod:`typecase` is work in progress, its implementation is not yet
feature-complete.

* data is stored in immutable tuples
* simple type-checks using ``isinstance`` are available
* recursive type checks are avilable (using :class:`typecase.This`)

not yet implemented:

* named-tuples / structs (Rust) / records (Haskell)
* parametric types (might not be feasible, let's see)


API
===

Tuple
-----

The tuple is the only product-type available with this library at the moment. It
can be used in a variant declaration.

.. class:: typecase.Tuple

   Represents a typed tuple.


Variant
-------

Variants are typecase's sum types.

>>> from typecase import variant, Tuple, This
>>> @variant
... class Tree(object):
...     Branch = Tuple(This, This)
...     Leaf = Tuple(object)

The cases of the variant type, ``Branch`` and ``Leaf`` in this example, are
generated Python types, that inherit from the class that ``variant`` decorates.

>>> isinstance(Tree.Leaf(5), Tree)
True


.. function:: typecase.variant

   Class-decorator that converts the static declarations of a class with typed
   class attributes into a variant type.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
