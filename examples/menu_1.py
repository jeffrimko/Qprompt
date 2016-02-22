from qprompt import MenuEntry, show_menu, ask_yesno
def foo():
    print("foo")
def bar(a):
    print("bar %r" % (a))
val = {'a':42}
entries = []
entries.append(MenuEntry("1", "Item A.", foo, None, None))
entries.append(MenuEntry("2", "Item B.", bar, None, val))
entries.append(MenuEntry("q", "Quit", None, None, None))
compact = ask_yesno("Use compact menu?")
while "q" != show_menu(entries, compact=compact):
    pass
