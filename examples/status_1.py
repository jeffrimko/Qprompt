import time
from qprompt import status, echo
status("Sleeping...", time.sleep, [1], fin="Awake.")
result = status("Adding...", sum, [range(10)])
echo("result = {0}".format(result))
