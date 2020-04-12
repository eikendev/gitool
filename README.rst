.. image:: https://img.shields.io/travis/eikendev/gitool/master
    :alt: Build status
    :target: https://travis-ci.org/github/eikendev/gitool/builds/

.. image:: https://img.shields.io/pypi/status/gitool
    :alt: Development status
    :target: https://pypi.org/project/gitool/

.. image:: https://img.shields.io/pypi/l/gitool
    :alt: License
    :target: https://pypi.org/project/gitool/

.. image:: https://img.shields.io/pypi/pyversions/gitool
    :alt: Python version
    :target: https://pypi.org/project/gitool/

.. image:: https://img.shields.io/pypi/v/gitool
    :alt: Version
    :target: https://pypi.org/project/gitool/

.. image:: https://img.shields.io/pypi/dm/gitool
    :alt: Downloads
    :target: https://pypi.org/project/gitool/

Usage
=====

This tool can be used to manage many `Git <https://git-scm.com/>`_ repositories at once through the command line.
It can display repositories that contain uncommitted code or not yet pushed commits.
Another feature is to synchronize a list of your repositories including their configuration across multiple machines.

For a quick introduction, let me show how you would use the tool to get started.

.. code:: bash

    gitool status -d ~/git/

This command will collect status information for all repositories in ``~/git/`` and display a summary when done.
As can be seen above, you have to specify a directory where all your repositories are located in.

Installation
============

From PyPI
---------

.. code:: bash

    pip install gitool

From Source
-----------

.. code:: bash

    ./setup.py install

Fedora
------

.. code:: bash

    sudo dnf copr enable eikendev/gitool
    sudo dnf install gitool

Configuration
=============

A configuration file can be saved to ``~/.config/gitool/config.ini`` to avoid specifying the path for each invocation.
Of course, ``$XDG_CONFIG_HOME`` can be set to change your configuration path.
Alternatively, the path to the configuration file can be set via the ``--config-file`` argument.

.. code:: ini

    [GENERAL]
    RootDir = ~/git/

Development
===========

The source code is located on `GitHub <https://github.com/eikendev/gitool>`_.
To check out the repository, the following command can be used.

.. code:: bash

    git clone https://github.com/eikendev/gitool.git
