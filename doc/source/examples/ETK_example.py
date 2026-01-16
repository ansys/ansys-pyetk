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

# # Use the ToolkitBackend API to create a transformer model in AEDT
#
# This example demonstrates how to use the ``ToolkitBackend`` class.
# More specifically, it does the following:
# - Initializes the ``ToolkitBackend`` class.
# - Sets common properties like ``non_graphical`` and ``aedt_version``.
# - Defines the path to the JSON file with the transformer properties.
# - Reads the properties from the JSON file.
# - Launches AEDT.
# - Creates the transformer model.

# ## Perform required imports

import importlib.resources
import sys

from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend

# ## Create backend instance
toolkit_api = ToolkitBackend()

# ## Set common properties
toolkit_api.properties.non_graphical = False
toolkit_api.properties.aedt_version = "2025.2"

# ## Define the JSON path
package_root = importlib.resources.files("ansys.aedt.toolkits.electronic_transformer")
json_path = package_root / "tests" / "backend" / "json_files" / "RM_wound_circular.json"

# ## Set JSON reading properties
toolkit_api.read_props_from_json(json_path)

# ## Launch AEDT
thread_msg = toolkit_api.launch_thread(toolkit_api.launch_aedt)
idle = toolkit_api.wait_to_be_idle()
if not idle:
    print("AEDT not initialized.")
    sys.exit()

# ## Create the models
setup = toolkit_api.create_model()
