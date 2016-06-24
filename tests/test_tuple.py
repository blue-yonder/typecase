from __future__ import print_function, division, absolute_import

from typecase import variant, Tuple

import pytest
import unittest


class TestTypeNaming(unittest.TestCase):
    def test_may_not_start_with_lowercase(self):
        with pytest.raises(NameError):
            @variant
            class Maybe(object):
                just = Tuple(object)

    def test_may_not_contain_underscore(self):
        with pytest.raises(NameError):
            @variant
            class Maybe(object):
                jus_t = Tuple(object)

    def test_camel_case_is_fine(self):
        with pytest.raises(NameError):
            @variant
            class Maybe(object):
                just = Tuple(object)
