"""Tests the menu features."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import enum_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_menu_1(test):
        """Check for main() call from console functionality."""

        test.assertFalse(op.exists("generated_file.txt"))
        subprocess.call("menu_helper_1.py g q", shell=True)
        test.assertTrue(op.exists("generated_file.txt"))
        subprocess.call("menu_helper_1.py d q", shell=True)
        test.assertFalse(op.exists("generated_file.txt"))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
