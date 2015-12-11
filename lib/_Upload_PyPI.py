"""Uploads the qprompt package to PyPI."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import subprocess
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
    ver = VERCHK.run()
    if not ver:
        qprompt.alert("Issue with version info!")
        exit()
    if qprompt.ask_yesno("Upload version `%s`?" % (ver)):
        generate_readme()
        subprocess.call("python setup.py sdist upload", shell=True)
        cleanup_readme()
