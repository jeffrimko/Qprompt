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

    def test_menu_1(self):
        """Check for menu enum() functionality."""
        menu = Menu()
        menu.enum("foo")
        menu.enum("bar")

        setinput("1")
        result = menu.show()
        self.assertEqual("1", result)

        setinput("1")
        result = menu.show(returns="desc")
        self.assertEqual("foo", result)

        setinput("2")
        result = menu.show(returns="desc")
        self.assertEqual("bar", result)

        setinput("3\n2")
        result = menu.show(returns="desc")
        self.assertEqual("bar", result)

    def test_menu_2(self):
        """Check for enum_menu() functionality."""
        items = ["foo", "bar"]
        for idx in range(len(items),1):
            setinput(str(idx))
            result = enum_menu(items).show()
            self.assertEqual(items[idx], items[int(result)])

    def test_menu_3(self):
        """Check for enum_menu() functionality."""
        menu = Menu()
        menu.add("s", "skip")
        items = ["foo", "bar"]
        menu = enum_menu(items, menu=menu)
        setinput("1")
        with self.assertRaises(EOFError):
            menu.show()
        setinput("s")
        result = menu.show(returns="desc")
        self.assertEqual("skip", result)
        setinput("2")
        result = menu.show(returns="desc")
        self.assertEqual("foo", result)
        setinput("3")
        result = menu.show(returns="desc")
        self.assertEqual("bar", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
