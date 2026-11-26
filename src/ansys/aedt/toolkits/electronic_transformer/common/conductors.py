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

"""Conductor types shared by the frontend and backend."""

RECTANGULAR_TYPES = ("Rectangular", "Litz Rectangular")
LITZ_TYPES = ("Litz", "Litz Rectangular")

CONDUCTOR_LABELS = {
    "Rectangular": "Rectangular (Solid)",
    "Circular": "Round (Solid)",
    "Litz Rectangular": "Rectangular (Litz)",
    "Litz": "Round (Litz)",
}
