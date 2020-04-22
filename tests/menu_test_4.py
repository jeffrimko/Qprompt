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

    def setUp(self):
        self.items = ["foo", "bar", "baz", "qux", "quux"]

    def test_menu_1(self):
        setinput("4")
        with self.assertRaises(EOFError):
            enum_menu(self.items).show(limit=3, returns="desc")

    def test_menu_2(self):
        setinput("n\n4\n")
        result = enum_menu(self.items).show(limit=3, returns="desc")
        self.assertEqual("qux", result)

    def test_menu_3(self):
        setinput("n\np\n1")
        result = enum_menu(self.items).show(limit=3, returns="desc")
        self.assertEqual("foo", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
