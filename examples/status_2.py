import time
from qprompt import status
@status("Something is happening...")
def do_something(a):
    time.sleep(a)
do_something(1)
