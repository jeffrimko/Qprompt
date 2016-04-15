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

    def test_menu_1(test):
        """Check for basic menu functionality."""
        menu = Menu()
        menu.add("1", "foo")
        menu.add("2", "bar")

        setinput("1")
        result = menu.show()
        test.assertEqual("1", result)

        setinput("1")
        result = menu.show(ret_desc=True)
        test.assertEqual("foo", result)

        setinput("2")
        result = menu.show(ret_desc=True)
        test.assertEqual("bar", result)

    def test_menu_2(test):
        """Check for regression of fix from `0.4.1`."""
        m1 = Menu()
        m1.add("1", "foo")
        m1.add("2", "bar")
        test.assertEqual(len(m1.entries), 2)

        m2 = Menu()
        m2.add("a", "AAA")
        m2.add("b", "BBB")
        m2.add("c", "CCC")
        test.assertEqual(len(m2.entries), 3)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
