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

    def setUp(self):
        items = ["foo", "bar", "baz", "qux", "quux"]
        self.menu = enum_menu(items)

    def test_menu_1(self):
        setinput("\n")
        result = self.menu.show(dft="1")
        self.assertEqual("1", result)

    def test_menu_2(self):
        setinput("\n")
        result = self.menu.show(dft=1)
        self.assertEqual("1", result)

    def test_menu_3(self):
        setinput("2\n")
        result = self.menu.show(dft=1)
        self.assertEqual("2", result)

    def test_menu_4(self):
        setinput("2\n")
        result = self.menu.show(dft=1)
        self.assertEqual("2", result)

    def test_menu_5(self):
        setinput("10\n")
        with self.assertRaises(EOFError):
            result = self.menu.show(dft=1)

    def test_menu_6(self):
        setinput("\n")
        with self.assertRaises(EOFError):
            result = self.menu.show()

    def test_menu_7(self):
        setinput("2\n")
        result = self.menu.show()
        self.assertEqual("2", result)

    def test_menu_8(self):
        setinput("\n")
        result = self.menu.show(default=3)
        self.assertEqual("3", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
