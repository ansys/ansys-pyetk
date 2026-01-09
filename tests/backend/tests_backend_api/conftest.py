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

from ansys.aedt.core import generate_unique_project_name
from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend
from ansys.aedt.toolkits.electronic_transformer.backend.models import properties
from tests.backend.conftest import DEFAULT_CONFIG
from tests.backend.conftest import read_local_config
from tests.backend.conftest import setup_aedt_settings

# Setup config
config = DEFAULT_CONFIG.copy()
local_cfg = read_local_config()
config.update(local_cfg)

# Update AEDT settings
setup_aedt_settings(config)


def _initialize_aedt_common(logger, common_temp_dir):
    """Initialize AEDTCommon API."""
    logger.info("AEDTCommon API initialization")

    aedt_common = ToolkitBackend()
    aedt_common.properties.aedt_version = config["desktop_version"]
    aedt_common.properties.non_graphical = config["non_graphical"]
    aedt_common.properties.use_grpc = config["use_grpc"]
    aedt_common.properties.debug = config["debug"]

    aedt_common.launch_thread(aedt_common.launch_aedt)
    is_aedt_launched = aedt_common.wait_to_be_idle()

    aedt_common.active_project = generate_unique_project_name(common_temp_dir)
    properties.active_project = aedt_common.active_project

    properties.active_design = "No Design"
    aedt_common.connect_design("Maxwell3D")

    return aedt_common, is_aedt_launched


def _close_aedt_common(aedt_common):
    """Close AEDTCommon API."""
    aedt_common.release_aedt(True, True)


@pytest.fixture(scope="function")
def aedt_common_fixture_function(logger, common_temp_dir):
    aedt_common, is_aedt_launched = _initialize_aedt_common(logger, common_temp_dir)

    if is_aedt_launched:
        yield aedt_common
    else:
        logger.error("AEDT is not launched")

    _close_aedt_common(aedt_common)


@pytest.fixture(scope="class")
def aedt_common_fixture_class(logger, common_temp_dir):
    aedt_common, is_aedt_launched = _initialize_aedt_common(logger, common_temp_dir)

    if is_aedt_launched:
        yield aedt_common
    else:
        logger.error("AEDT is not launched")

    _close_aedt_common(aedt_common)
