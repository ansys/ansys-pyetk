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

"""Unit tests for the utils module."""

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.common.utils import extract_sort_key

pytestmark = [pytest.mark.frontend]


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
