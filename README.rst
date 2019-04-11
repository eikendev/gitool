Installation
============

From PyPI
---------
::

   pip install gitool

From Source
-----------
::

   ./setup.py install

Usage
=====

This tool can be used to manage many `Git <https://git-scm.com/>`_ repositories at once through the command line.
``gitool`` can display repositories that contain uncommitted code.
Another feature is to synchronize a list of your repositories including their configuration across multiple machines.

For a quick introduction, let me show how you would use the tool to get started.
::

    $ gitool status -d ~/git/

This will collect status information for all repositories in ``~/git/`` and display a summary when done.
As can be seen above, you have to specify a directory where all your repositories are located in.

Configuration
=============

A configuration file can be saved to ``~/.config/gitool/config.ini`` to avoid specifying the path for each invocation.
Of course, ``$XDG_CONFIG_HOME`` can be set to change your configuration path.
::

    [GENERAL]
    RootDir = ~/git/
