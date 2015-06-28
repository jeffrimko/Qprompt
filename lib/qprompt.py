"""This library provides a quick method of creating command line prompts for
user input."""

##==============================================================#
## DEVELOPED 2015, REVISED 2015, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from collections import namedtuple
from functools import partial

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.1.0-alpha"

#: A menu entry that can call a function when selected.
MenuEntry = namedtuple("MenuEntry", "name desc func args krgs")

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class Menu:
    """Menu object that will show the associated MenuEntry items."""
    def __init__(self, entries=[]):
        self.entries = entries
    def add(self, name, desc, func=None, args=[], krgs={}):
        self.entries.append(MenuEntry(name, desc, func, args, krgs))
    def show(self, **kwargs):
        return show_menu(self.entries, **kwargs)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def show_menu(entries, header="** MENU **", footer="Enter menu selection."):
    """Showns a menu with the given list of MenuEntry items."""
    def show_banner():
        print header
        for i in entries:
            print "  (%s) %s" % (i.name, i.desc)
    valid = [i.name for i in entries]
    show_banner()
    while True:
        choice = raw_input("[?] %s : " % (footer))
        if choice in valid:
            entry = [i for i in entries if i.name == choice][0]
            if entry.func:
                if entry.args and entry.krgs:
                    entry.func(*entry.args, **entry.krgs)
                elif entry.args:
                    entry.func(*entry.args)
                elif entry.krgs:
                    entry.func(**entry.krgs)
                else:
                    entry.func()
            return choice
        elif choice == "?":
            show_banner()

def cast(val, typ=int):
    """Attempts to cast the given value to the given type otherwise None is
    returned."""
    try:
        val = typ(val)
    except:
        val = None
    return val

def ask(msg="Enter input.", dft=None, vld=[], fmt=None):
    """Prompts the user for input and returns the given answer. Optionally
    checks if answer is valid.

    *Params*:
      - msg (str) - Message to prompt the user with.
      - dft (int|float|str) - Default value if input is left blank.
      - vld ([int|float|str]) - Valid input entries.
      - fmt (func) - Function used to format user input.
    """
    msg = "[?] %s" % (msg)
    if dft:
        msg += " [%s]" % (dft if type(dft) is str else repr(dft))
        vld.append(dft)
    msg += " : "
    ans = None
    while ans is None:
        ans = raw_input(msg)
        if "?" == ans:
            if vld:
                print vld
            ans = None
            continue
        blk = "" == ans
        if blk:
            ans = dft if dft else None
        if fmt:
            ans = fmt(ans)
        if vld and not blk:
            for v in vld:
                if type(v) is type and cast(ans, v) is not None:
                    ans = cast(ans, v)
                    break
                elif ans in vld:
                    break
            else:
                ans = None
    return ans

def ask_yesno(msg="Proceed?", dft=None):
    """Prompts the user for a yes or no answer. Returns True for yes, False
    for no."""
    yes = ["y", "yes", "Y", "YES"]
    no = ["n", "no", "N", "NO"]
    dft = yes[0] if dft in yes else no[0]
    return ask(msg, dft=dft, vld=yes+no) in yes

def ask_int(msg="Enter an integer.", dft=None, vld=[int]):
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=int))

def ask_float(msg="Enter a float.", dft=None, vld=[float]):
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=float))

def ask_str(msg="Enter a string.", dft=None, vld=[str]):
    return ask(msg, dft=dft, vld=vld)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    print ask_yesno(dft="y")
    print ask_int(dft=1)
