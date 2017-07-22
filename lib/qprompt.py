"""This library provides a quick method of creating command line prompts for
user input."""

##==============================================================#
## DEVELOPED 2015, REVISED 2017, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from __future__ import print_function

import copy
import ctypes
import random
import string
import sys
from collections import namedtuple
from functools import partial
from getpass import getpass
from subprocess import call

# Handle Python 2/3 differences.
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.9.3"

#: A menu entry that can call a function when selected.
MenuEntry = namedtuple("MenuEntry", "name desc func args krgs")

#: Prompt start character sequence.
QSTR = "[?] "

#: User input start character sequence.
ISTR = ": "

#: Default horizontal rule width.
HRWIDTH = 65

#: Default horizontal rule character.
HRCHAR = "-"

#: Default top wrap character.
TCHAR = "-"

#: Default bottom wrap character.
BCHAR = "-"

#: User input function.
_input = input if sys.version_info >= (3, 0) else raw_input

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class StdinSetup:
    """Sets up stdin to be supplied via `setinput()`; a default context manager
    is provided by `stdin_setup`."""
    def __init__(self, stream=None):
        self._stream = stream or StringIO()
        self.original = sys.stdin
    def setup(self):
        sys.stdin = self._stream
    def teardown(self):
        sys.stdin = self.original
    def __enter__(self):
        self.setup()
        return self
    def __exit__(self, type, value, traceback):
        self.teardown()
stdin_setup = StdinSetup()

class StdinAuto:
    """Automatically set stdin using supplied list; a default context manager
    is provided by `stdin_auto`."""
    def __init__(self, auto=None):
        self.auto = auto or sys.argv[1:]
    def __enter__(self, auto=None):
        if self.auto:
            stdin_setup.setup()
            setinput("\n".join(self.auto))
    def __exit__(self, type, value, traceback):
        stdin_setup.teardown()
stdin_auto = StdinAuto()

class Menu:
    """Menu object that will show the associated MenuEntry items."""
    def __init__(self, entries=None, **kwargs):
        """Initializes menu object. Any `kwargs` supplied will be passed as
        defaults to `show_menu()`."""
        self.entries = entries or []
        self._show_kwargs = kwargs
    def add(self, name, desc, func=None, args=None, krgs=None):
        """Add a menu entry."""
        self.entries.append(MenuEntry(name, desc, func, args or [], krgs or {}))
    def enum(self, desc, func=None, args=None, krgs=None):
        """Add a menu entry."""
        name = str(len(self.entries)+1)
        self.entries.append(MenuEntry(name, desc, func, args or [], krgs or {}))
    def show(self, **kwargs):
        """Shows the menu. Any `kwargs` supplied will be passed to
        `show_menu()`."""
        self._show_kwargs.update(kwargs)
        return show_menu(self.entries, **self._show_kwargs)
    def run(self, name):
        """Runs the function associated with the given entry `name`."""
        for entry in self.entries:
            if entry.name == name:
                run_func(entry)
                break
    def main(self, auto=None, loop=False, quit=("q", "Quit"), **kwargs):
        """Runs the standard menu main logic. Any `kwargs` supplied will be
        pass to `Menu.show()`. If `argv` is provided to the script, it will be
        used as the `auto` parameter.

        **Params:**
          - auto ([str]) - If provided, the list of strings with be used as
            input for the menu prompts.
          - loop (bool) - If true, the menu will loop until quit.
          - quit ((str,str)) - If provided, adds a quit option to the menu.
        """
        if quit:
            if self.entries[-1][:2] != quit:
                self.add(*quit)
        with StdinAuto(auto):
            if loop:
                note = "Menu loops until quit."
                while self.show(note=note, **kwargs) not in quit:
                    pass
            else:
                note = "Menu does not loop, single entry."
                return self.show(note=note, **kwargs)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

#: Returns a line of characters at the given width.
getline = lambda c, w: "".join([c for _ in range(w)])[:w]

#: String index replace.
stridxrep = lambda s, i, r: "".join([(s[x] if x != i else r) for x in range(len(s))])

#: Allows stdin to be set via function; use with `stdin_setup` context.
setinput = lambda x: [
        sys.stdin.seek(0),
        sys.stdin.truncate(0),
        sys.stdin.write(x),
        sys.stdin.seek(0)]

