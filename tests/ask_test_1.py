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

    def test_int_1(test):
        setinput("2")
        result = ask_int()
        test.assertEqual(2, result)

        setinput("2f\n3")
        result = ask_int()
        test.assertEqual(3, result)

        setinput("\n")
        result = ask_int(dft=4)
        test.assertEqual(4, result)

        setinput("\n3")
        result = ask_int()
        test.assertEqual(3, result)

        setinput("2\n3")
        result = ask_int(vld=3)
        test.assertEqual(3, result)

        setinput("2\n3")
        result = ask_int(vld=lambda x: 3 == x)
        test.assertEqual(3, result)

    def test_yesno_1(test):
        setinput("yes")
        result = ask_yesno()
        test.assertTrue(result)

        setinput("y")
        result = ask_yesno()
        test.assertTrue(result)

        setinput("YES")
        result = ask_yesno()
        test.assertTrue(result)

        setinput("Y")
        result = ask_yesno()
        test.assertTrue(result)

        setinput("n")
        result = ask_yesno()
        test.assertFalse(result)

        setinput("no")
        result = ask_yesno()
        test.assertFalse(result)

        setinput("N")
        result = ask_yesno()
        test.assertFalse(result)

        setinput("NO")
        result = ask_yesno()
        test.assertFalse(result)

    def test_float_1(test):
        setinput("1.234")
        result = ask_float()
        test.assertEqual(1.234, result)

        setinput("3")
        result = ask_float()
        test.assertEqual(3.0, result)

    def test_str_1(test):
        setinput("hello")
        result = ask_str()
        test.assertEqual("hello", result)

        setinput("world")
        result = ask_str()
        test.assertEqual("world", result)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
