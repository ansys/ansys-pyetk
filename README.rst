Electronic Transformer toolKit (PyETK)
=============================================

|pyansys| |PythonVersion| |GH-CI| |Apache| |coverage| |ruff|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |GH-CI| image:: https://github.com/ansys/ansys-pyetk/actions/workflows/ci-main.yml/badge.svg
   :target: https://github.com/ansys/ansys-pyetk/actions/workflows/ci_cd.yml

.. |Apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |coverage| image:: https://codecov.io/gh/ansys/ansys-pyetk/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/ansys-pyetk

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff


The ``ansys-pyetk`` package provides a user-friendly interface to set up electronic transformer
models in Ansys Electronic Desktop (AEDT). The toolkit could be used inside AEDT or launched
from a python console. The toolkit leverages the common toolkit library that consists of two
main parts: a backend and a User Interface (UI).

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

The following are known missing functionality / current work in progress

- Remove button logic in Winding menu has not been implemented.
- Check of windings fitting in cores not implemented.

Expected Behaviour
------------------
ETK does not create a unique Maxwell model every time "Create Transformer" button is pressed,
after the first click it will create a model on top of the previous one.

Installation
~~~~~~~~~~~~
Visit the `Releases <https://github.com/ansys/ansys-pyetk/releases>`__ page and pull
down the latest installer.

Distributing
~~~~~~~~~~~~
This project is vectored to be an open-source project. For the time being, feel
free to distribute it internally, but direct users to visit the
`Releases <https://github.com/ansys/ansys-pyetk/releases>`__ page.

Security
~~~~~~~~
Information on how to report vulnerabilities can be found in the
`Security Policy <https://github.com/ansys/ansys-pyetk/blob/main/SECURITY.md>`__.

License
~~~~~~~
This toolkit is licensed under the Apache-2.0 license.

This module makes no commercial claim over Ansys whatsoever. The use of the interactive control
of this toolkit requires a legally licensed local copy of AEDT. For more information about AEDT,
visit the `AEDT page <https://www.ansys.com/products/electronics>`_ on the Ansys website.
