"""Tests that arguments passed to a script using Menu.main() execute the
matching menu entries."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Files created by the script menu entries.
ENTRY_FILES = ["foo", "bar", "caz"]

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class ScriptTestBase(object):
    """Shared helpers for running a menu script and checking created files."""

    #: Script run by the test; set by subclass.
    SCRIPT = None

    #: Files to remove before/after each test.
    CLEANUP = ENTRY_FILES

    def setUp(self):
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        for fname in self.CLEANUP:
            rmfile(fname)
            self.assertFalse(op.exists(fname))

    def run_script(self, args=""):
        """Run the script with the given arguments; check it exits cleanly."""
        result = os.system("python %s %s" % (self.SCRIPT, args))
        self.assertEqual(0, result)

    def assert_created(self, *expected):
        """Check that exactly the expected entry files were created."""
        for fname in ENTRY_FILES:
            if fname in expected:
                self.assertTrue(op.exists(fname), fname + " should exist")
            else:
                self.assertFalse(op.exists(fname), fname + " should not exist")

class MenuMainLoopScriptTest(ScriptTestBase, unittest.TestCase):
    """Tests a script using Menu.main(loop=True); each argument runs its
    matching entry."""

    SCRIPT = "script_loop.py"

    def test_unknown_arg_runs_no_entries(self):
        self.run_script("x")
        self.assert_created()

    def test_single_arg_runs_matching_entry(self):
        for arg, fname in [("f", "foo"), ("b", "bar"), ("c", "caz")]:
            self._cleanup()
            self.run_script(arg)
            self.assert_created(fname)

    def test_multiple_args_run_each_entry(self):
        self.run_script("f b")
        self.assert_created("foo", "bar")
        self._cleanup()
        self.run_script("c f")
        self.assert_created("caz", "foo")

    def test_default_flag_runs_default_entry(self):
        self.run_script("-d")
        self.assert_created("bar")

class MenuMainNoLoopScriptTest(ScriptTestBase, unittest.TestCase):
    """Tests a script using Menu.main(loop=False); only the first argument
    runs its matching entry."""

    SCRIPT = "script_noloop.py"

    def test_unknown_arg_runs_no_entries(self):
        self.run_script("x")
        self.assert_created()

    def test_single_arg_runs_matching_entry(self):
        for arg, fname in [("f", "foo"), ("b", "bar"), ("c", "caz")]:
            self._cleanup()
            self.run_script(arg)
            self.assert_created(fname)

    def test_only_first_of_multiple_args_runs(self):
        self.run_script("f b")
        self.assert_created("foo")
        self._cleanup()
        self.run_script("c f")
        self.assert_created("caz")

    def test_default_flag_runs_default_entry(self):
        self.run_script("-d")
        self.assert_created("bar")

class MenuMainArgsPreservedScriptTest(ScriptTestBase, unittest.TestCase):
    """Tests that sys.argv is still available to a script after
    Menu.main(loop=True) consumes the menu arguments."""

    SCRIPT = "script_loop_args.py"
    CLEANUP = ENTRY_FILES + ["args"]

    def check_args_file(self, args):
        self.assertTrue(op.exists("args"))
        with open("args") as fi:
            self.assertEqual(args, fi.read())

    def test_no_args_runs_no_entries(self):
        self.run_script("")
        self.assert_created()
        self.check_args_file("")

    def test_args_run_entries_and_remain_in_argv(self):
        self.run_script("f c")
        self.assert_created("foo", "caz")
        self.check_args_file("f c")

    def test_default_flag_runs_default_entry(self):
        self.run_script("-d")
        self.assert_created("bar")
        self.check_args_file("-d")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
