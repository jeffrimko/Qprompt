##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import subprocess
import sys

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

_input = input if sys.version_info >= (3, 0) else raw_input

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def run_tests():
    """Runs all found test scripts. Returns True if all tests pass."""
    fail = []
    okay = []
    for i in os.listdir("."):
        if i.find("_test_") > -1 and i.endswith(".py"):
            if 0 != subprocess.call("python " + i, shell=True):
                fail.append(i)
            else:
                okay.append(i)
    if fail:
        print("[ERROR] The following %u tests failed: %r" % (len(fail), fail))
        return False
    print("[DONE] All %u tests completely successfully!" % (len(okay)))
    return True

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pause = True
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    if len(sys.argv) > 1 and "nopause" == sys.argv[1]:
        pause = False
    okay = run_tests()
    if pause:
        _input("Press ENTER to continue...")
    sys.exit(0 if okay else 1)
