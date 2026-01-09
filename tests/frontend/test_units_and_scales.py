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

"""Unit tests for the units_and_scales module."""

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import freq_scale
from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import freq_units
from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import scale_units

pytestmark = [pytest.mark.frontend]


class TestFreqScale:
    """Test the freq_scale dictionary."""

    def test_hz_conversion(self):
        """Test Hz conversion factor."""
        assert freq_scale["Hz"] == 1

    def test_khz_conversion(self):
        """Test kHz conversion factor."""
        assert freq_scale["kHz"] == 1e3

    def test_mhz_conversion(self):
        """Test MHz conversion factor."""
        assert freq_scale["MHz"] == 1e6

    def test_all_units_present(self):
        """Test all frequency units are present."""
        assert len(freq_scale) == 3
        assert "Hz" in freq_scale
        assert "kHz" in freq_scale
        assert "MHz" in freq_scale


class TestFreqUnits:
    """Test the freq_units list."""

    def test_units_list(self):
        """Test frequency units list."""
        assert freq_units == ["Hz", "kHz", "MHz"]

    def test_units_count(self):
        """Test number of frequency units."""
        assert len(freq_units) == 3


class TestScaleUnits:
    """Test the scale_units list."""

    def test_scale_types(self):
        """Test scale unit types."""
        assert scale_units == ["Logarithmic", "Linear"]

    def test_scale_count(self):
        """Test number of scale types."""
        assert len(scale_units) == 2

    def test_logarithmic_present(self):
        """Test Logarithmic scale is present."""
        assert "Logarithmic" in scale_units

    def test_linear_present(self):
        """Test Linear scale is present."""
        assert "Linear" in scale_units
