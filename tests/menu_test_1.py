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

    def setUp(self):
        self.menu = Menu()
        self.menu.add("1", "foo")
        self.menu.add("2", "bar")

    def test_menu_1(self):
        setinput("1")
        result = self.menu.show()
        self.assertEqual("1", result)

    def test_menu_2(self):
        setinput("1")
        result = self.menu.show(returns="desc")
        self.assertEqual("foo", result)

    def test_menu_3(self):
        setinput("2")
        result = self.menu.show(returns="desc")
        self.assertEqual("bar", result)

    def test_menu_4(self):
        """Check for regression of fix from `0.4.1`."""
        m1 = Menu()
        m1.add("1", "foo")
        m1.add("2", "bar")

        m2 = Menu()
        m2.add("a", "AAA")
        m2.add("b", "BBB")
        m2.add("c", "CCC")

        self.assertEqual(len(m1.entries), 2)
        self.assertEqual(len(m2.entries), 3)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
