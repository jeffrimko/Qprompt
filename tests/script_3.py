from testlib import *
import qprompt
from script_1 import *

if __name__ == '__main__':
    menu.main(default="b", loop=True)
    args = " ".join(sys.argv[1:])
    with open("args", "w") as fo:
        fo.write(args)
