"""This library provides a quick method of creating command line prompts for
user input."""

##==============================================================#
## DEVELOPED 2015, REVISED 2015, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import sys
import ctypes
from getpass import getpass
from collections import namedtuple
from functools import partial

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.1.11"

#: A menu entry that can call a function when selected.
MenuEntry = namedtuple("MenuEntry", "name desc func args krgs")

#: Prompt start character sequence.
QSTR = "[?] "

#: User input start character sequence.
ISTR = ": "

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

def show_menu(entries, header="** MENU **", msg="Enter menu selection", compact=False):
    """Showns a menu with the given list of MenuEntry items."""
    def show_banner():
        print header
        for i in entries:
            print "  (%s) %s" % (i.name, i.desc)
    valid = [i.name for i in entries]
    if not compact:
        show_banner()
    choice = ask(msg, vld=valid)
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

def cast(val, typ=int):
    """Attempts to cast the given value to the given type otherwise None is
    returned."""
    try:
        val = typ(val)
    except:
        val = None
    return val

def ask(msg="Enter input", dft=None, vld=[], fmt=lambda x: x, shw=True, blk=False):
    """Prompts the user for input and returns the given answer. Optionally
    checks if answer is valid.

    *Params*:
      - msg (str) - Message to prompt the user with.
      - dft (int|float|str) - Default value if input is left blank.
      - vld ([int|float|str]) - Valid input entries.
      - fmt (func) - Function used to format user input.
      - shw (bool) - If true, show the user's input as typed.
      - blk (bool) - If true, accept a blank string as valid input.
    """
    msg = "%s%s" % (QSTR, msg)
    if dft != None:
        dft = fmt(dft)
        msg += " [%s]" % (dft if type(dft) is str else repr(dft))
        vld.append(dft)
    if vld:
        # Sanitize valid inputs.
        vld = sorted(list(set([fmt(v) if fmt(v) else v for v in vld ])))
    msg += ISTR
    ans = None
    while ans is None:
        get_input = raw_input if shw else getpass
        ans = get_input(msg)
        if "?" == ans:
            if vld:
                print vld
            ans = None
            continue
        if "" == ans:
            if dft != None:
                ans = dft if not fmt else fmt(dft)
                break
            if not blk:
                ans = None
                continue
        try:
            ans = ans if not fmt else fmt(ans)
        except:
            ans = None
        if vld:
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
    if dft != None:
        dft = yes[0] if (dft in yes or dft == True) else no[0]
    return ask(msg, dft=dft, vld=yes+no) in yes

def ask_int(msg="Enter an integer", dft=None, vld=[int]):
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=int))

def ask_float(msg="Enter a float", dft=None, vld=[float]):
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=float))

def ask_str(msg="Enter a string", dft=None, vld=[str], shw=True, blk=True):
    return ask(msg, dft=dft, vld=vld, shw=shw, blk=blk)

def pause():
    """Pauses until user continues."""
    getpass("Press ENTER to continue...")

def alert(msg):
    """Prints alert message to console."""
    print "[!] " + msg

def title(msg):
    """Sets the title of the console window."""
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleA(msg)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
