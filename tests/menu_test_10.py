"""Tests Menu.get() method."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu, MenuEntry

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

ENTRIES = [
        MenuEntry("1", "foo", None, [], {}),
        MenuEntry("2", "bar", None, [], {}),
        MenuEntry("3", "baz", None, [], {}),
    ]

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(self):
        self.menu = Menu(*ENTRIES)

    def test_menu_1(self):
        self.assertEqual(ENTRIES[0], self.menu.get("1"))
        self.assertEqual(ENTRIES[1], self.menu.get("2"))
        self.assertEqual(ENTRIES[2], self.menu.get("3"))
        self.assertEqual(None, self.menu.get("4"))
        self.assertEqual(None, self.menu.get(""))
        self.assertEqual(None, self.menu.get(None))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
