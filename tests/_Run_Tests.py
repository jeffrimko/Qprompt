##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import subprocess
import sys

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def run_tests():
    """Runs all found test scripts. Returns True if all tests pass."""
    fail = 0
    for i in os.listdir("."):
        if i.find("_test_") > -1 and i.endswith(".py"):
            if 0 != subprocess.call("python " + i):
                fail += 1
    print "[DONE]",
    if fail:
        print "Errors in unit tests!"
        return False
    print "All tests completely successfully!"
    return True

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    okay = run_tests()
    raw_input("Press ENTER to continue...")
    sys.exit(0 if okay else 1)
