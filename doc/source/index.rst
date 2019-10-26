.. Qprompt documentation master file, created by
   sphinx-quickstart on Sat Apr 30 12:29:12 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

------------

.. image:: https://raw.githubusercontent.com/jeffrimko/Qprompt/master/doc/logo/qprompt.png

------------

.. image:: http://img.shields.io/:license-mit-blue.svg
.. image:: https://travis-ci.org/jeffrimko/Qprompt.svg?branch=master

------------

This is the main documentation for Qprompt, a Python library for quickly creating user input prompts and various related functionality.

For more information:

  - **Readme** - https://github.com/jeffrimko/Qprompt/blob/master/README.adoc - Main readme file.
  - **GitHub** - https://github.com/jeffrimko/Qprompt - Main version control repository.
  - **PyPI** - https://pypi.python.org/pypi/qprompt - Package index page.

.. include:: readme_excerpt.rst


Usage
-----
Start by importing Qprompt into your Python script:

.. code:: python

    import qprompt

You can prompt the user for various input types:

.. code:: python

    qprompt.ask_yesno()
    qprompt.ask_int()
    qprompt.ask_float()
    qprompt.ask_str()

All prompts requiring user input will start with ``[?]``:

.. code:: python

    qprompt.ask_int()
    # [?] Enter an integer:

At any prompt, the user can enter the ``?`` character to show valid
entries:

.. code:: python

    qprompt.ask_yesno()
    # [?] Proceed?: ?
    # ['N', 'NO', 'Y', 'YES', 'n', 'no', 'y', 'yes']

The default prompt message can be changed:

.. code:: python

    qprompt.ask_str("Enter your name")
    # [?] Enter your name:

An optional default value can be supplied:

.. code:: python

    qprompt.ask_yesno(default="y")
    # [?] Proceed? [y]:

Optional validity checks can be added:

.. code:: python

    qprompt.ask_int(valid=[1,2,3])
    # [?] Enter an integer: 4
    # [?] Enter an integer: 1

    qprompt.ask_str(valid=lambda x: x.startswith("spa"))
    # [?] Enter a string: foo
    # [?] Enter a string: spam

    qprompt.ask_str("Enter a path", valid=lambda x: os.path.exists(x))
    # [?] Enter a path: C:\Windows

Robot problem? Try using a captcha:

.. code:: python

    qprompt.ask_captcha()
    # [?] Enter the following letters, "kslg":

    qprompt.ask_captcha(length=6)
    # [?] Enter the following letters, "dkixzp":

Menus are easy to make:

.. code:: python

    menu = qprompt.Menu()
    menu.add("p", "Previous")
    menu.add("n", "Next")
    menu.add("q", "Quit")
    choice = menu.show()
    # -- MENU --
    #   (p) Previous
    #   (n) Next
    #   (q) Quit
    # [?] Enter menu selection:

The menu entry name (first parameter of ``add()``) is returned by
default but can be changed:

.. code:: python

    print(menu.show())
    # [?] Enter menu selection: p
    # p

    print(menu.show(returns="desc"))
    # [?] Enter menu selection: p
    # Previous

Your menus can do cool stuff by registering functions:

.. code:: python

    def foo(a, b):
        print(a + b)
    menu.add("f", "foo", foo, [1, 2])

If you just need a quick menu to call functions:

.. code:: python

    Menu(func1, func2, func3).show()

Additionally, menus can be searched with fzf by entering `/` at the prompt. This feature uses the excellent `iterfzf library by dahlia <https://github.com/dahlia/iterfzf>`_. Example of the menu fzf search feature:

.. image:: ../demos/menu_fzf_demo.gif

Some print-like functions:

.. code:: python

    qprompt.echo("foo")
    # foo

    qprompt.alert("bar")
    # [!] bar

    qprompt.warn("baz")
    # [WARNING] baz

    qprompt.error("qux")
    # [ERROR] qux

    qprompt.fatal("ugh")
    # [FATAL] ugh

Got a function that takes a while? Show that it is running with
``status`` which can be used as a function or decorator:

.. code:: python

    qprompt.status("Doing stuff...", time.sleep, [1])
    # [!] Doing stuff... DONE.

    @qprompt.status("Doing more stuff...")
    def do_stuff():
        time.sleep(1)
    do_stuff()
    # [!] Doing more stuff... DONE.

Additional convenience functions:

.. code:: python

    qprompt.pause()
    # Press ENTER to continue...

    qprompt.hrule(width=10)
    # ----------

    qprompt.wrap("hello world", "hi", width=10)
    # /-- hi ---
    # hello world
    # \---------

