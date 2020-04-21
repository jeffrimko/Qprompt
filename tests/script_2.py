from testlib import *
import qprompt

def _do_thing(name):
    with open(name, "w") as fo:
        fo.write(name)
    print(name)

def foo():
    _do_thing("foo")

def bar():
    _do_thing("bar")

def caz():
    _do_thing("caz")

menu = qprompt.Menu(foo, bar, caz)
menu.main(default="b", loop=False)
