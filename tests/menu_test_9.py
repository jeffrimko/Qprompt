"""Tests menu 'result' option return."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

TOTAL = 0

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(test):
        global TOTAL
        TOTAL = 0
        test.menu = Menu(inc, dec)

    def test_menu_1(test):
        global TOTAL
        setinput("i")
        result = test.menu.show()
        test.assertEqual(1, TOTAL)

    def test_menu_2(test):
        global TOTAL
        setinput("d")
        result = test.menu.show()
        test.assertEqual(-1, TOTAL)

    def test_menu_3(test):
        global TOTAL
        setinput("i\ni\nd\ni\n")
        result = test.menu.main(loop=True)
        test.assertEqual(2, TOTAL)

def inc():
    global TOTAL
    TOTAL += 1

def dec():
    global TOTAL
    TOTAL -= 1

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
