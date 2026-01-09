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

"""Unit tests for the splash screen module."""

from pathlib import Path

import pytest

pytestmark = [pytest.mark.frontend]


class TestSplashScreen:
    """Test the splash screen functionality."""

    def test_splash_image_exists(self):
        """Test that the splash image file exists."""
        from ansys.aedt.toolkits.electronic_transformer.ui import splash

        splash_path = Path(splash.__file__).parent / "splash.png"
        assert splash_path.exists(), f"Splash image should exist at {splash_path}"
