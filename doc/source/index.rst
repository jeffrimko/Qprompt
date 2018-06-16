.. Qprompt documentation master file, created by
   sphinx-quickstart on Sat Apr 30 12:29:12 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Qprompt
=======

This is the main documentation for Qprompt, a Python library for quickly creating user input prompts and various related functionality.

For more information:

  - **Readme** - https://github.com/jeffrimko/Qprompt/blob/master/README.adoc - Main readme file.
  - **GitHub** - https://github.com/jeffrimko/Qprompt - Main version control repository.
  - **PyPI** - https://pypi.python.org/pypi/qrompt - Package index page.

Compatibility Note
------------------
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

Console Output
--------------
These functions write to the console. They are essentially slight variations of the Python3 ``print()`` function and each adds a prefix to the displayed message.

.. autofunction:: qprompt.echo
.. autofunction:: qprompt.alert
.. autofunction:: qprompt.warn
.. autofunction:: qprompt.error

User Input
----------
These functions prompt the user for input.

This is the generic user input function:

.. autofunction:: qprompt.ask

These functions accept only specific data types:

.. autofunction:: qprompt.ask_yesno
.. autofunction:: qprompt.ask_str
.. autofunction:: qprompt.ask_int
.. autofunction:: qprompt.ask_float

Additional input functions:

.. autofunction:: qprompt.ask_captcha

Menus
-----
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
-------
The following are miscellaneous convenience functions:

.. autofunction:: qprompt.cast
.. autofunction:: qprompt.clear
.. autofunction:: qprompt.hrule
.. autofunction:: qprompt.pause
.. autofunction:: qprompt.status
.. autofunction:: qprompt.title
.. autofunction:: qprompt.wrap

Automation
~~~~~~~~~~
The following helpers are provided for automation:

.. autofunction:: qprompt.StdinSetup
.. autofunction:: qprompt.setinput
.. autofunction:: qprompt.StdinAuto
