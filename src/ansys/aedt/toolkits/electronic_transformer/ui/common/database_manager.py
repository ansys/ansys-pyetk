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

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.electronic_transformer.ui.common.utils import extract_sort_key

# data and example directory location
data_dir = Path(__file__).resolve().parents[1] / "data"


class CoreDataBase:
    def __init__(self):
        self.cores_database = self.import_core_dimensions()

    def import_core_dimensions(self):
        """Import core dimensions to the ``cores_database`` dictionary."""
        self.core_file_path = data_dir / "core_dimensions.json"

        try:
            self.cores_database = json.loads(self.core_file_path.read_text())

        except FileNotFoundError:
            msg = "Error: core_dimensions.json missing at " + str(self.core_file_path)
            logger.error(msg)

        self.cores_database = self._format_cores_database(self.cores_database)
        return self.cores_database

    def _format_cores_database(self, obj):
        """Format the cores database by sorting alphabetically.

        Args:
            obj (dict): The cores database.

        Returns
        -------
            dict: The formatted cores database.
        """
        labeled_dimensions_database = self._label_dimensions(obj)
        return self._sort_core_database(labeled_dimensions_database)

    def _sort_core_database(self, data):
        """Sort the core database.

        Args:
            data (dict): The core database.

        Returns
        -------
            dict: The sorted core database.
        """
        sorted_data = {}
        for supplier in sorted(data.keys(), key=str.lower):
            sorted_data[supplier] = {}
            for core_type in sorted(data[supplier].keys(), key=str.lower):
                core_models = data[supplier][core_type]
                sorted_models = dict(
                    sorted(core_models.items(), key=lambda item: extract_sort_key(item[0]), reverse=False)
                )
                sorted_data[supplier][core_type] = sorted_models
        return sorted_data

    def _label_dimensions(self, data):
        """Label the dimensions in the core data.

        Args:
            data (dict or list): The data to label.

        Returns
        -------
            dict: The labeled data.
        """
        if isinstance(data, dict):
            for key in list(data.keys()):
                data[key] = self._label_dimensions(data[key])
            return data
        elif isinstance(data, list):
            return {f"D_{i + 1}": dimension for i, dimension in enumerate(data)}
        else:
            return data


class MaterialDataBase:
    def __init__(self):
        self.core_materials = self.import_material_properties()

    def import_material_properties(self):
        """Import material properties from a JSON file and write to backend properties."""
        self.mat_file_path = data_dir / "material_properties.json"

        try:
            self.materials_database = json.loads(self.mat_file_path.read_text())
            return self.materials_database

        except FileNotFoundError:
            msg = "Error: material_properties.json missing at " + str(self.mat_file_path)
            logger.error(msg)
            self.materials_database = {}
            return self.materials_database

        except json.JSONDecodeError:
            msg = "Error: material_properties.json at " + str(self.mat_file_path) + " contains invalid JSON."
            logger.error(msg)
            self.materials_database = {}
            return self.materials_database


class DataBaseManager(CoreDataBase, MaterialDataBase):
    """Handles the import of core and material database at runtime."""

    def __init__(self):
        CoreDataBase.__init__(self)
        MaterialDataBase.__init__(self)


database_manager = DataBaseManager()
