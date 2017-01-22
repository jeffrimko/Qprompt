"""Uploads the package to PyPI."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import auxly.shell as sh
import sys

import qprompt

sys.path.append("..")
sys.dont_write_bytecode = True

from _Check_Versions import VERCHK
from _Install_Package import generate_readme, cleanup_readme

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
    if 0 != qprompt.status("Running tests...", sh.silent, [r"..\tests\_Run_Tests.py nopause"]):
        qprompt.alert("Issue running tests!")
        sys.exit(1)
    if qprompt.ask_yesno("Upload version `%s`?" % (ver)):
        generate_readme()
        sh.call("python setup.py sdist upload")
        cleanup_readme()
    if pause:
        qprompt.pause()
    sys.exit(0)
