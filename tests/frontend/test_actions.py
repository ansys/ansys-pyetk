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

"""Unit tests for the Frontend actions class."""

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.actions import Frontend

pytestmark = [pytest.mark.frontend]


class TestFrontend:
    """Test the Frontend class."""

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_init(self, mock_mkdtemp, mock_parent_init):
        """Test Frontend initialization."""
        mock_mkdtemp.return_value = "/tmp/test_folder"
        mock_parent_init.return_value = None

        frontend = Frontend()

        assert frontend.temp_folder == "/tmp/test_folder"
        assert frontend.properties is not None
        assert frontend.data_manager is not None
        mock_parent_init.assert_called_once()

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.requests.post")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_create_model_success(self, mock_mkdtemp, mock_parent_init, mock_post):
        """Test successful model creation."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_parent_init.return_value = None
        mock_response = Mock()
        mock_response.ok = True
        mock_post.return_value = mock_response

        frontend = Frontend()
        frontend.url = "http://localhost:5000"
        frontend.get_properties = Mock(
            return_value={
                "active_project": "Test_Project",
                "active_design": "Test_Design",
                "project_list": ["Test_Project"],
                "design_list": {"Test_Project": ["Test_Design"]},
            }
        )
        frontend._update_backend_properties = Mock()
        frontend.get_project_name = Mock(side_effect=lambda x: x)

        result = frontend.create_model("Test_Project", "Test_Design")

        assert result is True
        mock_post.assert_called_once_with("http://localhost:5000/create_model")

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.requests.post")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_create_model_failure(self, mock_mkdtemp, mock_parent_init, mock_post):
        """Test failed model creation."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_parent_init.return_value = None
        mock_response = Mock()
        mock_response.ok = False
        mock_post.return_value = mock_response

        frontend = Frontend()
        frontend.url = "http://localhost:5000"
        frontend.get_properties = Mock(
            return_value={
                "active_project": "Test_Project",
                "active_design": "Test_Design",
                "project_list": ["Test_Project"],
                "design_list": {"Test_Project": ["Test_Design"]},
            }
        )
        frontend._update_backend_properties = Mock()
        frontend.get_project_name = Mock(side_effect=lambda x: x)

        result = frontend.create_model("Test_Project", "Test_Design")

        assert result is False

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.generate_unique_project_name")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.requests.post")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_create_model_no_project(self, mock_mkdtemp, mock_parent_init, mock_post, mock_generate):
        """Test model creation with 'No Project' selected."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_parent_init.return_value = None
        mock_generate.return_value = "Unique_Project_Name"
        mock_response = Mock()
        mock_response.ok = True
        mock_post.return_value = mock_response

        frontend = Frontend()
        frontend.url = "http://localhost:5000"
        frontend.get_properties = Mock(
            return_value={
                "active_project": "Test_Project",
                "active_design": "Test_Design",
                "project_list": ["Test_Project"],
                "design_list": {"Test_Project": ["Test_Design"]},
            }
        )
        frontend._update_backend_properties = Mock()
        frontend.get_project_name = Mock(side_effect=lambda x: x)

        result = frontend.create_model("No Project", "Test_Design")

        assert result is True
        mock_generate.assert_called_once()

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.requests.post")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_update_backend_properties(self, mock_mkdtemp, mock_parent_init, mock_post):
        """Test updating backend properties."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_parent_init.return_value = None

        # Create mocks with proper configuration
        mock_set_properties = Mock()
        mock_data_manager = Mock()
        mock_data_manager.create_backend_data.return_value = {
            "core": {"supplier": "TDK"},
            "winding": {"layer_type": "Wound"},
        }

        frontend = Frontend()
        frontend.url = "http://localhost:5000"
        frontend.set_properties = mock_set_properties
        frontend.data_manager = mock_data_manager

        be_props = {"active_project": "Test"}
        frontend._update_backend_properties(be_props)

        # Verify backend data was created and merged
        mock_data_manager.create_backend_data.assert_called_once()
        # set_properties is called once per key in etk_model (2 times: core and winding)
        assert mock_set_properties.call_count == 2
        # Verify the calls were made with the correct keys
        calls = mock_set_properties.call_args_list
        call_dicts = [call[0][0] for call in calls]
        assert {"core": {"supplier": "TDK"}} in call_dicts
        assert {"winding": {"layer_type": "Wound"}} in call_dicts

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.generate_unique_project_name")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.requests.post")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_create_model_with_empty_design_list(self, mock_mkdtemp, mock_parent_init, mock_post, mock_generate):
        """Test model creation when design list is empty."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_parent_init.return_value = None
        mock_generate.return_value = "New_Project"
        mock_response = Mock()
        mock_response.ok = True
        mock_post.return_value = mock_response

        frontend = Frontend()
        frontend.url = "http://localhost:5000"
        frontend.get_properties = Mock(
            return_value={
                "active_project": "Test_Project",
                "active_design": "",
                "project_list": ["Test_Project"],
                "design_list": {},  # Empty design list
            }
        )
        frontend._update_backend_properties = Mock()
        frontend.get_project_name = Mock(side_effect=lambda x: x)

        result = frontend.create_model("Test_Project", "New_Design")

        assert result is True

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_temp_folder_creation(self, mock_mkdtemp, mock_parent_init):
        """Test that temporary folder is created on initialization."""
        expected_folder = "/tmp/unique_folder_123"
        mock_mkdtemp.return_value = expected_folder
        mock_parent_init.return_value = None

        frontend = Frontend()

        assert frontend.temp_folder == expected_folder
        mock_mkdtemp.assert_called_once()

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.actions.FrontendGeneric.__init__")
    @patch("tempfile.mkdtemp")
    def test_properties_and_data_manager_initialization(self, mock_mkdtemp, mock_parent_init):
        """Test that properties and data_manager are properly initialized."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_parent_init.return_value = None

        frontend = Frontend()

        assert frontend.properties is not None
        assert frontend.data_manager is not None
        assert hasattr(frontend.data_manager, "create_backend_data")
