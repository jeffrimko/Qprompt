"""Tests the menu features."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import enum_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_menu_1(test):
        """Check for limit functionality."""
        items = ["foo", "bar", "baz", "qux", "quux"]

        setinput("4")
        with test.assertRaises(EOFError):
            enum_menu(items).show(limit=3, returns="desc")

        setinput("n\n4\n")
        result = enum_menu(items).show(limit=3, returns="desc")
        test.assertEqual("qux", result)

        setinput("n\np\n1")
        result = enum_menu(items).show(limit=3, returns="desc")
        test.assertEqual("foo", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
