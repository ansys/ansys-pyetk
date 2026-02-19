.. _architecture:

Architecture
============

The Electronic Transformer toolKit (PyETK) main dependency is the `PyAEDT Common Toolkit <https://aedt.common.toolkit.docs.pyansys.com/version/stable/index.html>`_, a package that provides common methods and best practices for creating Ansys Electronics Desktop toolkits.
To better understand the toolkit template architecture (backend and user interface) you can refer to the `PyAEDT Common Toolkit Architecture <https://aedt.common.toolkit.docs.pyansys.com/version/stable/getting_started/architecture.html>`_.
To understand how the Backend API is structured and see an example refer to `Backend API reference <https://aedt.common.toolkit.docs.pyansys.com/version/stable/toolkit/api.html>`_.
The `UI API reference <https://aedt.common.toolkit.docs.pyansys.com/version/stable/toolkit/ui.html>`_ explains how the UI is built and its modules.


The PyETK's file structure is the following

.. code-block:: text

    ansys-pyetk
    ├───.github
    │   └───workflows
    ├───.idea
    │   └───inspectionProfiles
    ├───.reuse
    │   └───templates
    ├───doc
    │   ├───changelog.d
    │   ├───source
    │   │   ├───examples
    │   │   ├───getting_started
    │   │   ├───toolkit
    │   │   │   └───_autosummary
    │   │   ├───_static
    │   │   │   ├───assets
    │   │   │   │   └───download
    │   │   │   └───thumbnails
    │   │   └───_templates
    │   └───styles
    │       └───config
    │           └───vocabularies
    │               └───ANSYS
    ├───installer
    │   ├───assets
    │   │   └───scripts
    │   ├───hooks
    │   └───linux
    │       └───debian
    ├───src
    │   └───ansys
    │       └───aedt
    │           └───toolkits
    │               └───electronic_transformer
    │                   ├───backend
    │                   │   └───workflows
    │                   ├───data
    │                   └───ui
    │                       └───windows
    │                           ├───help
    │                           ├───images
    │                           └───transformer_input
    └───tests
        └───backend
            ├───json_files
            ├───tests_backend_api
            └───tests_toolkit_rest_api


- `.github <https://github.com/ansys/ansys-pyetk/tree/main/.github>`_: GitHub Action configuration.

- `doc <https://github.com/ansys/ansys-pyetk/tree/main/doc>`_: Documentation structure.

- `template <https://github.com/ansys/ansys-pyetk/tree/main/src/ansys/aedt/toolkits/template>`_:
  Toolkit code, split into backend and UI.

  - `backend <https://github.com/ansys/ansys-pyetk/tree/main/src/ansys/aedt/toolkits/template/backend>`_:
     Non-user-facing part of the toolkit for handling requests and preparing data for the UI. Key files include:

    - ``rest_api.py``: Defines Flask entrypoints.
    - ``api.py``: Defines the toolkit API.
    - ``backend_properties.toml``: Defines common backend properties.
    - ``models.py``: Defines the class for storing backend properties.

  - `ui <https://github.com/ansys/ansys-pyetk/tree/main/src/ansys/aedt/toolkits/template/ui>`_: UI part of
    the toolkit. Key files include:

    - ``frontend_properties.toml``: Defines common UI properties.
    - ``models.py``: Defines the class for storing UI properties.

- `tests <https://github.com/ansys/ansys-pyetk/tree/main/tests>`_: Folder containing the backend
  unit tests.

- `installer <https://github.com/ansys/ansys-pyetk/tree/main/installer>`_: Folder containing the
  installer configuration files.
