import time
from qprompt import status
status(time.sleep, "Sleeping...", 1, fin="Awake.")
