# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Tests for conditional Litz post-processing."""

from types import SimpleNamespace
from unittest.mock import MagicMock
from unittest.mock import call

import pytest

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.post_processing import PostProcessing


@pytest.mark.parametrize(
    ("conductor_types", "expect_stranded_report"),
    [
        (["Rectangular"], False),
        (["Circular"], False),
        (["Litz"], True),
        (["Litz Rectangular"], True),
        (["Rectangular", "Litz"], True),
    ],
)
def test_stranded_loss_report_depends_on_conductor_type(conductor_types, expect_stranded_report):
    aedt = MagicMock()
    winding = SimpleNamespace(
        properties=SimpleNamespace(
            layers={
                str(index): SimpleNamespace(conductor=SimpleNamespace(type=kind))
                for index, kind in enumerate(conductor_types)
            }
        ),
        objects_list=[],
    )
    post = PostProcessing(aedt, SimpleNamespace(objects_list=[]), winding, None, SimpleNamespace(connections={}))

    post.create_post_processing()

    calls = [
        call(plot_name="Loss Table", expressions=["CoreLoss", "SolidLoss"], plot_type="Data Table"),
    ]
    if expect_stranded_report:
        calls.append(
            call(
                plot_name="Stranded Loss",
                expressions=["StrandedLoss", "StrandedLossAC"],
                primary_sweep_variable="Freq",
                plot_type="Rectangular Plot",
            )
        )
    assert aedt.post.create_report.call_args_list == calls


def test_stranded_loss_report_failure_is_reported():
    aedt = MagicMock()
    aedt.post.create_report.side_effect = [MagicMock(), False]
    winding = SimpleNamespace(
        properties=SimpleNamespace(layers={"layer_1": SimpleNamespace(conductor=SimpleNamespace(type="Litz"))}),
        objects_list=[],
    )
    post = PostProcessing(aedt, SimpleNamespace(objects_list=[]), winding, None, SimpleNamespace(connections={}))

    with pytest.raises(RuntimeError, match="Failed to create the stranded loss report"):
        post.create_post_processing()
