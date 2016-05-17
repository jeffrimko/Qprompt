import sys
from qprompt import Menu, echo

menu = Menu()
menu.add("f", "foo", lambda: echo("foo selected!"))
menu.add("b", "bar", lambda: echo("bar selected!"))
arg = None
for arg in sys.argv[1:]:
    menu.run(arg)
if None == arg:
    menu.show()
