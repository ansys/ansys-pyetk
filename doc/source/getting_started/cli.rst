.. _command line interface:

Command line interface
======================

PyETK provides a command line interface (command line interface) as a sub-command of the ``pyaedt`` command line interface,
enabling you to validate transformer configurations and create transformer models
in running AEDT instances without leaving the terminal.

Get started
-----------

To see the available PyETK commands, run:

.. code-block:: bash

    pyaedt etk --help

All commands can be run with ``--json`` to output results in JSON format for easy parsing in scripts.

.. code-block:: console

    $ pyaedt etk --json validate config.json
    {"file": "config.json", "status": "ok", "errors": []}

    $ pyaedt etk validate config.json
    ✓ config.json: Validation passed.


Main commands
-------------

The PyETK command line interface provides these commands:

* ``validate`` - Validate one or more transformer JSON configuration files (no AEDT required)
* ``create`` - Create a transformer model in a running AEDT instance


Validation commands
-------------------

Use the ``validate`` command to check if transformer configuration files are valid
without launching AEDT.

**Validate a single configuration file**

.. code-block:: bash

    pyaedt etk validate config.json

**Validate multiple files**

.. code-block:: bash

    pyaedt etk validate config1.json config2.json config3.json

**Get JSON output for scripting**

.. code-block:: bash

    pyaedt etk validate config.json --json

The JSON output includes the validation status and a list of any errors found.


Create commands
---------------

Use the ``create`` command to build a transformer model in a running AEDT instance.

**Prerequisites**

Before running the ``create`` command, you must start an AEDT session:

.. code-block:: bash

    pyaedt session start --version 2026.1

This displays the gRPC port (for example, ``50051``) that the session is using.

**Create a full model**

.. code-block:: bash

    pyaedt etk create config.json --port 50051

By default, the full transformer model is created: core, winding, bobbin, circuit, and setup.

**Create only specific parts**

You can build individual components using part flags:

.. code-block:: bash

    pyaedt etk create config.json --port 50051 --create-core
    pyaedt etk create config.json --port 50051 --create-winding
    pyaedt etk create config.json --port 50051 --create-bobbin

**Combine multiple parts**

.. code-block:: bash

    pyaedt etk create config.json --port 50051 --create-core --create-winding

This creates only the core and winding geometries, which is useful for iterating
on specific components without rebuilding the entire design.

**Get JSON output for scripting**

.. code-block:: bash

    pyaedt etk create config.json --port 50051 --json

The JSON output includes the creation status, list of created parts, project name, and design name.


Tips and tricks
---------------

**Find the gRPC port of a running session**

.. code-block:: bash

    pyaedt session list

This shows all running AEDT sessions with their PID, version, and gRPC port.

**Validate before creating**

Always validate your configuration file before attempting to create a model:

.. code-block:: bash

    pyaedt etk validate config.json
    pyaedt etk create config.json --port 50051

**Automate transformer creation**

Use the ``--json`` flag to integrate PyETK into automation scripts:

.. code-block:: bash

    # Validate and capture result
    RESULT=$(pyaedt etk validate config.json --json)
    
    # Create model if validation passed
    if echo $RESULT | jq -e '.status == "ok"' > /dev/null; then
        pyaedt etk create config.json --port 50051
    fi
