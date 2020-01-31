##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import verace

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

VERCHK = verace.VerChecker("Qprompt", __file__)
VERCHK.include(r"setup.py", match="version = ", splits=[('"',1)])
VERCHK.include(r"lib\qprompt.py", match="__version__ = ", splits=[('"',1)])
VERCHK.include(r"doc\source\conf.py", match="version = ", splits=[("'",1)])
VERCHK.include(r"doc\source\conf.py", match="release = ", splits=[("'",1)])
VERCHK.include(r"doc\source\conf.py", match="html_title = ", splits=[("v",1)])
VERCHK.include(r"CHANGELOG.adoc", match="qprompt-", splits=[("-",1),(" ",0)], updatable=False)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    VERCHK.prompt()
