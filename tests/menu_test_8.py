"""Tests menu 'result' option return."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(self):
        menu = Menu(returns="func")
        menu.add("a", "Add", lambda x,y: x+y, [1,2])
        menu.add("s", "Sub", lambda x,y: x-y, [1,2])
        self.menu = menu

    def test_menu_1(self):
        setinput("a")
        result = self.menu.show()
        self.assertEqual(3, result)

    def test_menu_2(self):
        setinput("s")
        result = self.menu.show()
        self.assertEqual(-1, result)

    def test_menu_3(self):
        setinput("s")
        result = self.menu.show(returns="name")
        self.assertEqual("s", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
