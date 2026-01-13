API reference
=============

The PyETK API contains the ``ToolkitBackend`` class, which provides methods for
controlling the toolkit workflow. This API provides methods
to create core types, bobbins, excitations, circuits, and ultimately put it all together as an electronic transformer model.
You use the PyETK API at the toolkit level.

The common methods for creating an AEDT session or connecting to an existing AEDT session are provided by the
`Common toolkit library <https://aedt.common.toolkit.docs.pyansys.com/>`_.


.. currentmodule:: ansys.aedt.toolkits.electronic_transformer.backend.api

.. autosummary::
   :toctree: _autosummary

   ToolkitBackend

You can use the Toolkit API as shown in this example:

.. code:: python

    # Backend instance
    toolkit_api = ToolkitBackend()

    # Sets common properties
    toolkit_api.properties.non_graphical = False
    toolkit_api.properties.aedt_version = "2025.2"

    # Defines the Json path
    json_file_name = "demo_EC.json"

    temp_dir = tempfile.TemporaryDirectory(suffix="_ansys")
    project_name = generate_unique_project_name(
        root_name=temp_dir.name, project_name="ETK_example"
    )
    json_path = Path(__file__).parents[3]
    json_path = Path(json_path) / "tests" / "backend" / "json_files" / json_file_name

    # Sets the Json reading properties
    toolkit_api.read_props_from_json(json_path)

    # Launches AEDT
    thread_msg = toolkit_api.launch_thread(toolkit_api.launch_aedt)
    idle = toolkit_api.wait_to_be_idle()
    if not idle:
        print("AEDT not initialized.")
        sys.exit()

    # Creates the models
    setup = toolkit_api.create_setup()
    core = toolkit_api.create_core_geometry()
    winding = toolkit_api.create_winding_geometry()
    bobbin = toolkit_api.create_bobbin_geometry()
    circuit = toolkit_api.create_circuit()
    region = toolkit_api.create_region()

    # Releases the AEDT
    toolkit_api.release_aedt()
