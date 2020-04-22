"""Checks that the README in RST format is valid."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os

import qprompt

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class ReadmeRst:
    """Context manager that temporarily creates a RST file for the README."""
    def __enter__(self):
        _generate_readme()
    def __exit__(self, type, value, traceback):
        _cleanup_readme()

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def _generate_readme():
    os.system("asciidoctor -b docbook ../README.adoc")

    os.system("pandoc -r docbook -w rst -o README.rst.tmp ../README.xml")
    os.remove("../README.xml")

    # NOTE: The following removes the reference links that are created in the
    # RST by Pandoc. These currently cause PyPI to complain that the RST is not
    # valid.
    with open("README.rst.tmp") as fi:
        with open("README.rst", "w") as fo:
            for line in fi.readlines():
                if line.startswith(".. __"):
                    continue
                fo.write(line)
    os.remove("README.rst.tmp")

def _cleanup_readme():
    os.remove("README.rst")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    with ReadmeRst():
        os.system("python setup.py check -r -s")
    qprompt.pause()
