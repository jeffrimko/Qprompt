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

    def test_int_1(self):
        setinput("2")
        result = ask_int()
        self.assertEqual(2, result)

        setinput("2f\n3")
        result = ask_int()
        self.assertEqual(3, result)

        setinput("\n3")
        result = ask_int()
        self.assertEqual(3, result)

    def test_yesno_1(self):
        setinput("yes")
        result = ask_yesno()
        self.assertTrue(result)

        setinput("y")
        result = ask_yesno()
        self.assertTrue(result)

        setinput("YES")
        result = ask_yesno()
        self.assertTrue(result)

        setinput("Y")
        result = ask_yesno()
        self.assertTrue(result)

        setinput("n")
        result = ask_yesno()
        self.assertFalse(result)

        setinput("no")
        result = ask_yesno()
        self.assertFalse(result)

        setinput("N")
        result = ask_yesno()
        self.assertFalse(result)

        setinput("NO")
        result = ask_yesno()
        self.assertFalse(result)

    def test_float_1(self):
        setinput("1.234")
        result = ask_float()
        self.assertEqual(1.234, result)

        setinput("3")
        result = ask_float()
        self.assertEqual(3.0, result)

    def test_str_1(self):
        setinput("hello")
        result = ask_str()
        self.assertEqual("hello", result)

        setinput("world")
        result = ask_str()
        self.assertEqual("world", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
