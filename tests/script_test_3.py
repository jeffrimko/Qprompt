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

    def _cleanup(self):
        rmfile("foo")
        rmfile("bar")
        rmfile("caz")
        rmfile("args")

    def setUp(self):
        self._cleanup()
        self.assertFalse(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertFalse(op.exists("caz"))
        self.assertFalse(op.exists("args"))

    def tearDown(self):
        self._cleanup()

    def test_script_1(self):
        args = ""
        result = os.system("python %s %s" % (SCRIPT, args))
        self.assertEqual(0, result)
        self.assertFalse(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertFalse(op.exists("caz"))
        self.assertTrue(op.exists("args"))
        with open("args") as fi:
            self.assertEqual(fi.read(), args)

    def test_script_2(self):
        args = "f c"
        result = os.system("python %s %s" % (SCRIPT, args))
        self.assertEqual(0, result)
        self.assertTrue(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertTrue(op.exists("caz"))
        self.assertTrue(op.exists("args"))
        with open("args") as fi:
            self.assertEqual(fi.read(), args)

    def test_script_3(self):
        args = "-d"
        result = os.system("python %s %s" % (SCRIPT, args))
        self.assertEqual(0, result)
        self.assertFalse(op.exists("foo"))
        self.assertTrue(op.exists("bar"))
        self.assertFalse(op.exists("caz"))
        self.assertTrue(op.exists("args"))
        with open("args") as fi:
            self.assertEqual(fi.read(), args)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
