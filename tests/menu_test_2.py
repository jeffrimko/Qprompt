"""Tests the menu features."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu, enum_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_menu_1(test):
        """Check for menu enum() functionality."""
        menu = Menu()
        menu.enum("foo")
        menu.enum("bar")

        setinput("1")
        result = menu.show()
        test.assertEqual("1", result)

        setinput("0")
        result = menu.show(returns="desc")
        test.assertEqual("foo", result)

        setinput("1")
        result = menu.show(returns="desc")
        test.assertEqual("bar", result)

        setinput("2\n1")
        result = menu.show(returns="desc")
        test.assertEqual("bar", result)

    def test_menu_2(test):
        """Check for enum_menu() functionality."""
        items = ["foo", "bar"]
        for idx in range(len(items)):
            setinput(str(idx))
            result = enum_menu(items)
            test.assertEqual(items[idx], items[int(result)])

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
