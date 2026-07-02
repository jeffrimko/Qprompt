"""Provides a library to aid testing."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import os.path as op
import sys
import subprocess
import unittest

# Allows development version of library to be used instead of installed.
libdir = op.normpath(op.join(op.abspath(op.dirname(__file__)), r"../src"))
sys.path.insert(0, libdir)

# Handle Python 2/3 differences.
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#{-- Allows stdin to be set via function setinput(). --
sys.stdin = StringIO()
setinput = lambda x: [
        sys.stdin.seek(0),
        sys.stdin.truncate(0),
        sys.stdin.write(x),
        sys.stdin.seek(0)]
#----}

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def show_with_input(keys, menu, **kwargs):
    """Set stdin to the given keys then show the menu; return the result."""
    setinput(keys)
    return menu.show(**kwargs)

def ask_with_input(keys, askfunc, **kwargs):
    """Set stdin to the given keys then call the ask function; return the result."""
    setinput(keys)
    return askfunc(**kwargs)

def rmfile(fname):
    """Delete a file if it exists."""
    if op.isfile(fname):
        os.remove(fname)
