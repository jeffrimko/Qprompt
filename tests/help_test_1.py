"""Tests the basic user input ask_X() functions."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import ask_int, ask_yesno, ask_float, ask_str

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_help_1(test):
        """Checks for regression of retaining default values in the help
        dialog."""
        sys.stdout = stdout = StringIO()
        setinput("?\n\n")
        result = ask_int(dft=1)
        test.assertEqual(1, result)
        test.assertEqual(stdout.getvalue(), "[?] Enter an integer [1]: [1, <class 'int'>]\n[?] Enter an integer [1]: ")

        sys.stdout = stdout = StringIO()
        setinput("?\n\n")
        result = ask_int(dft=2)
        test.assertEqual(2, result)
        test.assertEqual(stdout.getvalue(), "[?] Enter an integer [2]: [2, <class 'int'>]\n[?] Enter an integer [2]: ")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
