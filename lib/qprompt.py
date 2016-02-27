"""This library provides a quick method of creating command line prompts for
user input."""

##==============================================================#
## DEVELOPED 2015, REVISED 2015, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from __future__ import print_function

import sys
import ctypes
from getpass import getpass
from collections import namedtuple
from functools import partial

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.3.0"

#: A menu entry that can call a function when selected.
MenuEntry = namedtuple("MenuEntry", "name desc func args krgs")

#: Prompt start character sequence.
QSTR = "[?] "

#: User input start character sequence.
ISTR = ": "

#: User input function.
_input = input if sys.version_info >= (3, 0) else raw_input

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

def show_menu(entries, header="** MENU **", msg="Enter menu selection", compact=False, ret_desc=False):
    """Showns a menu with the given list of MenuEntry items."""
    def show_banner():
        print(header)
        for i in entries:
            print("  (%s) %s" % (i.name, i.desc))
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
    if ret_desc:
        return entry.desc
    return choice

def enum_menu(strs, **kwargs):
    """Enumerates the given list of strings into a menu."""
    entries = []
    for i,s in enumerate(strs, 1):
        entries.append(MenuEntry(str(i), str(s), None, None, None))
    return show_menu(entries, **kwargs)

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

    **Params:**
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
        get_input = _input if shw else getpass
        ans = get_input(msg)
        if "?" == ans:
            if vld:
                print(vld)
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
    """Prompts the user for an integer."""
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=int))

def ask_float(msg="Enter a float", dft=None, vld=[float]):
    """Prompts the user for a float."""
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=float))

def ask_str(msg="Enter a string", dft=None, vld=[str], shw=True, blk=True):
    """Prompts the user for a string."""
    return ask(msg, dft=dft, vld=vld, shw=shw, blk=blk)

def pause():
    """Pauses until user continues."""
    getpass("Press ENTER to continue...")

def status(*args, **kwargs):
    """Prints a status message at the start and finish of an associated
    function. Can be used as a function decorator or as a function that accepts
    another function as the first parameter.

    **Params:**
      - func (func) - Function to call. First `args` if using `status()` as a
        function. Automatically provided if using `status()` as a decorator.
      - msg (str) [args] - Message to print at start of `func`.
      - args (list) - Remainder of `args` are passed to `func`.
      - fin (str) [kwargs] - Message to print when `func` finishes.
      - kwargs (dict) - Remainder of `kwargs` are passed to `func`.
    """
    def decor(func):
        def wrapper(*fargs, **fkwargs):
            print("[!] " + msg, end=" ")
            result = func(*fargs, **fkwargs)
            print(fin)
            return result
        return wrapper
    fin = kwargs.pop('fin', "DONE.")
    args = list(args)
    if callable(args[0]):
        func = args.pop(0)
        msg = args.pop(0)
        return decor(func)(*args, **kwargs)
    msg = args.pop(0)
    return decor

def alert(msg, **kwargs):
    """Prints alert message to console."""
    print("[!] " + msg, **kwargs)

def error(msg, **kwargs):
    """Prints error message to console."""
    print("[ERROR] " + msg, **kwargs)

def warn(msg, **kwargs):
    """Prints warning message to console."""
    print("[WARNING] " + msg, **kwargs)

def title(msg):
    """Sets the title of the console window."""
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleA(msg)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
