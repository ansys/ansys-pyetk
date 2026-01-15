"""PyETK Example.

This example shows how to use the ``ToolkitBackend`` API to create a transformer model in AEDT.

The example does the following:
- Initializes the ``ToolkitBackend`` class.
- Sets common properties like ``non_graphical`` and ``aedt_version``.
- Defines the path to the JSON file with the transformer properties.
- Reads the properties from the JSON file.
- Launches AEDT.
- Creates the transformer model.

"""

from pathlib import Path
import sys
import tempfile

from ansys.aedt.core import generate_unique_project_name
from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend

# Backend instance
toolkit_api = ToolkitBackend()

# Sets common properties
toolkit_api.properties.non_graphical = False
toolkit_api.properties.aedt_version = "2025.2"

# Defines the Json path
json_file_name = "RM_wound_circular.json"

temp_dir = tempfile.TemporaryDirectory(suffix="_ansys")
project_name = generate_unique_project_name(root_name=temp_dir.name, project_name="ETK_example")
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
setup = toolkit_api.create_model()
