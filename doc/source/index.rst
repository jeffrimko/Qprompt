.. Qprompt documentation master file, created by
   sphinx-quickstart on Sat Apr 30 12:29:12 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Qprompt API
===========

This is the main documentation for the Qprompt API. Qprompt is a Python library for quickly creating user input prompts and various related functionality.

Contents:

.. toctree::
   :maxdepth: 2

Overview
========

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
.. autofunction:: qprompt.ask_float

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
.. autofunction:: qprompt.status
.. autofunction:: qprompt.title
