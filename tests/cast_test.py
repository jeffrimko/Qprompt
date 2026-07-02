"""Tests the cast() function."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import cast

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class CastTest(unittest.TestCase):
    """Tests casting values to a target type."""

    def _check(self, value, totype, expected):
        result = cast(value, totype)
        self.assertEqual(totype, type(result))
        self.assertEqual(expected, result)

    def test_int_cast_to_str(self):
        self._check(123, str, "123")

    def test_float_cast_to_float_unchanged(self):
        self._check(1.23, float, 1.23)

    def test_str_cast_to_int(self):
        self._check("123", int, 123)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
