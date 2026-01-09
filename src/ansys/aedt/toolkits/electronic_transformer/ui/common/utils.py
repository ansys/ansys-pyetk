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

import re


def extract_sort_key(key):
    """
    Extract numeric components from a string for natural sorting.

    This function finds all integer and decimal numbers within a string,
    converts them to floats, and returns them as a list. When used as a
    key for sorting, it ensures strings are ordered by their numeric
    value rather than lexicographically.

    Args:
        key (str): The string to extract numbers from.

    Returns
    -------
        list[float]: A list of all numbers found in the string.
    """
    return [float(n) for n in re.findall(r"\d+(?:\.\d+)?", key)]
