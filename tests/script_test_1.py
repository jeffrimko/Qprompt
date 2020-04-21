"""Test that arguments passed to a script main menu execute properly."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from auxly import shell, filesys

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

SCRIPT = "script_1.py"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def _cleanup(test):
        filesys.File("foo").delete()
        filesys.File("bar").delete()
        filesys.File("caz").delete()

    def setUp(test):
        test._cleanup()
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def tearDown(test):
        test._cleanup()

    def test_script_1(test):
        result = shell.call(f"python {SCRIPT} x")
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_2(test):
        result = shell.call(f"python {SCRIPT} f")
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_3(test):
        result = shell.call(f"python {SCRIPT} b")
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_4(test):
        result = shell.call(f"python {SCRIPT} f b")
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_5(test):
        result = shell.call(f"python {SCRIPT} c")
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertTrue(op.exists("caz"))

    def test_script_6(test):
        result = shell.call(f"python {SCRIPT} c f")
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertTrue(op.exists("caz"))

    def test_script_7(test):
        result = shell.call(f"python {SCRIPT} -d")
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
