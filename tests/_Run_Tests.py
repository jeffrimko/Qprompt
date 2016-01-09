import os
import subprocess
import sys

fail = 0
for i in os.listdir("."):
    if i.find("_test_") > -1 and i.endswith(".py"):
        if 0 != subprocess.call("python " + i):
            fail += 1
print "[DONE]",
if fail:
    print "Errors in unit tests!"
    sys.exit(1)
else:
    print "All tests completely successfully!"
raw_input("Press ENTER to continue...")
sys.exit(0)
