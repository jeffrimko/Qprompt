##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import qprompt
from verace import VerChecker, VerInfo

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class QpromptChecker(VerChecker):
    """Check versions in the Qprompt project."""
    NAME = "Qprompt"
    def check_setup(self):
        path = r"lib\setup.py"
        with open(path) as f:
            for num,line in enumerate(f.readlines(), 1):
                if line.find("version =") > -1:
                    return [VerInfo(path, num, line.split('"')[1].strip())]
    def check_main(self):
        path = r"lib\qprompt.py"
        with open(path) as f:
            for num,line in enumerate(f.readlines(), 1):
                if line.find("__version__ =") > -1:
                    return [VerInfo(path, num, line.split('"')[1].strip())]
    def check_log(self):
        path = r"CHANGELOG.md"
        with open(path) as f:
            for num,line in enumerate(f.readlines(), 1):
                if line.find("qprompt-") > -1:
                    return [VerInfo(path, num, line.split('-')[1].split(" ")[0].strip())]

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    QpromptChecker().show()
    qprompt.pause()
