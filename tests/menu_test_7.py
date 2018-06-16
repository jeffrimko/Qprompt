"""Tests menu initial arguments and overrides."""

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
        items = ["foo", "bar", "baz", "qux", "quux"]
        test.menu = enum_menu(items, default=1)

    def test_menu_1(test):
        setinput("\n")
        result = test.menu.show()
        test.assertEqual("1", result)

    def test_menu_2(test):
        setinput("2\n")
        result = test.menu.show()
        test.assertEqual("2", result)

    def test_menu_3(test):
        setinput("\n")
        result = test.menu.show(default=3)
        test.assertEqual("3", result)

    def test_menu_4(test):
        setinput("\n")
        result = test.menu.show()
        test.assertEqual("1", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
