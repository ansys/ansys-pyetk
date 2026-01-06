# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
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
from pathlib import Path
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
        model_create = aedt_common_fixture_class.create_model()
        aedtapp = aedt_common_fixture_class.aedtapp
        if "circuit" in aedtapp.design_list[0].lower():
            circuit_design_name = aedtapp.design_list[0]
        else:
            circuit_design_name = aedtapp.design_list[1]

        cir = aedtapp.desktop_class[[aedtapp.project_name, circuit_design_name]]
        assert len(cir.modeler.schematic.components) == 17
