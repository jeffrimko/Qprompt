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

    def setUp(self):
        global TOTAL
        TOTAL = 0
        self.menu = Menu(inc, dec)

    def test_menu_1(self):
        global TOTAL
        setinput("i")
        result = self.menu.show()
        self.assertEqual(1, TOTAL)

    def test_menu_2(self):
        global TOTAL
        setinput("d")
        result = self.menu.show()
        self.assertEqual(-1, TOTAL)

    def test_menu_3(self):
        global TOTAL
        setinput("i\ni\nd\ni\n")
        result = self.menu.main(loop=True)
        self.assertEqual(2, TOTAL)

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
