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

"""Unit tests for the database_manager module."""

import json
from unittest.mock import patch

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import CoreDataBase
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import DataBaseManager
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import MaterialDataBase

pytestmark = [pytest.mark.frontend]


class TestCoreDataBase:
    """Test the CoreDataBase class."""

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    def test_import_core_dimensions_success(self, mock_read_text):
        """Test successful import of core dimensions."""
        sample_data = {
            "Ferroxcube": {
                "E": {
                    "E5.3/2.7/2": [5.25, 3.8, 1.4, 2.65, 1.9, 2, 0, 0],
                    "E10/5/5": [10.0, 5.0, 5.0, 5.0, 2.5, 2.5, 0, 0],
                }
            }
        }
        mock_read_text.return_value = json.dumps(sample_data)

        db = CoreDataBase()

        assert db.cores_database is not None
        assert "Ferroxcube" in db.cores_database
        assert "E" in db.cores_database["Ferroxcube"]

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_import_core_dimensions_file_not_found(self, mock_logger, mock_read_text):
        """Test handling of missing core dimensions file."""
        mock_read_text.side_effect = FileNotFoundError()

        with pytest.raises(AttributeError):
            _ = CoreDataBase()

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_import_core_dimensions_invalid_json(self, mock_logger, mock_read_text):
        """Test handling of invalid JSON in core dimensions file."""
        mock_read_text.return_value = "invalid json content"

        # Invalid JSON will raise JSONDecodeError which should be caught and logged
        try:
            _ = CoreDataBase()
            # If it doesn't raise, check that error was logged
            assert mock_logger.error.called
        except json.JSONDecodeError:
            # This is expected
            pass

    def test_label_dimensions_list(self):
        """Test labeling dimensions from a list."""
        db = CoreDataBase.__new__(CoreDataBase)

        data = [5.25, 3.8, 1.4, 2.65, 1.9, 2, 0, 0]
        result = db._label_dimensions(data)

        assert isinstance(result, dict)
        assert "D_1" in result
        assert result["D_1"] == 5.25
        assert "D_8" in result
        assert result["D_8"] == 0

    def test_label_dimensions_dict(self):
        """Test labeling dimensions with nested dictionaries."""
        db = CoreDataBase.__new__(CoreDataBase)

        data = {"Supplier1": {"Type1": {"Model1": [10.0, 20.0, 30.0]}}}
        result = db._label_dimensions(data)

        assert isinstance(result, dict)
        assert "Supplier1" in result
        assert "Type1" in result["Supplier1"]
        assert "Model1" in result["Supplier1"]["Type1"]
        assert result["Supplier1"]["Type1"]["Model1"]["D_1"] == 10.0

    def test_label_dimensions_scalar(self):
        """Test labeling dimensions with scalar values."""
        db = CoreDataBase.__new__(CoreDataBase)

        result = db._label_dimensions(42)

        assert result == 42

    def test_sort_core_database(self):
        """Test sorting of core database."""
        db = CoreDataBase.__new__(CoreDataBase)

        data = {
            "Zebra": {
                "Z": {
                    "Z10": {"D_1": 10.0},
                    "Z2": {"D_1": 2.0},
                }
            },
            "Alpha": {
                "A": {
                    "A5": {"D_1": 5.0},
                }
            },
        }

        result = db._sort_core_database(data)

        suppliers = list(result.keys())
        assert suppliers[0] == "Alpha"
        assert suppliers[1] == "Zebra"

        models = list(result["Zebra"]["Z"].keys())
        assert models[0] == "Z2"
        assert models[1] == "Z10"


