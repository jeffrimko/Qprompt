"""Tests menu default."""

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
        test.menu = enum_menu(items)

    def test_menu_1(test):
        setinput("\n")
        result = test.menu.show(dft="1")
        test.assertEqual("1", result)

    def test_menu_2(test):
        setinput("\n")
        result = test.menu.show(dft=1)
        test.assertEqual("1", result)

    def test_menu_3(test):
        setinput("2\n")
        result = test.menu.show(dft=1)
        test.assertEqual("2", result)

    def test_menu_4(test):
        setinput("2\n")
        result = test.menu.show(dft=1)
        test.assertEqual("2", result)

    def test_menu_5(test):
        setinput("10\n")
        with test.assertRaises(EOFError):
            result = test.menu.show(dft=1)

    def test_menu_6(test):
        setinput("\n")
        with test.assertRaises(EOFError):
            result = test.menu.show()

    def test_menu_7(test):
        setinput("2\n")
        result = test.menu.show()
        test.assertEqual("2", result)

    def test_menu_8(test):
        setinput("\n")
        result = test.menu.show(default=3)
        test.assertEqual("3", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
