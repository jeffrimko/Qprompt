"""Provides a library to aid testing."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import sys
import unittest

# Handle Python 2/3 differences.
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

sys.path.append(r"..\lib")

#{-- Allows stdin to be set via function setinput(). --
sys.stdin = StringIO()
setinput = lambda x: [
        sys.stdin.seek(0),
        sys.stdin.truncate(0),
        sys.stdin.write(x),
        sys.stdin.seek(0)]
#----}
