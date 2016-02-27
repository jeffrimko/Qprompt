from qprompt import Menu
def foo():
    print("foo")
def bar():
    print("bar")
menu = Menu()
menu.add("f", "foo", foo)
menu.add("b", "bar", bar)
menu.add("q", "quit")
while "q" != menu.show():
    pass
