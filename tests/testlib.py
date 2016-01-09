"""Provides a library to aid testing."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import StringIO
import sys
import unittest

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#{-- Allows stdin to be set via function setinput(). --
sys.stdin = StringIO.StringIO()
setinput = lambda x: [sys.stdin.truncate(0), sys.stdin.write(x), sys.stdin.seek(0)]
#----}
