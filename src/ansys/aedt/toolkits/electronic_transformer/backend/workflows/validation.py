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
        """
        with self.schema.open("r", encoding="utf-8") as file:
            schema = json.load(file)

        try:
            validate(instance=data, schema=schema)
        except Exception as e:
            raise Exception("Invalid input data:", e)
