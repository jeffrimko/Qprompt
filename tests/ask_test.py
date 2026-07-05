"""Tests the basic user input ask_X() functions."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from unittest import mock

from qprompt import ask, ask_int, ask_yesno, ask_float, ask_str, ask_captcha

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

class AskTest(unittest.TestCase):
    """Tests the general ask() function."""

    def test_fmt_function_formats_input(self):
        self.assertEqual("ABC", ask_with_input("abc", ask, fmt=lambda s: s.upper()))

    def test_help_input_shows_help_and_reprompts(self):
        self.assertEqual(5, ask_with_input("?\n5", ask_int))

    def test_help_input_with_blank_allowed_and_no_valid_list(self):
        """Check for regression: entering `?` raised ValueError when blk=True
        and no vld was supplied."""
        self.assertEqual("5", ask_with_input("?\n5", ask, blk=True))

    def test_fmt_not_applied_twice_to_default(self):
        """Check for regression: the default value was formatted twice when
        accepted via blank input."""
        result = ask_with_input("\n", ask, dft="bob", fmt=lambda s: s + "!")
        self.assertEqual("bob!", result)

class AskYesNoTest(unittest.TestCase):
    """Tests the ask_yesno() function."""

    def test_empty_input_returns_default(self):
        self.assertTrue(ask_with_input("\n", ask_yesno, dft=True))
        self.assertFalse(ask_with_input("\n", ask_yesno, dft=False))
        self.assertTrue(ask_with_input("\n", ask_yesno, dft="y"))
        self.assertFalse(ask_with_input("\n", ask_yesno, dft="n"))

    def test_explicit_input_overrides_default(self):
        self.assertFalse(ask_with_input("n", ask_yesno, dft=True))

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

    def test_blank_input_accepted_by_default(self):
        self.assertEqual("", ask_with_input("\n", ask_str))

    def test_blank_input_reprompts_when_blk_false(self):
        self.assertEqual("hello", ask_with_input("\nhello", ask_str, blk=False))

class AskCaptchaTest(unittest.TestCase):
    """Tests the ask_captcha() function; the captcha is made predictable by
    patching random.choice."""

    def test_correct_captcha_accepted(self):
        with mock.patch("qprompt.random.choice", return_value="a"):
            setinput("aaaa")
            ask_captcha()

    def test_uppercase_captcha_accepted(self):
        with mock.patch("qprompt.random.choice", return_value="a"):
            setinput("AAAA")
            ask_captcha()

    def test_wrong_captcha_reprompts(self):
        with mock.patch("qprompt.random.choice", return_value="a"):
            setinput("bbbb\naaaa")
            ask_captcha()

    def test_captcha_length_option(self):
        with mock.patch("qprompt.random.choice", return_value="a"):
            setinput("aaaaaa")
            ask_captcha(length=6)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
