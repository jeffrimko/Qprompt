##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from qprompt import MenuEntry, show_menu

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    def foo():
        print "foo"
    def bar(a="hi"):
        print "bar", a
    val = {'a':1}
    entries = []
    entries.append(MenuEntry("1", "Item A.", foo, None, None))
    entries.append(MenuEntry("2", "Item B.", bar, None, val))
    val['a'] += 1
    show_menu(entries)
