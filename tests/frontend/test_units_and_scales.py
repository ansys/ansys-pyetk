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

"""Unit tests for the units_and_scales module."""

import pytest

pytestmark = [pytest.mark.frontend]

from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import (
    freq_scale,
    freq_units,
    scale_units,
)


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

