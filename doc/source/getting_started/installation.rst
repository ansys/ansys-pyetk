.. _installation:

Installation
============

You can install PyETK using an installer, using Python, or in developer mode. Choose the method that best suits your needs.

Install PyETK using an installer
================================

The repository's `Releases  <https://github.com/ansys/ansys-pyetk/releases>`_ page provides for
downloading PyETK assets. For the `latest PyETK release <https://github.com/ansys/ansys-pyetk/releases/latest/>`_, use one of these links to download the installer for your operating system:

- `Windows installer <https://github.com/ansys/ansys-pyetk/releases/latest/download/PyETK-Installer-Windows.exe>`_
- `Ubuntu 22.04 installer <https://github.com/ansys/ansys-pyetk/releases/latest/download/PyETK-Installer-ubuntu_22_04.zip>`_
- `Ubuntu 24.04 installer <https://github.com/ansys/ansys-pyetk/releases/latest/download/PyETK-Installer-ubuntu_24_04.zip>`_

.. tab-set::

  .. tab-item:: Windows

   Follow these steps to use the Windows installer to install PyETK in user mode:

   #. Download the `Windows installer <https://github.com/ansys/ansys-pyetk/releases/latest/download/PyETK-Installer-Windows.exe>`_. The file should be named ``PyETK-Installer-Windows.exe``.

   #. Run the installer.

   #. Search for ``PyETK`` and run it.

   The PyETK UI opens.

  .. tab-item:: Linux

   On Linux, supported operating systems are Ubuntu 22.04 and 24.04.

   Follow these steps to use a Linux installer to install PyETK in user mode:

   #. Run the following commands to update the ``apt-get`` repository and install these packages
      with **sudo** privileges: ``wget``, ``gnome``, ``libffi-dev``, ``libssl-dev``, ``libsqlite3-dev``, ``libxcb-xinerama0``, and ``build-essential``:

      .. code:: shell

         sudo apt-get update -y
         sudo apt-get install wget gnome libffi-dev libssl-dev libsqlite3-dev libxcb-xinerama0 build-essential -y

   #. Install the ``zlib`` package:

      .. code:: shell

         wget https://zlib.net/current/zlib.tar.gz
         tar xvzf zlib.tar.gz
         cd zlib-*
         make clean
         ./configure
         make
         sudo make install

   #. Install the Toolkit Template:

      #. Download the latest ``Toolkit-Template_*.zip`` file from the repository's
         `Release <https://github.com/ansys/ansys-pyetk/releases/latest>`_ page.

      #. Run this command on the terminal:

         .. code:: shell

            unzip Toolkit-Template_*.zip
            ./installer.sh

      #. Search for ``PyETK`` and run it.

   The PyETK UI opens.

To uninstall PyETK, follow these steps.

#. Select **File > Uninstall**.

#. Click **Uninstall**.

Install PyETK using Python
==========================

You can use Python to install from PyPI either both the PyETK backend and UI
methods or only the backend methods.

To install both the backend and UI methods:

.. code:: bash

    pip install ansys-pyetk[all]

To install only the backend methods:

.. code:: bash

    pip install ansys-pyetk

Install PyETK in developer mode
===============================

Installing PyETK in developer mode allows you to modify the source
and enhance it.

.. note::
   Before contributing to the project, see the `PyAnsys developer's guide`_.

You can install PyETK in developer mode with only these few lines of code:

.. code:: bash

   git clone https://github.com/ansys/ansys-pyetk
   cd ansys-pyetk
   python -m pip install -U pip uv
   uv venv
   uv pip install -e .

To run PyEDT, use this command:

.. code:: bash

   uv run run_toolkit

**Work environment setup**

To set up your work environment for development, follow these steps:

#. Create a fresh-clean Python environment and activate it. For more information,
   see the `venv`_ Python documentation.

   .. code:: bash

      # Create a virtual environment
      python -m uv venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Make sure you have the latest version of `pip`_:

   .. code:: bash

      python -m pip install -U pip uv

#. Install the project in editable mode:

   .. code:: bash

      python -m uv pip install -e .[tests,doc]

#. Verify your development installation by running the tests:

   .. code:: bash

      uv run pytest tests -v


Run style checks and tests
--------------------------
This project uses `pre-commit <https://pre-commit.com/>`_ to run style
checks and tests.

Install ``pre-commit``:

.. code::

   uv pip install pre-commit
   uv run pre-commit install

After each commit, ``pre-commit`` runs to ensure your changes follow project
style guidelines:

.. code::

   git commit -am 'fix style'
   isort....................................................................Passed
   black....................................................................Passed
   blacken-docs.............................................................Passed
   flake8...................................................................Passed
   codespell................................................................Passed
   pydocstyle...............................................................Passed
   check for merge conflicts................................................Passed
   debug statements (python)................................................Passed
   check yaml...............................................................Passed
   trim trailing whitespace.................................................Passed
   Validate GitHub Workflows................................................Passed

If you need to run ``pre-commit`` again on all files and not just staged files, run
it with the ``--all-files`` option:

.. code::

   uv run pre-commit run --all-files

Deploy a local build
--------------------
You can deploy PyETK as a *frozen* application using `PyInstaller
<https://pypi.org/project/pyinstaller/>`_:

.. code::

   uv pip install -e .[freeze]
   uv run pyinstaller frozen.spec

This generates app files at ``dist/ansys_pyetk/Electronic Transformer Toolkit.exe``. To
The ``Electronic Transformer Toolkit.exe`` is a standalone application,
without the need to install Python or any dependencies.

It is also possible to deploy an Windows installer using `NSIS`.

For more information see: `Distributing Toolkits <https://aedt.common.toolkit.docs.pyansys.com/version/stable/distributing.html>`_

Build documentation
-------------------
To build the documentation, run the usual rules provided in the
`Sphinx`_ Makefile:

.. code:: bash

    uv pip install -e .[doc]
    uv run make -C doc/ html

    # subsequently open the documentation with (under Linux):
    <your_browser_name> doc/html/index.html

.. LINKS AND REFERENCES
.. _PyAnsys developer's guide: https://dev.docs.pyansys.com/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pip: https://pypi.org/project/pip/
.. _venv: https://docs.python.org/3/library/venv.html