"""Tests the basic user input ask_X() functions."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import ask_int, ask_yesno, ask_float, ask_str

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class AskIntTest(unittest.TestCase):
    """Tests the ask_int() function."""

    def test_valid_input_returned_as_int(self):
        self.assertEqual(2, ask_with_input("2", ask_int))

    def test_invalid_input_reprompts_until_valid(self):
        self.assertEqual(3, ask_with_input("2f\n3", ask_int))

    def test_empty_input_returns_default(self):
        self.assertEqual(4, ask_with_input("\n", ask_int, dft=4))

    def test_empty_input_without_default_reprompts(self):
        self.assertEqual(3, ask_with_input("\n3", ask_int))

    def test_input_not_in_valid_list_reprompts(self):
        self.assertEqual(3, ask_with_input("2\n3", ask_int, vld=3))

    def test_input_rejected_by_valid_function_reprompts(self):
        self.assertEqual(3, ask_with_input("2\n3", ask_int, vld=lambda x: 3 == x))

class AskYesNoTest(unittest.TestCase):
    """Tests the ask_yesno() function."""

    def test_yes_answers_return_true(self):
        for answer in ["yes", "y", "YES", "Y"]:
            self.assertTrue(ask_with_input(answer, ask_yesno), answer)

    def test_no_answers_return_false(self):
        for answer in ["no", "n", "NO", "N"]:
            self.assertFalse(ask_with_input(answer, ask_yesno), answer)

class AskFloatTest(unittest.TestCase):
    """Tests the ask_float() function."""

    def test_float_input_returned_as_float(self):
        self.assertEqual(1.234, ask_with_input("1.234", ask_float))

    def test_int_input_returned_as_float(self):
        self.assertEqual(3.0, ask_with_input("3", ask_float))

class AskStrTest(unittest.TestCase):
    """Tests the ask_str() function."""

    def test_input_returned_as_str(self):
        self.assertEqual("hello", ask_with_input("hello", ask_str))
        self.assertEqual("world", ask_with_input("world", ask_str))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
