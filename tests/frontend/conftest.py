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

"""Frontend test configuration and fixtures."""

import json
from unittest.mock import Mock
from unittest.mock import patch

import pytest


@pytest.fixture
def mock_requests():
    """Provide a mock requests module.

    Returns
    -------
        Mock: A mocked requests module with default successful responses.
    """
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        # Configure successful responses by default
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_post.return_value = mock_response
        mock_get.return_value = mock_response

        yield {"post": mock_post, "get": mock_get}


@pytest.fixture
def mock_frontend_generic():
    """Provide a mock FrontendGeneric class.

    Returns
    -------
        Mock: A mocked FrontendGeneric class.
    """
    with patch("ansys.aedt.toolkits.common.ui.actions_generic.FrontendGeneric") as mock:
        instance = Mock()
        instance.url = "http://localhost:5000"
        instance.get_properties.return_value = {
            "active_project": "Test_Project",
            "active_design": "Test_Design",
            "project_list": ["Test_Project"],
            "design_list": {"Test_Project": ["Test_Design"]},
        }
        mock.return_value = instance
        yield mock


@pytest.fixture
def sample_json_data():
    """Provide sample JSON data for testing.

    Returns
    -------
        dict: Sample JSON configuration data.
    """
    return {
        "json_version": "0.1.0",
        "core": {
            "supplier": "TDK",
            "type": "EI",
            "model": "EI30",
            "material": "N87",
            "dimensions": {"A": 30.0, "B": 15.0},
            "airgap": {
                "define_airgap": False,
                "airgap_on_leg": "None",
                "airgap_value": 0.0,
            },
        },
        "winding": {
            "layer_type": "rectangular",
            "layer_spacing": 0.5,
            "top_margin": 1.0,
            "side_margin": 1.0,
            "layers": [],
        },
        "bobbin": {
            "draw_bobbin": False,
            "board_thickness": 1.6,
            "material": "FR4",
        },
        "circuit": {
            "connections": [],
            "side_loads": {},
            "excitation": {
                "type": "voltage",
                "value": 10.0,
            },
        },
        "settings": {
            "analysis_setup": {
                "adaptive_frequency": 100000.0,
                "frequency_sweep": {
                    "frequency_sweep": True,
                    "samples": 50,
                    "scale": "Logarithmic",
                    "start_frequency": 1000.0,
                    "stop_frequency": 1000000.0,
                },
            },
        },
    }


@pytest.fixture
def temp_json_file(tmp_path, sample_json_data):
    """Create a temporary JSON file for testing.

    Args:
        tmp_path: Pytest temporary directory fixture.
        sample_json_data: Sample JSON data fixture.

    Returns
    -------
        Path: Path to the temporary JSON file.
    """
    json_file = tmp_path / "test_config.json"
    with json_file.open("w") as f:
        json.dump(sample_json_data, f)
    return json_file


@pytest.fixture
def mock_logger():
    """Provide a mock logger.

    Returns
    -------
        Mock: A mocked logger instance.
    """
    with patch("ansys.aedt.toolkits.common.ui.logger_handler.logger") as mock:
        yield mock
