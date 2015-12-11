##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import subprocess

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def generate_readme():
    subprocess.call("asciidoc -b docbook ../README.adoc", shell=True)
    subprocess.call("pandoc -r docbook -w rst -o README.rst ../README.xml", shell=True)
    os.remove("../README.xml")

def cleanup_readme():
    os.remove("README.rst")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    generate_readme()
    subprocess.call("python setup.py install", shell=True)
    cleanup_readme()
