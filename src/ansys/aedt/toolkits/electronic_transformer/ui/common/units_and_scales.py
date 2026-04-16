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

freq_scale = {"Hz": 1, "kHz": 1e3, "MHz": 1e6}
freq_units = ["Hz", "kHz", "MHz"]
scale_units = ["Logarithmic", "Linear"]


def auto_freq_unit(freq_hz):
    """Return a frequency value and sensible unit string for a value given in Hz.

    Args:
        freq_hz (float): Frequency in Hz.

    Returns:
        tuple[float, str]: Converted value and unit string (``"Hz"``, ``"kHz"``, or ``"MHz"``).
    """
    if freq_hz >= 1e6:
        return freq_hz / 1e6, "MHz"
    elif freq_hz >= 1e3:
        return freq_hz / 1e3, "kHz"
    else:
        return freq_hz, "Hz"
