# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create parts of transformer model and edit them in AEDT using the PyETK API.

This example uses :class:`ToolkitBackend` to:

- Initialize the backend.
- Set common properties such as ``non_graphical`` and ``aedt_version``.
- Load transformer properties from a JSON file.
- Launch AEDT.
- Create core and winding geometries.
- Update their properties
- Create updated geometries.
"""

# ## Perform required imports
from pathlib import Path
import sys

from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend

# ## Create backend instance
toolkit_api = ToolkitBackend()

# ## Set common properties
toolkit_api.properties.non_graphical = False
toolkit_api.properties.aedt_version = "2026.1"
toolkit_api.properties.active_project = "PyETK_Example"

# ## Define the JSON path
json_file_name = "RM_wound_circular.json"
try:
    # Works in standard .py scripts
    json_path = Path(__file__).resolve().parents[3]
except NameError:
    # Fallback for Jupyter / Interactive sessions
    json_path = Path.cwd().parents[2]
json_path = Path(json_path) / "tests" / "backend" / "json_files" / json_file_name


# ## Set JSON reading properties
toolkit_api.load_properties_from_json(json_path)

# ## Launch AEDT
thread_msg = toolkit_api.launch_thread(toolkit_api.launch_aedt)
idle = toolkit_api.wait_to_be_idle()
if not idle:
    print("AEDT not initialized.")
    sys.exit()

# ## Create and update the geometry


# Create an example of a possible core
core = toolkit_api.create_core_geometry()

# Create an example of a possible winding
winding = toolkit_api.create_winding_geometry()

# Modify the diameter of the conductor in the winding properties
winding.properties.layers["layer_1"].conductor.diameter = 5.0

# Generate the new model.
winding = toolkit_api.create_winding_geometry()
