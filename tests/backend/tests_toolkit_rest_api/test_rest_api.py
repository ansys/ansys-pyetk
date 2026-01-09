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

import pytest

from tests.backend.conftest import DEFAULT_CONFIG
from tests.backend.tests_toolkit_rest_api.conftest import geometry_properties

pytestmark = [pytest.mark.rest_API]


class TestRestAPI:
    """Class defining a workflow to test rest api toolkit.

    The properties used in the tests are defined in the conftest.py file.
    """

    def test_create_core_geometry(self, client):
        """
        Create core geometry using the REST API and verify the response.

        Send geometry properties to the API and trigger core geometry creation.
        Assert that the response status code is 200, indicating success.
        """
        client.put("/properties", json=geometry_properties)

        response = client.post("/create_core_geometry")
        assert response.status_code == 200

    def test_create_winding_geometry(self, client):
        """
        Create winding geometry using the REST API and verify the response.

        Send geometry properties to the API and trigger winding geometry creation.
        Assert that the response status code is 200, indicating success.
        """
        client.put("/properties", json=geometry_properties)

        response = client.post("/create_winding_geometry")
        assert response.status_code == 200

    def test_create_bobbin_geometry(self, client):
        """
        Create bobbin geometry using the REST API and verify the response.

        Send geometry properties to the API and trigger bobbin geometry creation.
        Assert that the response status code is 200, indicating success.
        """
        client.put("/properties", json=geometry_properties)

        response = client.post("/create_bobbin_geometry")
        assert response.status_code == 200

    @pytest.mark.skipif(DEFAULT_CONFIG["non_graphical"], reason="Not running in non-graphical mode.")
    def test_create_create_model(self, client):
        """
        Create the complete model using the REST API and verify the response.

        Send geometry properties to the API and trigger model creation.
        Assert that the response status code is 200, indicating success.
        """
        client.put("/properties", json=geometry_properties)

        response = client.post("/create_model")
        assert response.status_code == 200
