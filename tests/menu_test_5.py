"""Check for main() call from console functionality."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from qprompt import enum_menu

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_menu_1(self):
        self.assertFalse(op.exists("generated_file.txt"))
        subprocess.call("python ./menu_helper_1.py g q", shell=True)
        self.assertTrue(op.exists("generated_file.txt"))
        subprocess.call("python ./menu_helper_1.py d q", shell=True)
        self.assertFalse(op.exists("generated_file.txt"))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
