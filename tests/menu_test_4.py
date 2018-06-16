"""Check for menu limit functionality."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import enum_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(test):
        test.items = ["foo", "bar", "baz", "qux", "quux"]

    def test_menu_1(test):
        setinput("4")
        with test.assertRaises(EOFError):
            enum_menu(test.items).show(limit=3, returns="desc")

    def test_menu_2(test):
        setinput("n\n4\n")
        result = enum_menu(test.items).show(limit=3, returns="desc")
        test.assertEqual("qux", result)

    def test_menu_3(test):
        setinput("n\np\n1")
        result = enum_menu(test.items).show(limit=3, returns="desc")
        test.assertEqual("foo", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
