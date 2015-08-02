"""Example ask function usage."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import qprompt

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    name = qprompt.ask_str("Name")
    age = qprompt.ask_int("Age", vld=range(130))
    if qprompt.ask_yesno("Say hello?", dft="y"):
        print "Hi %s! You are %u years old!" % (name, age)
