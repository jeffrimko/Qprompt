"""This library provides a quick method of creating command line prompts for
user input."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from __future__ import print_function

import copy
import ctypes
import random
import string
import os
import sys
from collections import namedtuple
from functools import partial
from getpass import getpass
from subprocess import call
from functools import wraps

##==============================================================#
## SECTION: Special Setup                                       #
##==============================================================#

# Handle Python 2/3 differences.
if sys.version_info >= (3, 0):
    from io import StringIO
    tounicode = lambda s: s
else:
    from StringIO import StringIO
    tounicode = lambda s: unicode(s, "utf-8")

def _format_kwargs(func):
    """Decorator to handle formatting kwargs to the proper names expected by
    the associated function. The formats dictionary string keys will be used as
    expected function kwargs and the value list of strings will be renamed to
    the associated key string."""
    formats = {}
    formats['blk'] = ["blank"]
    formats['dft'] = ["default"]
    formats['hdr'] = ["header"]
    formats['hlp'] = ["help"]
    formats['msg'] = ["message"]
    formats['shw'] = ["show"]
    formats['vld'] = ["valid"]
    @wraps(func)
    def inner(*args, **kwargs):
        for k in formats.keys():
            for v in formats[k]:
                if v in kwargs:
                    kwargs[k] = kwargs[v]
                    kwargs.pop(v)
        return func(*args, **kwargs)
    return inner

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.16.3"

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

#: Default menu find/search command character.
FCHR = "/"

#: Flag to indicate if running in auto mode.
_AUTO = False

#: User input function.
_input = input if sys.version_info >= (3, 0) else raw_input

#: If true, prevents stdout from displaying.
SILENT = False

#: If true, echo() returns the string to print.
ECHORETURN = True

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
    def __init__(self, *entries, **kwargs):
        """Initializes menu object. Any `kwargs` supplied will be passed as
        defaults to `show_menu()`."""
        self.entries = []
        for entry in entries:
            if callable(entry):
                name = _guess_name(entry.__name__, [e.name for e in self.entries])
                desc = _guess_desc(entry.__name__)
                entry = (name, desc, entry)
            self.add(*entry)
        self._show_kwargs = kwargs
    def add(self, name, desc, func=None, args=None, krgs=None):
        """Add a menu entry."""
        self.entries.append(MenuEntry(name, desc, func, args or [], krgs or {}))
    def enum(self, desc, func=None, args=None, krgs=None):
        """Add a menu entry whose name will be an auto indexed number."""
        name = str(len(self.entries)+1)
        self.entries.append(MenuEntry(name, desc, func, args or [], krgs or {}))
    def show(self, **kwargs):
        """Shows the menu. Any `kwargs` supplied will be passed to
        `show_menu()`."""
        show_kwargs = copy.deepcopy(self._show_kwargs)
        show_kwargs.update(kwargs)
        return show_menu(self.entries, **show_kwargs)
    def get(self, name):
        """Gets the MenuEntry associated with the given `name`."""
        for entry in self.entries:
            if entry.name == name:
                return entry
    def run(self, name):
        """Runs the function associated with the given entry `name`."""
        entry = get_entry(name)
        if entry:
            run_func(entry)
    def main(self, auto=None, loop=False, quit=("q", "Quit"), **kwargs):
        """Runs the standard menu main logic. Any `kwargs` supplied will be
        pass to `Menu.show()`. If `argv` is provided to the script, it will be
        used as the `auto` parameter.

        **Params**:
          - auto ([str]) - If provided, the list of strings with be used as
            input for the menu prompts.
          - loop (bool) - If true, the menu will loop until quit.
          - quit ((str,str)) - If provided, adds a quit option to the menu.
        """
        def _main():
            global _AUTO
            if quit:
                if self.entries[-1][:2] != quit:
                    self.add(*quit, func=lambda: quit[0])
            if stdin_auto.auto:
                _AUTO = True
            result = None
            if loop:
                note = "Menu loops until quit."
                try:
                    while True:
                        mresult = self.show(note=note, **kwargs)
                        if mresult in quit:
                            break
                        result = mresult
                except EOFError:
                    pass
                return result
            else:
                note = "Menu does not loop, single entry."
                try:
                    result = self.show(note=note, **kwargs)
                    if result in quit:
                        return None
                except EOFError:
                    pass
            return result
        global _AUTO
        if _AUTO:
            return _main()
        else:
            with stdin_auto:
                return _main()

class Wrap(object):
    """Context manager that wraps content between horizontal lines.

    **Examples**:
    ::

        with qprompt.Wrap():
            qprompt.echo("Hello world!")
    """
    @_format_kwargs
    def __init__(self, width=None, char="", **kwargs):
        hdr = kwargs.get('hdr', "")
        char = char or HRCHAR
        width = width or HRWIDTH
        top = "/" + getline(char, width-1)
        if hdr:
            top = stridxrep(top, 3, " ")
            for i,c in enumerate(hdr):
                top = stridxrep(top, i+4, hdr[i])
            top = stridxrep(top, i+5, " ")
        self.top = top
        self.bot = "\\" + getline(char, width-1)
    def __enter__(self):
        echo(self.top)
        return self
    def __exit__(self, type, value, traceback):
        echo(self.bot)

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
    def echo(text="", end="\n", flush=True):
        if not SILENT:
            print(text, end=end, flush=flush)
        if ECHORETURN:
            return text + end
except TypeError:
    def echo(text="", end="\n", flush=True):
        """Generic echo/print function; based off code from ``blessed``
        package. Returns the printed string."""
        if not SILENT:
            sys.stdout.write(u'{0}{1}'.format(text, end))
            if flush:
                sys.stdout.flush()
        if ECHORETURN:
            return text + end

@_format_kwargs
def show_limit(entries, **kwargs):
    """Shows a menu but limits the number of entries shown at a time.
    Functionally equivalent to `show_menu()` with the `limit` parameter set."""
    limit = kwargs.pop('limit', 5)
    if limit <= 0:
        return show_menu(entries, **kwargs)
    istart = 0 # Index of group start.
    iend = limit # Index of group end.
    dft = kwargs.pop('dft', None)
    if type(dft) == int:
        dft = str(dft)
    while True:
        if iend > len(entries):
            iend = len(entries)
            istart = iend - limit
        if istart < 0:
            istart = 0
            iend = limit
        unext = len(entries) - iend # Number of next entries.
        uprev = istart # Number of previous entries.
        nnext = "" # Name of 'next' menu entry.
        nprev = "" # Name of 'prev' menu entry.
        dnext = "" # Description of 'next' menu entry.
        dprev = "" # Description of 'prev' menu entry.
        group = copy.deepcopy(entries[istart:iend])
        names = [i.name for i in group]
        if unext > 0:
            for i in ["n", "N", "next", "NEXT", "->", ">>", ">>>"]:
                if i not in names:
                    nnext = i
                    dnext = "Next %u of %u entries" % (unext, len(entries))
                    group.append(MenuEntry(nnext, dnext, None, None, None))
                    names.append("n")
                    break
        if uprev > 0:
            for i in ["p", "P", "prev", "PREV", "<-", "<<", "<<<"]:
                if i not in names:
                    nprev = i
                    dprev = "Previous %u of %u entries" % (uprev, len(entries))
                    group.append(MenuEntry(nprev, dprev, None, None, None))
                    names.append("p")
                    break
        tmpdft = None
        if dft != None:
            if dft not in names:
                if "n" in names:
                    tmpdft = "n"
            else:
                tmpdft = dft
        result = show_menu(group, dft=tmpdft, **kwargs)
        if result == nnext or result == dnext:
            istart += limit
            iend += limit
        elif result == nprev or result == dprev:
            istart -= limit
            iend -= limit
        else:
            return result

@_format_kwargs
def show_menu(entries, **kwargs):
    """Shows a menu with the given list of MenuEntry items.

    **Params**:
      - header (str) - String to show above menu.
      - note (str) - String to show as a note below menu.
      - msg (str) - String to show below menu.
      - dft (str) - Default value if input is left blank.
      - compact (bool) - If true, the menu items will not be displayed.
        [default: False]
      - returns (str) - Controls what part of the MenuEntry is returned,
        'func' returns function result. [default: name]
      - limit (int) - If set, limits the number of menu entries show at a time.
        [default: None]
      - fzf (bool) - If true, can enter FCHR at the menu prompt to search menu.
    """
    global _AUTO
    hdr = kwargs.get('hdr', "")
    note = kwargs.get('note', "")
    dft = kwargs.get('dft', "")
    fzf = kwargs.pop('fzf', True)
    compact = kwargs.get('compact', False)
    returns = kwargs.get('returns', "name")
    limit = kwargs.get('limit', None)
    dft = kwargs.get('dft', None)
    msg = []
    if limit:
        return show_limit(entries, **kwargs)
    def show_banner():
        banner = "-- MENU"
        if hdr:
            banner += ": " + hdr
        banner += " --"
        msg.append(banner)
        if _AUTO:
            return
        for i in entries:
            msg.append("  (%s) %s" % (i.name, i.desc))
    valid = [i.name for i in entries]
    if type(dft) == int:
        dft = str(dft)
    if dft not in valid:
        dft = None
    if not compact:
        show_banner()
    if note and not _AUTO:
        msg.append("[!] " + note)
    if fzf:
        valid.append(FCHR)
    if _AUTO:
        valid.append("-d")
    msg.append(QSTR + kwargs.get('msg', "Enter menu selection"))
    msg = os.linesep.join(msg)
    entry = None
    while entry not in entries:
        choice = ask(msg, vld=valid, dft=dft, qstr=False)
        if _AUTO and choice == "-d":
            choice = dft
        if choice == FCHR and fzf:
            try:
                from iterfzf import iterfzf
                choice = iterfzf(reversed(["%s\t%s" % (i.name, i.desc) for i in entries])).strip("\0").split("\t", 1)[0]
            except:
                warn("Issue encountered during fzf search.")
        match = [i for i in entries if i.name == choice]
        if match:
            entry = match[0]
    if entry.func:
        fresult = run_func(entry)
        if "func" == returns:
            return fresult
    try:
        return getattr(entry, returns)
    except:
        return getattr(entry, "name")

def run_func(entry):
    """Runs the function associated with the given MenuEntry."""
    if entry.func:
        if entry.args and entry.krgs:
            return entry.func(*entry.args, **entry.krgs)
        if entry.args:
            return entry.func(*entry.args)
        if entry.krgs:
            return entry.func(**entry.krgs)
        return entry.func()

def enum_menu(strs, menu=None, *args, **kwargs):
    """Enumerates the given list of strings into returned menu.

    **Params**:
      - menu (Menu) - Existing menu to append. If not provided, a new menu will
        be created.
    """
    if not menu:
        menu = Menu(*args, **kwargs)
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

@_format_kwargs
def ask(msg="Enter input", fmt=None, dft=None, vld=None, shw=True, blk=False, hlp=None, qstr=True, multi=False, **kwargs):
    """Prompts the user for input and returns the given answer. Optionally
    checks if answer is valid.

    **Params**:
      - msg (str) - Message to prompt the user with.
      - fmt (func) - Function used to format user input.
      - dft (int|float|str) - Default value if input is left blank.
      - vld ([int|float|str|func]) - Valid input entries.
      - shw (bool) - If true, show the user's input as typed.
      - blk (bool) - If true, accept a blank string as valid input; blank input
        will be accepted even if the `vld` parameter is supplied. Note that
        supplying a default value will disable accepting blank input.
    """
    global _AUTO
    def print_help():
        lst = [v for v in vld if not callable(v)]
        if blk:
            lst.remove("")
        for v in vld:
            if not callable(v):
                continue
            if int == v:
                lst.append("<int>")
            elif float == v:
                lst.append("<float>")
            elif str == v:
                lst.append("<str>")
            else:
                lst.append("(" + v.__name__ + ")")
        if lst:
            echo("[HELP] Valid input: %s" % (" | ".join([str(l) for l in lst])))
        if hlp:
            echo("[HELP] Extra notes: " + hlp)
        if blk:
            echo("[HELP] Input may be blank.")
    vld = vld or []
    hlp = hlp or ""
    if not hasattr(vld, "__iter__"):
        vld = [vld]
    if not hasattr(fmt, "__call__"):
        fmt = lambda x: x  # NOTE: Defaults to function that does nothing.
    msg = "%s%s" % (QSTR if qstr else "", msg)
    dft = fmt(dft) if dft != None else None # Prevents showing [None] default.
    if dft != None:
        msg += " [%s]" % (dft if type(dft) is str else repr(dft))
        vld.append(dft)
        blk = False
    if vld:
        # Sanitize valid inputs.
        vld = list(set([fmt(v) if fmt(v) else v for v in vld]))
        if blk and "" not in vld:
            vld.append("")
        # NOTE: The following fixes a Py3 related bug found in `0.8.1`.
        try: vld = sorted(vld)
        except: pass
    msg += ISTR
    ans = None
    while ans is None:
        get_input = _input if shw else getpass
        ans = get_input(msg)
        if _AUTO:
            echo(ans)
        if "?" == ans:
            print_help()
            ans = None
            continue
        if "" == ans:
            if dft != None:
                ans = dft if not fmt else fmt(dft)
                break
            if "" not in vld:
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

@_format_kwargs
def ask_yesno(msg="Proceed?", dft=None, **kwargs):
    """Prompts the user for a yes or no answer. Returns True for yes, False
    for no."""
    yes = ["y", "yes", "Y", "YES"]
    no = ["n", "no", "N", "NO"]
    if dft != None:
        dft = yes[0] if (dft in yes or dft == True) else no[0]
    return ask(msg, dft=dft, vld=yes+no) in yes

@_format_kwargs
def ask_int(msg="Enter an integer", dft=None, vld=None, hlp=None, **kwargs):
    """Prompts the user for an integer."""
    vld = vld or [int]
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=int), hlp=hlp)

@_format_kwargs
def ask_float(msg="Enter a float", dft=None, vld=None, hlp=None, **kwargs):
    """Prompts the user for a float."""
    vld = vld or [float]
    return ask(msg, dft=dft, vld=vld, fmt=partial(cast, typ=float), hlp=hlp)

@_format_kwargs
def ask_str(msg="Enter a string", dft=None, vld=None, shw=True, blk=True, hlp=None, **kwargs):
    """Prompts the user for a string."""
    vld = vld or [str]
    return ask(msg, dft=dft, vld=vld, shw=shw, blk=blk, hlp=hlp)

#: Alias for `ask_str(shw=False)`.
ask_pass = partial(ask_str, msg="Enter password", shw=False)

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

    **Params**:

    The following parameters are available when used as a decorator:

      - msg (str) [args] - Message to print at start of `func`.

    The following parameters are available when used as a function:

      - msg (str) [args] - Message to print at start of `func`.
      - func (func) - Function to call. First `args` if using `status()` as a
        function. Automatically provided if using `status()` as a decorator.
      - fargs (list) - List of `args` passed to `func`.
      - fkrgs (dict) - Dictionary of `kwargs` passed to `func`.
      - fin (str) [kwargs] - Message to print when `func` finishes.

    **Examples**:
    ::

        @qprompt.status("Something is happening...")
        def do_something(a):
            time.sleep(a)

        do_something()
        # [!] Something is happening... DONE.

        qprompt.status("Doing a thing...", myfunc, [arg1], {krgk: krgv})
        # [!] Doing a thing... DONE.
    """
    def decor(func):
        @wraps(func)
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

