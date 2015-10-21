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

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    ver = VERCHK.run()
    if ver:
        if qprompt.ask_yesno("Upload version `%s`?" % (ver)):
            subprocess.call("asciidoc -b docbook ../README.adoc", shell=True)
            subprocess.call("pandoc -r docbook -w rst -o README.rst ../README.xml", shell=True)
            os.remove("../README.xml")
            subprocess.call("python setup.py sdist upload", shell=True)
            os.remove("README.rst")
    else:
        qprompt.alert("Issue with version info!")
