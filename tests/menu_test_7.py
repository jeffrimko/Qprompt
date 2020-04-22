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

    def setUp(self):
        items = ["foo", "bar", "baz", "qux", "quux"]
        self.menu = enum_menu(items, default=1)

    def test_menu_1(self):
        setinput("\n")
        result = self.menu.show()
        self.assertEqual("1", result)

    def test_menu_2(self):
        setinput("2\n")
        result = self.menu.show()
        self.assertEqual("2", result)

    def test_menu_3(self):
        setinput("\n")
        result = self.menu.show(default=3)
        self.assertEqual("3", result)

    def test_menu_4(self):
        setinput("\n")
        result = self.menu.show()
        self.assertEqual("1", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
