from __future__ import print_function, division, absolute_import

from ._variant import variant
from ._tuple import Tuple, Empty
from ._types import _This


This = _This()


__all__ = ["variant", "Tuple", "This", "Empty"]
