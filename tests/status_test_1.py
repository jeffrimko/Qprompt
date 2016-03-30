"""Tests the status() function."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import time
import random
from testlib import *

from qprompt import status

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Function used to return time point.
get_time = time.time

#: Delay times to check.
DELAYS = [0.1, 0.2, 0.3, 0.5]

#: Decimal places to check delay times; no need to be too accurate.
PLACES = 1

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def test_status_1(test):
        for delay in DELAYS:
            t_start = get_time()
            status("Sleeping...", time.sleep, delay, fin="Awake.")
            test.assertAlmostEqual(delay, get_time() - t_start, places=PLACES)

    def test_status_2(test):
        for delay in DELAYS:
            t_start = get_time()
            rand1 = random.randint(1, 100)
            rand2 = random.randint(1, 100)
            result = status("Doing something...", do_something, delay, rand1, rand2)
            test.assertAlmostEqual(delay, get_time() - t_start, places=PLACES)
            test.assertEqual(rand1+rand2, result)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def do_something(a, b, c):
    time.sleep(a)
    return b+c

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
