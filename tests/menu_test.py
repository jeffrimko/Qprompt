"""Tests menu functionality."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import Menu, MenuEntry, enum_menu, show_menu

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Items used to populate enumerated menus.
ITEMS = ["foo", "bar", "baz", "qux", "quux"]

#: Tracks side effects of menu entry functions; see MenuFunctionEntriesTest.
TOTAL = 0

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class MenuShowTest(unittest.TestCase):
    """Tests basic Menu.show() selection behavior."""

    def setUp(self):
        self.menu = Menu()
        self.menu.add("1", "foo")
        self.menu.add("2", "bar")

    def test_show_returns_selected_entry_name(self):
        self.assertEqual("1", show_with_input("1", self.menu))

    def test_show_returns_desc_when_requested(self):
        self.assertEqual("foo", show_with_input("1", self.menu, returns="desc"))
        self.assertEqual("bar", show_with_input("2", self.menu, returns="desc"))

    def test_separate_menus_do_not_share_entries(self):
        """Check for regression of fix from `0.4.1`."""
        m1 = Menu()
        m1.add("1", "foo")
        m1.add("2", "bar")

        m2 = Menu()
        m2.add("a", "AAA")
        m2.add("b", "BBB")
        m2.add("c", "CCC")

        self.assertEqual(2, len(m1.entries))
        self.assertEqual(3, len(m2.entries))

class MenuEnumTest(unittest.TestCase):
    """Tests Menu.enum() and the enum_menu() convenience function."""

    def setUp(self):
        self.menu = Menu()
        self.menu.enum("foo")
        self.menu.enum("bar")

    def test_enum_numbers_entries_starting_at_one(self):
        self.assertEqual("1", show_with_input("1", self.menu))
        self.assertEqual("foo", show_with_input("1", self.menu, returns="desc"))
        self.assertEqual("bar", show_with_input("2", self.menu, returns="desc"))

    def test_invalid_entry_reprompts_until_valid(self):
        self.assertEqual("bar", show_with_input("3\n2", self.menu, returns="desc"))

    def test_enum_menu_numbers_items_in_order(self):
        items = ["foo", "bar"]
        for idx, item in enumerate(items):
            result = show_with_input(str(idx + 1), enum_menu(items), returns="desc")
            self.assertEqual(item, result)

    def test_enum_menu_numbers_after_existing_entries(self):
        menu = Menu()
        menu.add("s", "skip")
        menu = enum_menu(["foo", "bar"], menu=menu)
        setinput("1")
        with self.assertRaises(EOFError):
            menu.show()
        self.assertEqual("skip", show_with_input("s", menu, returns="desc"))
        self.assertEqual("foo", show_with_input("2", menu, returns="desc"))
        self.assertEqual("bar", show_with_input("3", menu, returns="desc"))

class ShowMenuFunctionTest(unittest.TestCase):
    """Tests the show_menu() convenience function."""

    def setUp(self):
        self.entries = [
                MenuEntry("1", "foo", None, None, None),
                MenuEntry("2", "bar", None, None, None)]

    def test_returns_selected_entry_name(self):
        setinput("1")
        self.assertEqual("1", show_menu(self.entries))

    def test_returns_desc_when_requested(self):
        setinput("1")
        self.assertEqual("foo", show_menu(self.entries, returns="desc"))

class MenuLimitTest(unittest.TestCase):
    """Tests menu pagination via the show() limit option."""

    def setUp(self):
        self.menu = enum_menu(ITEMS)

    def test_entry_beyond_limit_not_selectable(self):
        setinput("4")
        with self.assertRaises(EOFError):
            self.menu.show(limit=3, returns="desc")

    def test_next_page_shows_later_entries(self):
        result = show_with_input("n\n4\n", self.menu, limit=3, returns="desc")
        self.assertEqual("qux", result)

    def test_previous_page_returns_to_earlier_entries(self):
        result = show_with_input("n\np\n1", self.menu, limit=3, returns="desc")
        self.assertEqual("foo", result)

class MenuDefaultTest(unittest.TestCase):
    """Tests the default entry options of Menu.show()."""

    def setUp(self):
        self.menu = enum_menu(ITEMS)

    def test_empty_input_returns_default_given_as_str(self):
        self.assertEqual("1", show_with_input("\n", self.menu, dft="1"))

    def test_empty_input_returns_default_given_as_int(self):
        self.assertEqual("1", show_with_input("\n", self.menu, dft=1))

    def test_explicit_input_overrides_default(self):
        self.assertEqual("2", show_with_input("2\n", self.menu, dft=1))

    def test_invalid_input_not_replaced_by_default(self):
        setinput("10\n")
        with self.assertRaises(EOFError):
            self.menu.show(dft=1)

    def test_empty_input_without_default_reprompts(self):
        setinput("\n")
        with self.assertRaises(EOFError):
            self.menu.show()

    def test_explicit_input_works_without_default(self):
        self.assertEqual("2", show_with_input("2\n", self.menu))

    def test_default_keyword_alias_accepted(self):
        self.assertEqual("3", show_with_input("\n", self.menu, default=3))

class MenuInitialDefaultTest(unittest.TestCase):
    """Tests a default entry set at menu creation."""

    def setUp(self):
        self.menu = enum_menu(ITEMS, default=1)

    def test_empty_input_returns_initial_default(self):
        self.assertEqual("1", show_with_input("\n", self.menu))

    def test_explicit_input_overrides_initial_default(self):
        self.assertEqual("2", show_with_input("2\n", self.menu))

    def test_show_default_overrides_initial_default_once(self):
        self.assertEqual("3", show_with_input("\n", self.menu, default=3))
        self.assertEqual("1", show_with_input("\n", self.menu))

class MenuReturnsFuncTest(unittest.TestCase):
    """Tests menus that return the result of the selected entry's function."""

    def setUp(self):
        self.menu = Menu(returns="func")
        self.menu.add("a", "Add", lambda x, y: x + y, [1, 2])
        self.menu.add("s", "Sub", lambda x, y: x - y, [1, 2])

    def test_selection_returns_function_result(self):
        self.assertEqual(3, show_with_input("a", self.menu))
        self.assertEqual(-1, show_with_input("s", self.menu))

    def test_show_returns_option_overrides_menu_option(self):
        self.assertEqual("s", show_with_input("s", self.menu, returns="name"))

