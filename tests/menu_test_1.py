"""Check for basic menu functionality."""

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
        test.menu = Menu()
        test.menu.add("1", "foo")
        test.menu.add("2", "bar")

    def test_menu_1(test):
        setinput("1")
        result = test.menu.show()
        test.assertEqual("1", result)

    def test_menu_2(test):
        setinput("1")
        result = test.menu.show(returns="desc")
        test.assertEqual("foo", result)

    def test_menu_3(test):
        setinput("2")
        result = test.menu.show(returns="desc")
        test.assertEqual("bar", result)

    def test_menu_4(test):
        """Check for regression of fix from `0.4.1`."""
        m1 = Menu()
        m1.add("1", "foo")
        m1.add("2", "bar")

        m2 = Menu()
        m2.add("a", "AAA")
        m2.add("b", "BBB")
        m2.add("c", "CCC")

        test.assertEqual(len(m1.entries), 2)
        test.assertEqual(len(m2.entries), 3)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
