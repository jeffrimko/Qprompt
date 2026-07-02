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

#: Delay times to check.
DELAYS = [0.1, 0.2, 0.3, 0.5]

#: Decimal places to check delay times; no need to be too accurate.
PLACES = 1

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class StatusTest(unittest.TestCase):
    """Tests running functions via status()."""

    def test_status_runs_function_for_expected_duration(self):
        for delay in DELAYS:
            t_start = time.time()
            status("Sleeping...", time.sleep, [delay], fin="Awake.")
            self.assertAlmostEqual(delay, time.time() - t_start, places=PLACES)

    def test_status_returns_result_of_function_with_args(self):
        for delay in DELAYS:
            t_start = time.time()
            rand1 = random.randint(1, 100)
            rand2 = random.randint(1, 100)
            result = status("Doing something...", do_something, [delay, rand1, rand2])
            self.assertAlmostEqual(delay, time.time() - t_start, places=PLACES)
            self.assertEqual(rand1 + rand2, result)

    def test_status_passes_kwargs_to_function(self):
        for delay in DELAYS:
            t_start = time.time()
            rand1 = random.randint(1, 100)
            rand2 = random.randint(1, 100)
            result = status("Doing another...", do_another, [delay, rand1], {'c': rand2})
            self.assertAlmostEqual(delay, time.time() - t_start, places=PLACES)
            self.assertEqual(rand1 + rand2, result)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def do_something(a, b, c):
    time.sleep(a)
    return b + c

def do_another(a, b=3, c=4):
    time.sleep(a)
    return b + c

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
