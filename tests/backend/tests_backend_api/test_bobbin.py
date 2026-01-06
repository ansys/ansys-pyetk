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

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]


class TestBackendAPI:
    def test_create_bobbin_geometry_plannar(self, aedt_common_fixture_function):
        json_file_name = "EI_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert bobbin.volume > 0 and round(abs(bobbin.volume - 204.8), 4) < vol_limit

    def test_create_bobbin_geometry_circular(self, aedt_common_fixture_function):
        json_file_name = "RM_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert bobbin.volume > 0 and round(abs(bobbin.volume - 1086.5826510971026), 4) < vol_limit
