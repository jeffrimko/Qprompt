"""Example ask as command usage."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import qprompt

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    while True:
        cmd = qprompt.ask_str("command", vld=["help", "run", "quit"])
        if "help" == cmd:
            print "DO HELP"
        if "run" == cmd:
            print "DO RUN"
        if "quit" == cmd:
            exit()
