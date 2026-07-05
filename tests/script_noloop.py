# NOTE: Test fixture for script_test.py.

from testlib import *
import qprompt
from script_loop import *

if __name__ == '__main__':
    menu.main(default="b", loop=False)