try:
    print("", end="", flush=True)
    echo = partial(print, end="\n", flush=True)
except TypeError:
    # TypeError: 'flush' is an invalid keyword argument for this function
    def echo(text="", end="\n", flush=True):
        """Generic echo/print function; based off code from ``blessed`` package."""
        sys.stdout.write(u'{0}{1}'.format(text, end))
        if flush:
            sys.stdout.flush()

def show_limit(entries, **kwargs):
    """Shows a menu but limits the number of entries shown at a time.
    Functionally equivalent to `show_menu()` with the `limit` parameter set."""
    limit = kwargs.pop('limit', 5)
    if limit <= 0:
        limit = 1
    istart = 0 # Index of group start.
    iend = limit # Index of group end.
    while True:
        if istart < 0:
            istart = 0
            iend = limit
        if iend > len(entries):
            iend = len(entries)
            istart = iend - limit
        unext = len(entries) - iend # Number of next entries.
        uprev = istart # Number of previous entries.
        nnext = "" # Name of 'next' menu entry.
        nprev = "" # Name of 'prev' menu entry.
        dnext = "" # Description of 'next' menu entry.
        dprev = "" # Description of 'prev' menu entry.
        group = copy.deepcopy(entries[istart:iend])
        names = [i.name for i in group]
        if unext:
            for i in ["n", "N", "next", "NEXT", "->", ">>", ">>>"]:
                if i not in names:
                    nnext = i
                    dnext = "Next %u entries" % (unext)
                    group.append(MenuEntry(nnext, dnext, None, None, None))
                    break
        if uprev:
            for i in ["p", "P", "prev", "PREV", "<-", "<<", "<<<"]:
                if i not in names:
                    nprev = i
                    dprev = "Previous %u entries" % (uprev)
                    group.append(MenuEntry(nprev, dprev, None, None, None))
                    break
        result = show_menu(group, **kwargs)
        if result == nnext or result == dnext:
            istart += limit
            iend += limit
        elif result == nprev or result == dprev:
            istart -= limit
            iend -= limit
        else:
            return result

def show_menu(entries, **kwargs):
    """Shows a menu with the given list of `MenuEntry` items.

    **Params**:
      - header (str) - String to show above menu.
      - note (str) - String to show as a note below menu.
      - msg (str) - String to show below menu.
      - compact (bool) - If true, the menu items will not be displayed [default: False].
      - returns (str) - Controls what part of the menu entry is returned [default: name].
      - limit (int) - If set, limits the number of menu entries show at a time [default: None].
    """
    header = kwargs.get('header', "-- MENU --")
    note = kwargs.get('note', "")
    msg = kwargs.get('msg', "Enter menu selection")
    compact = kwargs.get('compact', False)
    returns = kwargs.get('returns', "name")
    limit = kwargs.get('limit', None)
    if limit:
        return show_limit(entries, **kwargs)
    def show_banner():
        echo(header)
        for i in entries:
            echo("  (%s) %s" % (i.name, i.desc))
    valid = [i.name for i in entries]
    if not compact:
        show_banner()
    if note:
        alert(note)
    choice = ask(msg, vld=valid)
    entry = [i for i in entries if i.name == choice][0]
    run_func(entry)
    return getattr(entry, returns)

def run_func(entry):
    """Runs the function associated with the given entry."""
    if entry.func:
        if entry.args and entry.krgs:
            entry.func(*entry.args, **entry.krgs)
        elif entry.args:
            entry.func(*entry.args)
        elif entry.krgs:
            entry.func(**entry.krgs)
        else:
            entry.func()

def enum_menu(strs, menu=None):
    """Enumerates the given list of strings into returned menu.

    **Params**:
      - menu (Menu) - Existing menu to append. If not provided, a new menu will
        be created.
    """
    if not menu:
        menu = Menu()
    for s in strs:
        menu.enum(s)
    return menu

def cast(val, typ=int):
    """Attempts to cast the given value to the given type otherwise None is
    returned."""
    try:
        val = typ(val)
    except:
        val = None
    return val