class MenuFunctionEntriesTest(unittest.TestCase):
    """Tests menus built directly from functions; selection calls the function."""

    def setUp(self):
        global TOTAL
        TOTAL = 0
        self.menu = Menu(inc, dec)

    def test_selection_calls_entry_function(self):
        show_with_input("i", self.menu)
        self.assertEqual(1, TOTAL)
        show_with_input("d", self.menu)
        self.assertEqual(0, TOTAL)

    def test_main_loop_runs_selections_until_eof(self):
        setinput("i\ni\nd\ni\n")
        self.menu.main(loop=True)
        self.assertEqual(2, TOTAL)

class MenuGetTest(unittest.TestCase):
    """Tests the Menu.get() entry lookup method."""

    def setUp(self):
        self.entries = [
                MenuEntry("1", "foo", None, [], {}),
                MenuEntry("2", "bar", None, [], {}),
                MenuEntry("3", "baz", None, [], {})]
        self.menu = Menu(*self.entries)

    def test_get_returns_entry_matching_name(self):
        for entry in self.entries:
            self.assertEqual(entry, self.menu.get(entry.name))

    def test_get_returns_none_for_unknown_name(self):
        self.assertEqual(None, self.menu.get("4"))
        self.assertEqual(None, self.menu.get(""))
        self.assertEqual(None, self.menu.get(None))

class MenuConsoleMainTest(unittest.TestCase):
    """Tests Menu.main() run from the console with entry names as arguments."""

    def test_args_run_matching_entries(self):
        self.assertFalse(op.exists("generated_file.txt"))
        subprocess.call("python ./menu_helper.py g q", shell=True)
        self.assertTrue(op.exists("generated_file.txt"))
        subprocess.call("python ./menu_helper.py d q", shell=True)
        self.assertFalse(op.exists("generated_file.txt"))

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def inc():
    global TOTAL
    TOTAL += 1

def dec():
    global TOTAL
    TOTAL -= 1

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
