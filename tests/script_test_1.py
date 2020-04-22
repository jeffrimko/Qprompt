"""Test that arguments passed to a script Menu.main(loop=True) execute
properly."""

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

    def _cleanup(self):
        rmfile("foo")
        rmfile("bar")
        rmfile("caz")

    def setUp(self):
        self._cleanup()
        self.assertFalse(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertFalse(op.exists("caz"))

    def tearDown(self):
        self._cleanup()

    def test_script_1(self):
        result = os.system("python %s x" % SCRIPT)
        self.assertEqual(0, result)
        self.assertFalse(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertFalse(op.exists("caz"))

    def test_script_2(self):
        result = os.system("python %s f" % SCRIPT)
        self.assertEqual(0, result)
        self.assertTrue(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertFalse(op.exists("caz"))

    def test_script_3(self):
        result = os.system("python %s b" % SCRIPT)
        self.assertEqual(0, result)
        self.assertFalse(op.exists("foo"))
        self.assertTrue(op.exists("bar"))
        self.assertFalse(op.exists("caz"))

    def test_script_4(self):
        result = os.system("python %s f b" % SCRIPT)
        self.assertEqual(0, result)
        self.assertTrue(op.exists("foo"))
        self.assertTrue(op.exists("bar"))
        self.assertFalse(op.exists("caz"))

    def test_script_5(self):
        result = os.system("python %s c" % SCRIPT)
        self.assertEqual(0, result)
        self.assertFalse(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertTrue(op.exists("caz"))

    def test_script_6(self):
        result = os.system("python %s c f" % SCRIPT)
        self.assertEqual(0, result)
        self.assertTrue(op.exists("foo"))
        self.assertFalse(op.exists("bar"))
        self.assertTrue(op.exists("caz"))

    def test_script_7(self):
        result = os.system("python %s -d" % SCRIPT)
        self.assertEqual(0, result)
        self.assertFalse(op.exists("foo"))
        self.assertTrue(op.exists("bar"))
        self.assertFalse(op.exists("caz"))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
