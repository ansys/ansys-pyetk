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
Test module for AEDT application properties and circuit functionality.

This module contains unit tests for the AEDT application object properties
including mesh operations, design setups, ports, and circuit creation functionality.
"""

from pathlib import Path

import pytest

from tests.backend.conftest import DEFAULT_CONFIG

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]


@pytest.mark.skipif(DEFAULT_CONFIG["non_graphical"], reason="Not running in non-graphical mode.")
class TestBackendAPI:
    def test_01_create_model(self, aedt_common_fixture_class):
        json_file_name = "RM_wound_circular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_class.read_props_from_json(json_path)

        model = aedt_common_fixture_class.create_model()
        assert model

    def test_02_mesh_operations(self, aedt_common_fixture_class):
        aedt_common_fixture_class.connect_design("Maxwell3D")
        aedtapp = aedt_common_fixture_class.aedtapp

        # Verify mesh operations
        mesh = aedtapp.mesh
        mesh_ops = mesh.meshoperation_names
        mesh_ops_count = len(mesh_ops) if mesh_ops else 0
        assert mesh_ops_count == 2, f"Expected 2 mesh operations, got {mesh_ops_count}: {mesh_ops}"
        assert "Core" in mesh_ops, f"No 'Core' mesh operation found in: {mesh_ops}"
        assert "Layers" in mesh_ops, f"No 'Layers' mesh operation found in: {mesh_ops}"

    def test_03_setup(self, aedt_common_fixture_class):
        aedt_common_fixture_class.connect_design("Maxwell3D")
        aedtapp = aedt_common_fixture_class.aedtapp

        # Verify design setups
        setups = aedtapp.setups
        setups_count = len(setups) if setups else 0
        solution_type = aedtapp.solution_type
        assert setups_count == 1, f"Expected 1 setup, got {setups_count}"

        # Verify first setup properties
        if setups_count > 0:
            assert setups[0].name == "Setup1"
            assert setups[0].properties["Max. Number of Passes"] == 5

        # Verify solution type is AC Magnetic
        assert solution_type == "AC Magnetic", f"Solution type is {solution_type}, expected 'AC Magnetic'"

    def test_05_post_processing(self, aedt_common_fixture_class):
        aedt_common_fixture_class.connect_design("Maxwell3D")
        aedtapp = aedt_common_fixture_class.aedtapp
        assert aedtapp.post.field_plot_names == ["B", "Core_Loss", "J", "Ohmic_Loss"]
        assert aedtapp.post.plots[0].plot_name == "PyETK Leakage_Inductance"
        assert aedtapp.post.plots[0].expressions == ["L(Layer_1,Layer_1)*(1-sqr(CplCoef(Layer_1,Layer_1)))"]
