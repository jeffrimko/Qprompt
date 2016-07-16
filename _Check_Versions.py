##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import qprompt
import verace

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

VERCHK = verace.VerChecker("Qprompt", __file__)
VERCHK.include(r"lib\setup.py", opts={'match':"version = ", 'delim':'"'})
VERCHK.include(r"lib\qprompt.py", match="__version__ = ", delim='"')
VERCHK.include(r"doc\source\conf.py", match="version = ", delim="'")
VERCHK.include(r"doc\source\conf.py", match="release = ", delim="'")
VERCHK.include(r"doc\source\conf.py", match="html_title = ", delim="v", delim2="''")
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