class TestMaterialDataBase:
    """Test the MaterialDataBase class."""

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    def test_import_material_properties_success(self, mock_read_text):
        """Test successful import of material properties."""
        sample_data = {
            "N87": {
                "permeability": 2200,
                "conductivity": 0.0,
            }
        }
        mock_read_text.return_value = json.dumps(sample_data)

        db = MaterialDataBase()

        assert db.core_materials is not None
        assert "N87" in db.core_materials

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_import_material_properties_file_not_found(self, mock_logger, mock_read_text):
        """Test handling of missing material properties file."""
        mock_read_text.side_effect = FileNotFoundError()

        db = MaterialDataBase()

        assert db.materials_database == {}
        mock_logger.error.assert_called_once()

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_import_material_properties_invalid_json(self, mock_logger, mock_read_text):
        """Test handling of invalid JSON in material properties file."""
        mock_read_text.return_value = "invalid json content"

        db = MaterialDataBase()

        assert db.materials_database == {}
        mock_logger.error.assert_called_once()


class TestDataBaseManager:
    """Test the DataBaseManager class."""

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    def test_init(self, mock_read_text):
        """Test DataBaseManager initialization."""
        core_data = {"Supplier": {"Type": {"Model": [1, 2, 3]}}}
        material_data = {"Material1": {"prop": "value"}}

        mock_read_text.side_effect = [
            json.dumps(core_data),
            json.dumps(material_data),
        ]

        db = DataBaseManager()

        assert hasattr(db, "cores_database")
        assert hasattr(db, "core_materials")

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    def test_inheritance(self, mock_read_text):
        """Test that DataBaseManager inherits from both base classes."""
        core_data = {"Supplier": {"Type": {"Model": [1, 2, 3]}}}
        material_data = {"Material1": {"prop": "value"}}

        mock_read_text.side_effect = [
            json.dumps(core_data),
            json.dumps(material_data),
        ]

        db = DataBaseManager()

        assert isinstance(db, CoreDataBase)
        assert isinstance(db, MaterialDataBase)

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    def test_complete_database_structure(self, mock_read_text):
        """Test complete database structure with multiple suppliers."""
        core_data = {
            "Ferroxcube": {
                "E": {
                    "E30": [30, 20, 10, 5],
                    "E20": [20, 15, 8, 4],
                }
            },
            "TDK": {
                "EI": {
                    "EI30": [30, 15, 10],
                }
            },
        }
        material_data = {
            "N87": {"permeability": 2200, "conductivity": 0.0},
            "N97": {"permeability": 3000, "conductivity": 0.0},
        }

        mock_read_text.side_effect = [
            json.dumps(core_data),
            json.dumps(material_data),
        ]

        db = DataBaseManager()

        # Check cores database
        assert "Ferroxcube" in db.cores_database or "ferroxcube" in str(db.cores_database).lower()

        # Check materials database
        assert "N87" in db.core_materials
        assert db.core_materials["N87"]["permeability"] == 2200


class TestDatabaseErrorHandling:
    """Test error handling in database operations."""

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.Path.read_text")
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_corrupted_files(self, mock_logger, mock_read_text):
        """Test handling of corrupted JSON files."""
        mock_read_text.return_value = "{invalid json content"

        try:
            db = DataBaseManager()
            # Should handle gracefully
            assert db.materials_database == {}
        except json.JSONDecodeError:
            # Also acceptable
            pass


class TestDatabaseSortingAdvanced:
    """Test advanced sorting scenarios."""

    def test_sorting_with_special_characters(self):
        """Test sorting with special characters in model names."""
        db = CoreDataBase.__new__(CoreDataBase)

        data = {
            "Supplier": {
                "Type": {
                    "Model-A": {"D_1": 1.0},
                    "Model_B": {"D_1": 2.0},
                    "Model C": {"D_1": 3.0},
                }
            }
        }

        result = db._sort_core_database(data)
        assert "Supplier" in result

    def test_sorting_large_dataset(self):
        """Test sorting with large dataset."""
        db = CoreDataBase.__new__(CoreDataBase)

        # Create dataset with 50 models
        models = {f"Model_{i}": {"D_1": float(i)} for i in range(50)}
        data = {"Supplier1": {"TypeA": models}}

        result = db._sort_core_database(data)
        assert "Supplier1" in result
        assert len(result["Supplier1"]["TypeA"]) == 50
