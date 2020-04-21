"""Test that arguments passed to a script main menu execute properly."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

SCRIPT = "script_1.py"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def _cleanup(test):
        rmfile("foo")
        rmfile("bar")
        rmfile("caz")

    def setUp(test):
        test._cleanup()
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def tearDown(test):
        test._cleanup()

    def test_script_1(test):
        result = os.system("python %s x" % SCRIPT)
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_2(test):
        result = os.system("python %s f" % SCRIPT)
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_3(test):
        result = os.system("python %s b" % SCRIPT)
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_4(test):
        result = os.system("python %s f b" % SCRIPT)
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

    def test_script_5(test):
        result = os.system("python %s c" % SCRIPT)
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertTrue(op.exists("caz"))

    def test_script_6(test):
        result = os.system("python %s c f" % SCRIPT)
        test.assertEqual(0, result)
        test.assertTrue(op.exists("foo"))
        test.assertFalse(op.exists("bar"))
        test.assertTrue(op.exists("caz"))

    def test_script_7(test):
        result = os.system("python %s -d" % SCRIPT)
        test.assertEqual(0, result)
        test.assertFalse(op.exists("foo"))
        test.assertTrue(op.exists("bar"))
        test.assertFalse(op.exists("caz"))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
