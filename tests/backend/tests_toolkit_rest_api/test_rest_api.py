# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
