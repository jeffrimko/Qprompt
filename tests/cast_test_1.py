"""Tests cast() function."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import cast

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_cast_1(self):
        result = cast(123, str)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "123")

        result = cast(1.23, float)
        self.assertEqual(type(result), float)
        self.assertEqual(result, 1.23)

        result = cast("123", int)
        self.assertEqual(type(result), int)
        self.assertEqual(result, 123)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