Check out the following additional examples of Qprompt; more can be
found
`here <https://github.com/jeffrimko/Qprompt/tree/master/examples>`__:

-  `examples/ask\_1.py <https://github.com/jeffrimko/Qprompt/blob/master/examples/ask_1.py>`__
   - Basic info prompting.

-  `examples/menu\_1.py <https://github.com/jeffrimko/Qprompt/blob/master/examples/menu_1.py>`__
   - Basic menu usage.

-  `examples/display\_1.py <https://github.com/jeffrimko/Qprompt/blob/master/examples/display_1.py>`__
   - Basic display functions.

-  `examples/status\_1.py <https://github.com/jeffrimko/Qprompt/blob/master/examples/status_1.py>`__
   - Basic status function usage.

Compatibility Note
~~~~~~~~~~~~~~~~~~
Note that for backwards compatibility purposes, the following `kwargs` are equivalent:

  - `blk` = `blank`
  - `dft` = `default`
  - `hdr` = `header`
  - `hlp` = `help`
  - `msg` = `message`
  - `shw` = `show`
  - `vld` = `valid`

For example, the following calls are equivalent:

.. code-block:: python

    qprompt.ask_yesno(dft="y")
    qprompt.ask_yesno(default="y")

Input Automation
~~~~~~~~~~~~~~~~

User input can be automated using command-line arguments to the script.

Use the ``StdinAuto()`` context manager to automatically pass a list of
strings to input functions:

.. code:: python

    with qprompt.StdinAuto(["foo","bar","42"]):
        print(ask_str())
        print(ask_str())
        print(ask_int())
    # foo
    # bar
    # 42

The ``stdin_auto`` context manager will automatically pass script
command-line arguments to input functions:

.. code:: python

    with qprompt.stdin_auto:
        print(ask_str())
        print(ask_str())
        print(ask_int())
    # $ python example.py foo bar 42
    # foo
    # bar
    # 42

Menus can be automated using the ``main()`` method:

.. code:: python

    menu = qprompt.Menu
    menu.add("f", "Foo", some_useful_function)
    menu.add("b", "Bar", another_useful_function)
    menu.main()
    # $ python example.py f
    # some_useful_function() ran just now!

Menus can optionally loop allowing for multiple tasks to be run:

.. code:: python

    menu = qprompt.Menu
    menu.add("f", "Foo", some_useful_function)
    menu.add("b", "Bar", another_useful_function)
    menu.main(loop=True)
    # $ python example.py f b q
    # some_useful_function() ran just now!
    # another_useful_function() ran just now!

If no arguments are passed to the script, the input prompts will act as
normal.

API Documentation
-----------------

Console Output
~~~~~~~~~~~~~~
These functions write to the console. They are essentially slight variations of the Python3 ``print()`` function and each adds a prefix to the displayed message.

.. autofunction:: qprompt.echo
.. autofunction:: qprompt.alert
.. autofunction:: qprompt.info
.. autofunction:: qprompt.warn
.. autofunction:: qprompt.error

User Input
~~~~~~~~~~
These functions prompt the user for input.

This is the generic user input function:

.. autofunction:: qprompt.ask

These functions accept only specific data types:

.. autofunction:: qprompt.ask_yesno
.. autofunction:: qprompt.ask_int
.. autofunction:: qprompt.ask_float
.. autofunction:: qprompt.ask_str
.. autofunction:: qprompt.ask_pass

Additional input functions:

.. autofunction:: qprompt.ask_captcha

Menus
~~~~~
These classes/functions provide a method to quickly create menus for user input.

This is the menu entry type:

.. autodata:: qprompt.MenuEntry

A list of ``MenuEntry`` items can be passed to the following functions to create a menu:

.. autofunction:: qprompt.show_menu
.. autofunction:: qprompt.show_limit

The following class provides an object-based method of creating menus:

.. autoclass:: qprompt.Menu
    :members:

Additionally, a list of strings can be automatically enumerated into a menu with the following:

.. autofunction:: qprompt.enum_menu

Helpers
~~~~~~~
The following are miscellaneous convenience functions:

.. autofunction:: qprompt.cast
.. autofunction:: qprompt.clear
.. autofunction:: qprompt.hrule
.. autofunction:: qprompt.pause
.. autofunction:: qprompt.title
.. autofunction:: qprompt.status
.. autofunction:: qprompt.wrap

Automation
~~~~~~~~~~
The following helpers are provided for automation:

.. autofunction:: qprompt.StdinSetup
.. autofunction:: qprompt.setinput
.. autofunction:: qprompt.StdinAuto
