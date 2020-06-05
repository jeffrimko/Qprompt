"""Check for show_menu() functionality."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import MenuEntry, show_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(self):
        self.entries = [MenuEntry("1", "foo", None, None, None)]
        self.entries.append(MenuEntry("2", "bar", None, None, None))

    def test_menu_1(self):
        setinput("1")
        result = show_menu(self.entries)
        self.assertEqual("1", result)

    def test_menu_2(self):
        setinput("1")
        result = show_menu(self.entries, returns="desc")
        self.assertEqual("foo", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
