.. _custom_databases:

Custom material and core databases
==================================

PyETK ships with a material database (``material_properties.json``) and a core
dimensions database (``core_dimensions.json``). In the standalone application, you can add
your own materials and cores, or change shipped ones, without editing the shipped files.

How it works
------------

Each JSON file in your user data folder holds only what you add or change. When PyETK starts,
it loads the shipped database and merges your file on top of it:

- JSON objects are merged key by key.
- Any other value, such as a list or number, replaces the shipped value.

Because the shipped files are not modified, toolkit updates still reach you.

User data folder
----------------

The folder is selected as follows:

- If the ``PYAEDT_TOOLKIT_CONFIG_DIR`` environment variable is set, the folder is
  ``<PYAEDT_TOOLKIT_CONFIG_DIR>\data``.
- In the standalone application, the folder is
  ``%APPDATA%\Ansys\Electronic Transformer toolKit\data``. PyETK creates it on first start,
  with an empty ``{}`` file for each database.
- When running from source or a pip installation, user overrides are not used.

Adding a material
-----------------

Create or edit ``material_properties.json`` in the user data folder. The file must
contain a JSON object. For example, to add a ferrite material under ``core``, using the same
structure as the shipped file:

.. code-block:: json

    {
        "core": {
            "MY_FERRITE": {
                "conductivity": 1,
                "density": 4800,
                "power_ferrite_loss_params": {"cm": 2.55, "x": 1.485, "y": 2.51},
                "mu_vs_freq": [[1000, 2000], [10000, 1900]]
            }
        }
    }

To change a single property of a shipped material, include only that property:

.. code-block:: json

    {"core": {"3C81": {"density": 4900}}}

Adding a core
-------------

Use the same approach with ``core_dimensions.json``, following the structure of the
shipped file.

Error handling
--------------

If your file is not valid JSON or does not contain a JSON object, PyETK logs an error
and uses the shipped data only. A bad edit does not prevent the toolkit from starting.
Restart PyETK after editing the files.
