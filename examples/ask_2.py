import os
import qprompt
path = qprompt.ask_str("Enter path to file", vld=lambda x: os.path.isfile(x))
size = qprompt.ask_int("Enter number less than 10", vld=lambda x: x < 10)
