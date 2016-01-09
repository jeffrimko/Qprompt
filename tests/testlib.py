import StringIO
import sys
import unittest

sys.stdin = StringIO.StringIO()
setinput = lambda x: [sys.stdin.truncate(0), sys.stdin.write(x), sys.stdin.seek(0)]
