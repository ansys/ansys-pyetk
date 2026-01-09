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

"""
API Test Configuration Module.

This module contains the configuration and fixture for the pytest-based tests for the API.

The default configuration can be changed by placing a file called local_config.json.
An example of the contents of local_config.json:

{
  "desktop_version": "2025.2",
  "non_graphical": false,
  "use_grpc": true
}

You can enable the API log file in the backend_properties.json.

"""

import json
from pathlib import Path

import pytest

from ansys.aedt.core import generate_unique_project_name
from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend
from ansys.aedt.toolkits.electronic_transformer.backend.models import properties
from ansys.aedt.toolkits.electronic_transformer.backend.run_backend import app
from tests.backend.conftest import DEFAULT_CONFIG
from tests.backend.conftest import read_local_config
from tests.backend.conftest import setup_aedt_settings


def load_json_properties():
    """
    Load and parse a JSON properties file from the test data directory.

    Parameters
    ----------
    json_file_name : str
        Name of the JSON file to load.

    Returns
    -------
    dict
        Parsed JSON data as a dictionary.
    """
    json_file_name = "EI_planar_rectangular.json"
    json_path = Path(__file__).parents[1]
    json_path = Path(json_path) / "json_files" / json_file_name
    with json_path.open() as f:
        return json.load(f)
        pass


@pytest.fixture(scope="function")
def client(logger, common_temp_dir):
    """Initialize toolkit with common API."""
    logger.info("AEDTCommon API initialization")

    aedt_common = ToolkitBackend()
    properties.aedt_version = config["desktop_version"]
    properties.non_graphical = config["non_graphical"]
    properties.use_grpc = config["use_grpc"]
    properties.debug = config["debug"]

    aedt_common.launch_thread(aedt_common.launch_aedt)
    is_aedt_launched = aedt_common.wait_to_be_idle()
    aedt_common.active_project = generate_unique_project_name(common_temp_dir)
    properties.active_project = aedt_common.active_project
    properties.active_design = "No Design"
    aedt_common.connect_design("Maxwell3D")

    if not is_aedt_launched:
        logger.error("AEDT is not launched")

    app.testing = True

    with app.test_client() as test_client:
        new_properties = {
            "aedt_version": properties.aedt_version,
            "non_graphical": properties.non_graphical,
            "use_grpc": properties.use_grpc,
            "debug": properties.debug,
            "active_design": properties.active_design,
            "active_project": properties.active_project,
            "design_list": properties.design_list,
            "project_list": properties.project_list,
            "selected_process": properties.selected_process,
        }
        test_client.put("/properties", json=new_properties)
        yield test_client

        test_client.post("/close_aedt", json={"close_projects": True, "close_on_exit": True})


# Setup config
config = DEFAULT_CONFIG.copy()
local_cfg = read_local_config()
config.update(local_cfg)

# Update AEDT settings
setup_aedt_settings(config)

geometry_properties = load_json_properties()
