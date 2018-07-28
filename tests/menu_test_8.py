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

    def setUp(test):
        menu = Menu(returns="func")
        menu.add("a", "Add", lambda x,y: x+y, [1,2])
        menu.add("s", "Sub", lambda x,y: x-y, [1,2])
        test.menu = menu

    def test_menu_1(test):
        setinput("a")
        result = test.menu.show()
        test.assertEqual(3, result)

    def test_menu_2(test):
        setinput("s")
        result = test.menu.show()
        test.assertEqual(-1, result)

    def test_menu_3(test):
        setinput("s")
        result = test.menu.show(returns="name")
        test.assertEqual("s", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
