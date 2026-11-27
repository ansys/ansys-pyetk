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
import os
from pathlib import Path
import sys

from ansys.aedt.toolkits.common.ui.logger_handler import logger

from ansys.aedt.toolkits.electronic_transformer.ui.common.utils import extract_sort_key

# data and example directory location
data_dir = Path(__file__).resolve().parents[1] / "data"


def user_data_dir():
    """Return the folder where users of the standalone application can edit the databases.

    Each JSON file in this folder only holds what the user adds or changes. It is merged on
    top of the database shipped with the toolkit, so toolkit updates still reach the user.
    Returns ``None`` when running from source or a pip installation.
    """
    if "PYAEDT_TOOLKIT_CONFIG_DIR" in os.environ:
        return Path(os.environ["PYAEDT_TOOLKIT_CONFIG_DIR"]).absolute() / "data"
    if getattr(sys, "frozen", False):
        base = os.environ.get("APPDATA") or str(Path.home() / ".config")
        return Path(base) / "Ansys" / "Electronic Transformer toolKit" / "data"
    return None


def _merge(base, override):
    """Merge ``override`` into ``base``: objects key by key, any other value replaces."""
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge(base[key], value)
        else:
            base[key] = value
    return base


def load_with_user_overrides(path):
    """Load a shipped JSON database and merge the user's version of the file on top of it.

    Errors in the shipped file are raised as before. A problem with the user's file is
    logged and the shipped data is used, so a bad edit can't stop the toolkit from starting.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    folder = user_data_dir()
    if folder is None:
        return data

    user_file = folder / Path(path).name
    try:
        if not user_file.exists() and "PYAEDT_TOOLKIT_CONFIG_DIR" not in os.environ:
            folder.mkdir(parents=True, exist_ok=True)
            user_file.write_text("{}\n", encoding="utf-8")
        if not user_file.is_file():
            return data
        overrides = json.loads(user_file.read_text(encoding="utf-8-sig"))
        if not isinstance(overrides, dict):
            raise ValueError("the file must contain a JSON object")
        return _merge(data, overrides)
    except (OSError, ValueError, RecursionError) as error:
        logger.error(f"Ignoring {user_file}: {error}")
        return json.loads(Path(path).read_text(encoding="utf-8"))


class CoreDataBase:
    def __init__(self):
        self.cores_database = self.import_core_dimensions()

    def import_core_dimensions(self):
        """Import core dimensions to the ``cores_database`` dictionary."""
        self.core_file_path = data_dir / "core_dimensions.json"

        try:
            self.cores_database = load_with_user_overrides(self.core_file_path)

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
            self.materials_database = load_with_user_overrides(self.mat_file_path)
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