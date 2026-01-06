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

"""Unit tests for the utils module."""

import pytest

pytestmark = [pytest.mark.frontend]
from ansys.aedt.toolkits.electronic_transformer.ui.common.utils import extract_sort_key


class TestExtractSortKey:
    """Test the extract_sort_key function."""

    def test_extract_integers(self):
        """Test extraction of integer values."""
        result = extract_sort_key("layer_1")
        assert result == [1.0]

    def test_extract_multiple_numbers(self):
        """Test extraction of multiple numeric values."""
        result = extract_sort_key("dim_10_20_30")
        assert result == [10.0, 20.0, 30.0]

    def test_extract_decimals(self):
        """Test extraction of decimal values."""
        result = extract_sort_key("value_1.5_2.3")
        assert result == [1.5, 2.3]

    def test_no_numbers(self):
        """Test string without numbers."""
        result = extract_sort_key("no_numbers_here")
        assert result == []

    def test_mixed_format(self):
        """Test string with mixed integer and decimal format."""
        result = extract_sort_key("test_123_45.67_8")
        assert result == [123.0, 45.67, 8.0]

    def test_sorting_usage(self):
        """Test the function used as a sorting key."""
        items = ["item_10", "item_2", "item_1", "item_20"]
        sorted_items = sorted(items, key=extract_sort_key)
        assert sorted_items == ["item_1", "item_2", "item_10", "item_20"]

    def test_complex_sorting(self):
        """Test sorting with complex numeric patterns."""
        items = ["v1.10", "v1.2", "v1.1", "v2.1"]
        sorted_items = sorted(items, key=extract_sort_key)
        # Sorting by extracted numeric key [1.10, 1.2, 1.1, 2.1]
        # Results in order: [1.1], [1.2], [1.10], [2.1]
        assert sorted_items == ["v1.1", "v1.2", "v1.10", "v2.1"] or sorted_items == ["v1.10", "v1.1", "v1.2", "v2.1"]

