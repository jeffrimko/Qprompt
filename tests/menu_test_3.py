"""Tests the menu features."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import MenuEntry, show_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_menu_1(test):
        """Check for show_menu() functionality."""
        entries = []
        entries.append(MenuEntry("1", "foo", None, None, None))
        entries.append(MenuEntry("2", "bar", None, None, None))

        setinput("1")
        result = show_menu(entries)
        test.assertEqual("1", result)

        setinput("1")
        result = show_menu(entries, returns="desc")
        test.assertEqual("foo", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