def fatal(msg, exitcode=1, **kwargs):
    """Prints a message then exits the program. Optionally pause before exit
    with `pause=True` kwarg."""
    # NOTE: Can't use normal arg named `pause` since function has same name.
    pause_before_exit = kwargs.pop("pause") if "pause" in kwargs.keys() else False
    echo("[FATAL] " + msg, **kwargs)
    if pause_before_exit:
        pause()
    sys.exit(exitcode)

def error(msg, **kwargs):
    """Prints error message to console. Returns printed string."""
    return echo("[ERROR] " + msg, **kwargs)

def warn(msg, **kwargs):
    """Prints warning message to console. Returns printed string."""
    return echo("[WARNING] " + msg, **kwargs)

def info(msg, **kwargs):
    """Prints info message to console. Returns printed string."""
    return echo("[INFO] " + msg, **kwargs)

def alert(msg, **kwargs):
    """Prints alert message to console. Returns printed string."""
    return echo("[!] " + msg, **kwargs)

def hrule(width=None, char=None):
    """Outputs or returns a horizontal line of the given character and width.
    Returns printed string."""
    width = width or HRWIDTH
    char = char or HRCHAR
    return echo(getline(char, width))

def title(msg):
    """Sets the title of the console window."""
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleW(tounicode(msg))

@_format_kwargs
def wrap(item, args=None, krgs=None, **kwargs):
    """Wraps the given item content between horizontal lines. Item can be a
    string or a function.

    **Examples**:
    ::

        qprompt.wrap("Hi, this will be wrapped.")  # String item.
        qprompt.wrap(myfunc, [arg1, arg2], {'krgk': krgv})  # Func item.
    """
    with Wrap(**kwargs):
        if callable(item):
            args = args or []
            krgs = krgs or {}
            return item(*args, **krgs)
        else:
            echo(item)

def _guess_name(desc, taken=None):
    """Attempts to guess the MenuEntry name from the function name."""
    taken = taken or []
    name = ""
    # Try to find the shortest name based on the given description.
    for word in desc.split():
        c = word[0].lower()
        if not c.isalnum():
            continue
        name += c
        if name not in taken:
            break
    # If name is still taken, add a number postfix.
    count = 2
    while name in taken:
        name = name + str(count)
        count += 1
    return name

def _guess_desc(fname):
    """Attempts to guess the MenuEntry description from the function name."""
    return fname.title().replace("_", " ")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
