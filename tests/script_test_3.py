"""Test that arguments passed to a script Menu.main(loop=True) execute
properly and args passed into the script are handled properly."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

SCRIPT = "script_3.py"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def _cleanup(test):
        rmfile("foo")
        rmfile("bar")
        rmfile("caz")
        rmfile("args")

    def setUp(test):
        test._cleanup()
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))
        test.assertFalse(op.exists("args"))

    def tearDown(test):
        test._cleanup()

    def test_script_1(test):
        args = ""
        result = os.system("python %s %s" % (SCRIPT, args))
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))
        test.assertTrue(op.exists("args"))
        with open("args") as fi:
            test.assertEqual(fi.read(), args)

    def test_script_2(test):
        args = "f c"
        result = os.system("python %s %s" % (SCRIPT, args))
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertTrue(op.exists("caz"))
        test.assertTrue(op.exists("args"))
        with open("args") as fi:
            test.assertEqual(fi.read(), args)

    def test_script_3(test):
        args = "-d"
        result = os.system("python %s %s" % (SCRIPT, args))
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))
        test.assertTrue(op.exists("args"))
        with open("args") as fi:
            test.assertEqual(fi.read(), args)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
