Electronic Transformer toolKit (PyETK)
=============================================

|pyansys| |PythonVersion| |GH-CI| |MIT| |coverage| |ruff|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |GH-CI| image:: https://github.com/ansys/ansys-pyetk/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/ansys-pyetk/actions/workflows/ci_cd.yml

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |coverage| image:: https://codecov.io/gh/ansys/ansys-pyetk/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/ansys-pyetk

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff


The ``ansys-pyetk`` package provides a user-friendly interface to set up \
electronic transformer models in Ansys Electronic Desktop (AEDT).
The toolkit could be used inside AEDT or launched from a python console.
The toolkit leverages the common toolkit library that consists of two main parts: a backend and a User Interface (UI).

- The backend has some common methods for controlling an AEDT session and also an
  API based on `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_.

- The UI consists of some common methods for creating a desktop app based on
  `Pyside6 <https://doc.qt.io/qtforpython-6/quickstart.html>`_.


Requirements
~~~~~~~~~~~~
In addition to the runtime dependencies listed in the installation information, this toolkit
requires Ansys Electronics Desktop (AEDT) 2025 R2 or later.


Documentation and issues
~~~~~~~~~~~~~~~~~~~~~~~~
Documentation is currently Work in Progress.

On the `issues <https://github.com/ansys/ansys-pyetk/issues>`_ page, you can
create issues to submit questions, report bugs, and request new features.

The following are known Issues

1) ETK does not create a unique Maxwell model every time "Create Transformer" button is pressed, after the first click it will create a model on top of the previous one
2) Side1 load always set to 100 Ohm in external circuit.
3) Frequency sweep missing.
4) Maxwell post processing Matrix parameters, Rectangular plots and Field overlays missing.
5) Save ETK button missing from UI.
6) Remove button not working.
7) Segmentation Angle line edit missing.
8) Fractional Model tick box missing.
9) Skin Layers tick box missing.
10) Core Material properties can be selected in UI combo but do not appear in Maxwell model
11) Core dimensions (D_1 to D_9) not editable in UI
12) Auto population of "Start New Design" and behaviour of arrow buttons in UI not fully functional
13) Example models "demo_planarComponents", "demo_rectangular_EC" and "demo_rectangular_EQ" produce cores with incorrect sizes due to 11)
14) Combo boxes in UI are dark when windows dark mode is used
15) Check of windings fitting in cores not implemented.

Tests:
Run tests_backend_api and tests_toolkit_rest_api independtly.

Installation
~~~~~~~~~~~~
Visit the `Releases
<https://github.com/ansys/ansys-pyetk/releases>`__ page and pull
down the latest installer.


Distributing
~~~~~~~~~~~~
This project is vectored to be an open-source project. For the time being, feel
free to distribute it internally, but direct users to visit the `Releases
<https://github.com/ansys/ansys-pyetk/releases>`__ page

Security
~~~~~~~~
The versions that are still supported for security updates can be found at
the `Security guidelines <https://github.com/ansys/python-installer-qt-gui/blob/main/SECURITY.md>`_
site. Information on how to report vulenrabilities is also found.


License
~~~~~~~
This toolkit is licensed under the MIT license.

This module makes no commercial claim over Ansys whatsoever.
The use of the interactive control of this toolkit requires a legally licensed
local copy of AEDT. For more information about AEDT,
visit the `AEDT page <https://www.ansys.com/products/electronics>`_
on the Ansys website.
