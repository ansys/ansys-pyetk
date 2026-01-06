# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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
from ansys.aedt.core import generate_unique_project_name
from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend
from tests.backend.conftest import read_local_config, setup_aedt_settings, DEFAULT_CONFIG, PROJECT_NAME
from ansys.aedt.toolkits.electronic_transformer.backend.models import properties

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
