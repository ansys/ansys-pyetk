# -*- coding: utf-8 -*-
#
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

import json
from pathlib import Path

from jsonschema import validate


class Validation:
    """Manages the validation of the input data."""

    def __init__(self):
        """Initialize and launch the validation component."""
        self.schema = Path(__file__).parents[1] / "schemas" / "pyetk_schema.json"

    def validate_json(self, data):
        """Validate input data from a JSON file.

        Parameters
        ----------
        data : :class:`pathlib.Path`
            Path to the input data in JSON format.
        section : str, optional
            Section of the JSON file to validate. The default is ``None``.
        """
        with self.schema.open("r", encoding="utf-8") as file:
            schema = json.load(file)

        try:
            validate(instance=data, schema=schema)

        except Exception as e:
            raise Exception("Invalid input data:", e)