def ask(msg="Enter input", fmt=None, dft=None, vld=None, shw=True, blk=False):
    """Prompts the user for input and returns the given answer. Optionally
    checks if answer is valid.

    **Params:**
      - msg (str) - Message to prompt the user with.
      - fmt (func) - Function used to format user input.
      - dft (int|float|str) - Default value if input is left blank.
      - vld ([int|float|str|func]) - Valid input entries.
      - shw (bool) - If true, show the user's input as typed.
      - blk (bool) - If true, accept a blank string as valid input.
    """
    vld = vld or []
    if not hasattr(vld, "__iter__"):
        vld = [vld]
    if not hasattr(fmt, "__call__"):
        fmt = lambda x: x  # NOTE: Defaults to function that does nothing.
    msg = "%s%s" % (QSTR, msg)
    dft = fmt(dft) if dft != None else None # Prevents showing [None] default.
    if dft != None:
        msg += " [%s]" % (dft if type(dft) is str else repr(dft))
        vld.append(dft)
    if vld:
        # Sanitize valid inputs.
        vld = list(set([fmt(v) if fmt(v) else v for v in vld]))
        if str not in vld:
            blk = False
        # NOTE: The following fixes a Py3 related bug found in `0.8.1`.
        try: vld = sorted(vld)
        except: pass
    msg += ISTR
    ans = None
    while ans is None:
        get_input = _input if shw else getpass
        ans = get_input(msg)
        if "?" == ans:
            if vld:
                echo("%r %s" % (vld, "(may be blank)" if blk else ""))
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
                elif hasattr(v, "__call__"):
                    try:
                        if v(ans):
                            break
                    except:
                        pass
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

def ask_captcha(length=4):
    """Prompts the user for a random string."""
    captcha = "".join(random.choice(string.ascii_lowercase) for _ in range(length))
    ask_str('Enter the following letters, "%s"' % (captcha), vld=[captcha, captcha.upper()], blk=False)

def pause():
    """Pauses and waits for user interaction."""
    getpass("Press ENTER to continue...")

def clear():
    """Clears the console."""
    if sys.platform.startswith("win"):
        call("cls", shell=True)
    else:
        call("clear", shell=True)

def status(*args, **kwargs):
    """Prints a status message at the start and finish of an associated
    function. Can be used as a function decorator or as a function that accepts
    another function as the first parameter.

    **Params:**

    The following parameters are available when used as a decorator:

      - msg (str) [args] - Message to print at start of `func`.

    The following parameters are available when used as a function:

      - msg (str) [args] - Message to print at start of `func`.
      - func (func) - Function to call. First `args` if using `status()` as a
        function. Automatically provided if using `status()` as a decorator.
      - fargs (list) - List of `args` passed to `func`.
      - fkrgs (dict) - Dictionary of `kwargs` passed to `func`.
      - fin (str) [kwargs] - Message to print when `func` finishes.
    """
    def decor(func):
        def wrapper(*args, **krgs):
            echo("[!] " + msg, end=" ", flush=True)
            result = func(*args, **krgs)
            echo(fin, flush=True)
            return result
        return wrapper
    fin = kwargs.pop('fin', "DONE.")
    args = list(args)
    if len(args) > 1 and callable(args[1]):
        msg = args.pop(0)
        func = args.pop(0)
        try: fargs = args.pop(0)
        except: fargs = []
        try: fkrgs = args.pop(0)
        except: fkrgs = {}
        return decor(func)(*fargs, **fkrgs)
    msg = args.pop(0)
    return decor

def alert(msg, **kwargs):
    """Prints alert message to console."""
    echo("[!] " + msg, **kwargs)

def error(msg, **kwargs):
    """Prints error message to console."""
    echo("[ERROR] " + msg, **kwargs)

def warn(msg, **kwargs):
    """Prints warning message to console."""
    echo("[WARNING] " + msg, **kwargs)

def title(msg):
    """Sets the title of the console window."""
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleA(msg)

def hrule(width=None, char=None):
    """Outputs or returns a horizontal line of the given character and width."""
    width = width or HRWIDTH
    char = char or HRCHAR
    echo(getline(char, width))

def wrap(body, header="", width=None, tchar=TCHAR, bchar=BCHAR, char=""):
    """Wraps the given body content between horizontal lines."""
    if char:
        bchar = tchar = char
    width = width or HRWIDTH
    top = "/" + getline(tchar, width-1)
    if header:
        top = stridxrep(top, 3, " ")
        for i,c in enumerate(header):
            top = stridxrep(top, i+4, header[i])
        top = stridxrep(top, i+5, " ")
    echo(top)
    echo(body)
    echo("\\" + getline(bchar, width-1))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
