##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *
import qprompt

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

GENFILE = "generated_file.txt"

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def gen_file():
    with open(GENFILE, "w") as fo:
        fo.write("just a test")

def del_file():
    os.remove(GENFILE)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    menu = qprompt.Menu()
    menu.add("g", "Generate file", gen_file)
    menu.add("d", "Delete file", del_file)
    menu.main(loop=True)
