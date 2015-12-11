##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import qprompt
from verace import VerChecker, VerInfo

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

VERCHK = VerChecker("Verace", __file__)
VERCHK.include(r"lib\setup.py", opts={'match':"version = ", 'delim':'"'})
VERCHK.include(r"lib\qprompt.py", match="__version__ = ", delim='"')
VERCHK.include(r"CHANGELOG.adoc", match="qprompt-", delim="-", delim2=" ", updatable=False)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    VERCHK.run()
    if qprompt.ask_yesno("Update version?", dft="n"):
        newver = qprompt.ask_str("New version string")
        if newver:
            VERCHK.update(newver)
            VERCHK.run()
            qprompt.pause()
