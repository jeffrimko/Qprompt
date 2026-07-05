"""Tests menu functionality."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

import contextlib
from unittest import mock

import qprompt
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

    def test_int_name_is_cast_to_string(self):
        """Entry names given as ints must be stored as strings, otherwise
        they can never match user input (which is always a string)."""
        menu = Menu()
        menu.add(1, "foo")
        self.assertEqual("1", menu.entries[0].name)
        self.assertEqual("1", show_with_input("1", menu))
        self.assertEqual("foo", show_with_input("1", menu, returns="desc"))

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

    def test_next_page_works_when_entry_named_n_exists(self):
        """The pagination entry falls back to "N" when a real entry is
        named "n"."""
        menu = Menu()
        for name, desc in [("n", "north"), ("s", "south"), ("e", "east"),
                ("w", "west"), ("x", "extra")]:
            menu.add(name, desc)
        result = show_with_input("N\nw\n", menu, limit=3, returns="desc")
        self.assertEqual("west", result)

    def test_next_page_works_with_returns_func(self):
        """Check for regression: selecting the next-page entry returned None
        instead of paging when returns="func" was used."""
        menu = Menu()
        for idx, item in enumerate(ITEMS):
            menu.add(str(idx + 1), item, lambda v=item: v.upper())
        result = show_with_input("n\n4\n", menu, limit=3, returns="func")
        self.assertEqual("QUX", result)

class MenuLimitDefaultTest(unittest.TestCase):
    """Tests default entry handling with paginated menus."""

    def test_empty_input_pages_toward_offpage_default(self):
        """When the default entry is not on the current page, blank input
        advances to the next page until the default is reachable."""
        menu = enum_menu(ITEMS)
        result = show_with_input("\n\n", menu, limit=3, dft=4, returns="desc")
        self.assertEqual("qux", result)

    def test_offpage_default_not_confused_with_entry_named_n(self):
        """Check for regression: blank input selected a real entry named "n"
        instead of paging toward the off-page default."""
        menu = Menu()
        for name, desc in [("n", "north"), ("2", "two"), ("3", "three"),
                ("4", "four"), ("5", "five")]:
            menu.add(name, desc)
        result = show_with_input("\n\n", menu, limit=3, dft="5", returns="desc")
        self.assertEqual("five", result)

class MenuFzfTest(unittest.TestCase):
    """Tests fzf search ("/") behavior, including with paginated menus."""

    def setUp(self):
        self.menu = enum_menu(ITEMS)

    def show_with_fzf(self, menu, retval, **kwargs):
        """Runs menu.show() with "/" input and a mocked iterfzf that returns
        retval; returns (result, list of lines passed to fzf)."""
        seen = []
        def fake_iterfzf(iterable):
            seen.extend(iterable)
            return retval
        module = mock.MagicMock()
        module.iterfzf = fake_iterfzf
        with mock.patch.dict(sys.modules, {"iterfzf": module}):
            result = show_with_input("/", menu, **kwargs)
        return result, seen

    def test_fzf_lists_all_entries(self):
        result, seen = self.show_with_fzf(self.menu, "1\tfoo")
        self.assertEqual("1", result)
        self.assertEqual(len(ITEMS), len(seen))

    def test_fzf_with_limit_lists_all_entries(self):
        """With pagination, fzf must list every entry, not just the current
        page, and must not include the synthetic next/prev entries."""
        result, seen = self.show_with_fzf(self.menu, "1\tfoo", limit=3)
        self.assertEqual(len(ITEMS), len(seen))
        names = [line.split("\t", 1)[0] for line in seen]
        self.assertEqual(sorted(names), [str(i + 1) for i in range(len(ITEMS))])

    def test_fzf_with_limit_selects_entry_beyond_current_page(self):
        result, seen = self.show_with_fzf(self.menu, "4\tqux",
                limit=3, returns="desc")
        self.assertEqual("qux", result)

    def test_fzf_option_false_disables_search_with_limit(self):
        """Check for regression: fzf=False was ignored when limit was set,
        so "/" still triggered a search."""
        seen = []
        def fake_iterfzf(iterable):
            seen.extend(iterable)
            return "1\tfoo"
        module = mock.MagicMock()
        module.iterfzf = fake_iterfzf
        with mock.patch.dict(sys.modules, {"iterfzf": module}):
            result = show_with_input("/\n2\n", self.menu, limit=3, fzf=False)
        self.assertEqual("2", result)
        self.assertEqual([], seen)

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
        # NOTE: Menu.main() takes input from argv via stdin_auto; clear it so
        # this test is not affected by the arguments of the test runner.
        with mock.patch.object(qprompt.stdin_auto, "auto", []):
            self.menu.main(loop=True)
        self.assertEqual(2, TOTAL)

class MenuRunTest(unittest.TestCase):
    """Tests the Menu.run() method."""

    def setUp(self):
        global TOTAL
        TOTAL = 0
        self.menu = Menu(inc, dec)

    def test_run_calls_entry_function_by_name(self):
        self.menu.run("i")
        self.assertEqual(1, TOTAL)
        self.menu.run("d")
        self.assertEqual(0, TOTAL)

    def test_run_with_unknown_name_does_nothing(self):
        self.menu.run("x")
        self.assertEqual(0, TOTAL)

class GuessNameTest(unittest.TestCase):
    """Tests entry name/desc guessing for menus built from functions."""

    def test_names_and_descs_guessed_from_function_names(self):
        menu = Menu(inc, dec)
        self.assertEqual(["i", "d"], [e.name for e in menu.entries])
        self.assertEqual(["Inc", "Dec"], [e.desc for e in menu.entries])

    def test_colliding_names_get_number_postfix(self):
        def foo(): pass
        def faz(): pass
        menu = Menu(foo, faz)
        self.assertEqual(["f", "f2"], [e.name for e in menu.entries])

    def test_desc_guessed_from_underscored_name(self):
        def do_thing(): pass
        menu = Menu(do_thing)
        self.assertEqual("Do Thing", menu.entries[0].desc)

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

class MenuMainNoteTest(unittest.TestCase):
    """Tests note handling in Menu.main(). A user-supplied note previously
    raised `TypeError: got multiple values for keyword argument 'note'`."""

    LOOP_NOTE = "Menu loops until quit."
    NOLOOP_NOTE = "Menu does not loop, single entry."

    def run_main(self, menu, keys, **kwargs):
        """Runs Menu.main() with the given stdin keys; returns stdout."""
        setinput(keys)
        out = StringIO()
        # NOTE: Menu.main() takes input from argv via stdin_auto; clear it so
        # these tests are not affected by the arguments of the test runner.
        # Notes are only displayed when _AUTO is false.
        with mock.patch.object(qprompt.stdin_auto, "auto", []), \
                mock.patch.object(qprompt, "_AUTO", False), \
                contextlib.redirect_stdout(out):
            menu.main(**kwargs)
        return out.getvalue()

    def test_default_note_shown_when_looping(self):
        output = self.run_main(Menu(("1", "foo")), "q", loop=True)
        self.assertIn("[!] " + self.LOOP_NOTE, output)

    def test_default_note_shown_when_not_looping(self):
        output = self.run_main(Menu(("1", "foo")), "q", loop=False)
        self.assertIn("[!] " + self.NOLOOP_NOTE, output)

    def test_main_note_overrides_default_when_looping(self):
        output = self.run_main(Menu(("1", "foo")), "q",
                loop=True, note="My note")
        self.assertIn("[!] My note", output)
        self.assertNotIn(self.LOOP_NOTE, output)

    def test_main_note_overrides_default_when_not_looping(self):
        output = self.run_main(Menu(("1", "foo")), "q",
                loop=False, note="My note")
        self.assertIn("[!] My note", output)
        self.assertNotIn(self.NOLOOP_NOTE, output)

    def test_constructor_note_overrides_default(self):
        output = self.run_main(Menu(("1", "foo"), note="Ctor note"), "q",
                loop=True)
        self.assertIn("[!] Ctor note", output)
        self.assertNotIn(self.LOOP_NOTE, output)

    def test_main_note_overrides_constructor_note(self):
        output = self.run_main(Menu(("1", "foo"), note="Ctor note"), "q",
                loop=True, note="Main note")
        self.assertIn("[!] Main note", output)
        self.assertNotIn("Ctor note", output)

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
