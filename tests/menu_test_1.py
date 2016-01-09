"""Tests the menu features."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_menu_1(self):
        menu = Menu()
        menu.add("1", "foo")
        menu.add("2", "bar")

        setinput("1")
        result = menu.show()
        self.assertEqual("1", result)

        setinput("1")
        result = menu.show(ret_desc=True)
        self.assertEqual("foo", result)

        setinput("2")
        result = menu.show(ret_desc=True)
        self.assertEqual("bar", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
