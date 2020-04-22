"""Uploads the package to PyPI."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import auxly.shell as sh
import auxly.filesys as fs
import sys

import qprompt

sys.path.append("..")
sys.dont_write_bytecode = True

from _Check_Versions import VERCHK
from _Check_Readme import ReadmeRst

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pause = True
    if len(sys.argv) > 1 and "nopause" == sys.argv[1]:
        pause = False
    ver = VERCHK.run()
    if not ver:
        qprompt.alert("Issue with version info!")
        sys.exit(1)
    if 0 != qprompt.status("Running tests...", sh.silent, [r"python ..\tests\_Run_Tests.py nopause"]):
        qprompt.alert("Issue running tests!")
        sys.exit(1)
    if qprompt.ask_yesno("Upload version `%s`?" % (ver)):
        with ReadmeRst():
            fs.copy(r"..\LICENSE", "LICENSE")
            sh.call("python setup.py sdist upload")
            fs.delete("LICENSE")
    if pause:
        qprompt.pause()
    sys.exit(0)
