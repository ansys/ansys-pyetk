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

from pathlib import Path

import pytest

from tests.backend.conftest import DEFAULT_CONFIG

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]


class TestBackendAPI:
    @pytest.mark.skipif(DEFAULT_CONFIG["non_graphical"], reason="Not running in non-graphical mode.")
    def test_circuit(self, aedt_common_fixture_class):
        json_file_name = "EI_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_class.read_props_from_json(json_path)
        _ = aedt_common_fixture_class.create_model()
        aedtapp = aedt_common_fixture_class.aedtapp
        if "circuit" in aedtapp.design_list[0].lower():
            circuit_design_name = aedtapp.design_list[0]
        else:
            circuit_design_name = aedtapp.design_list[1]

        cir = aedtapp.desktop_class[[aedtapp.project_name, circuit_design_name]]
        assert len(cir.modeler.schematic.components) == 17
