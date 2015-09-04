##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os.path as op
import qprompt
from verace import VerChecker, VerInfo

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class QpromptChecker(VerChecker):
    """Check versions in the Qprompt project."""
    NAME = "Qprompt"
    def check_setup(self):
        path = basepath(r"lib\setup.py")
        with open(path) as f:
            for num,line in enumerate(f.readlines(), 1):
                if line.find("version =") > -1:
                    return [VerInfo(path, num, line.split('"')[1].strip())]
    def check_main(self):
        path = basepath(r"lib\qprompt.py")
        with open(path) as f:
            for num,line in enumerate(f.readlines(), 1):
                if line.find("__version__ =") > -1:
                    return [VerInfo(path, num, line.split('"')[1].strip())]
    def check_log(self):
        path = basepath(r"CHANGELOG.md")
        with open(path) as f:
            for num,line in enumerate(f.readlines(), 1):
                if line.find("qprompt-") > -1:
                    return [VerInfo(path, num, line.split('-')[1].split(" ")[0].strip())]

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

#: Returns path as absolute from base.
basepath = lambda x: op.join(op.abspath(op.dirname(op.realpath(__file__))), x)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    QpromptChecker().show()
    qprompt.pause()
