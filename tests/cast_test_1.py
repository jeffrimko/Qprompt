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

    def test_cast_1(test):
        result = cast(123, str)
        test.assertEqual(type(result), str)
        test.assertEqual(result, "123")

        result = cast(1.23, float)
        test.assertEqual(type(result), float)
        test.assertEqual(result, 1.23)

        result = cast("123", int)
        test.assertEqual(type(result), int)
        test.assertEqual(result, 123)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
