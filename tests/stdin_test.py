"""Tests the StdinSetup and StdinAuto stdin management helpers."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu, StdinSetup, StdinAuto, ask_str

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class StdinSetupTest(unittest.TestCase):
    """Tests the StdinSetup context manager."""

    def test_supplied_stream_used_as_stdin(self):
        with StdinSetup(stream=StringIO("hello\n")):
            self.assertEqual("hello", ask_str())

    def test_original_stdin_restored_after_context(self):
        original = sys.stdin
        with StdinSetup(stream=StringIO("hello\n")):
            self.assertNotEqual(original, sys.stdin)
            ask_str()
        self.assertEqual(original, sys.stdin)

class StdinAutoTest(unittest.TestCase):
    """Tests the StdinAuto context manager."""

    def setUp(self):
        self.menu = Menu()
        self.menu.add("a", "apple")
        self.menu.add("b", "banana")

    def test_auto_list_supplies_menu_input(self):
        with StdinAuto(auto=["a"]):
            self.assertEqual("a", self.menu.show())

    def test_auto_list_supplies_multiple_prompts(self):
        with StdinAuto(auto=["a", "b"]):
            self.assertEqual("a", self.menu.show())
            self.assertEqual("b", self.menu.show())

    def test_stdin_restored_after_context(self):
        original = sys.stdin
        with StdinAuto(auto=["a"]):
            self.menu.show()
        self.assertEqual(original, sys.stdin)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
