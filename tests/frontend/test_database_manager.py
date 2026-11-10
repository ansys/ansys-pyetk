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
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import CoreDataBase
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import DataBaseManager
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import MaterialDataBase
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import _merge
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import load_with_user_overrides
from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import user_data_dir

pytestmark = [pytest.mark.frontend]

CONFIG_DIR_ENV = "PYAEDT_TOOLKIT_CONFIG_DIR"
USER_DIR_PARTS = ("Ansys", "ElectronicTransformerToolkit", "data")


@pytest.fixture(autouse=True)
def run_from_source(monkeypatch):
    """Run every test as from source, whatever the developer's environment.

    Without this, a ``PYAEDT_TOOLKIT_CONFIG_DIR`` set on the developer's machine would make
    the loader read real user files during the tests.
    """
    monkeypatch.delenv(CONFIG_DIR_ENV, raising=False)
    monkeypatch.delattr(sys, "frozen", raising=False)


@pytest.fixture
def frozen_app(tmp_path, monkeypatch):
    """Simulate the standalone application with a temporary APPDATA folder.

    Returns
    -------
        Path: The per-user data folder the toolkit is expected to use.
    """
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    return tmp_path.joinpath("appdata", *USER_DIR_PARTS)


@pytest.fixture
def shipped_file(tmp_path):
    """Write a shipped database file to a temporary folder.

    Returns
    -------
        Path: The shipped ``core_dimensions.json``.
    """
    path = tmp_path / "shipped" / "core_dimensions.json"
    path.parent.mkdir()
    path.write_text(json.dumps(SHIPPED_CORES), encoding="utf-8")
    return path


SHIPPED_CORES = {
    "Ferroxcube": {
        "E": {"E10/5/5": [10.0, 5.0, 5.0, 5.0, 2.5, 2.5, 0, 0]},
    }
}


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


class TestUserDataDir:
    """Test the user_data_dir function."""

    def test_none_when_running_from_source(self):
        """Running from source or a pip installation uses only the shipped databases."""
        assert user_data_dir() is None

    def test_appdata_folder_when_frozen(self, frozen_app):
        """The standalone application uses a folder under APPDATA."""
        assert user_data_dir() == frozen_app

    def test_home_fallback_when_appdata_is_not_set(self, tmp_path, monkeypatch):
        """Without APPDATA (for example on Linux), the folder is under ~/.config."""
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.delenv("APPDATA", raising=False)
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        assert user_data_dir() == tmp_path.joinpath(".config", *USER_DIR_PARTS)

    def test_config_dir_env_when_running_from_source(self, tmp_path, monkeypatch):
        """PYAEDT_TOOLKIT_CONFIG_DIR enables overrides even when running from source."""
        monkeypatch.setenv(CONFIG_DIR_ENV, str(tmp_path / "config"))

        assert user_data_dir() == tmp_path / "config" / "data"

    def test_config_dir_env_takes_precedence_over_appdata(self, frozen_app, tmp_path, monkeypatch):
        """PYAEDT_TOOLKIT_CONFIG_DIR wins over the APPDATA folder."""
        monkeypatch.setenv(CONFIG_DIR_ENV, str(tmp_path / "config"))

        assert user_data_dir() == tmp_path / "config" / "data"

    def test_config_dir_env_is_made_absolute(self, tmp_path, monkeypatch):
        """A relative PYAEDT_TOOLKIT_CONFIG_DIR is resolved against the working directory."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv(CONFIG_DIR_ENV, "config")

        result = user_data_dir()

        assert result.is_absolute()
        assert result == tmp_path / "config" / "data"


class TestMerge:
    """Test the _merge function."""

    def test_adds_new_keys(self):
        """Keys only in the override are added."""
        assert _merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_override_wins_for_scalars(self):
        """A value in the override replaces the base value."""
        assert _merge({"a": 1}, {"a": 2}) == {"a": 2}

    def test_nested_dicts_are_merged_key_by_key(self):
        """Nested objects keep the base keys that the override does not mention."""
        base = {"winding": {"Copper": {"conductivity": 5.8e7, "mur": 1, "epsr": 1}}}
        override = {"winding": {"Copper": {"conductivity": 5.6e7}, "Silver": {"mur": 1, "epsr": 1}}}

        result = _merge(base, override)

        assert result["winding"]["Copper"] == {"conductivity": 5.6e7, "mur": 1, "epsr": 1}
        assert result["winding"]["Silver"] == {"mur": 1, "epsr": 1}

    def test_lists_are_replaced_not_merged(self):
        """A list (for example the dimensions of a core model) is replaced as a whole."""
        base = {"E10": [10.0, 5.0, 5.0, 5.0, 2.5, 2.5, 0, 0]}

        assert _merge(base, {"E10": [1, 2, 3, 4, 5, 6, 7, 8]}) == {"E10": [1, 2, 3, 4, 5, 6, 7, 8]}

    def test_non_dict_replaces_dict(self):
        """When the types differ, the override value replaces the base value."""
        assert _merge({"a": {"x": 1}}, {"a": "text"}) == {"a": "text"}

    def test_dict_replaces_non_dict(self):
        """When the base value is not an object, the override object replaces it."""
        assert _merge({"a": 1}, {"a": {"x": 1}}) == {"a": {"x": 1}}

    def test_empty_override_changes_nothing(self):
        """An empty override, like the seeded ``{}`` file, keeps the base unchanged."""
        assert _merge({"a": {"x": 1}}, {}) == {"a": {"x": 1}}

    def test_modifies_and_returns_base(self):
        """The base is merged in place and returned."""
        base = {"a": {"x": 1}}

        result = _merge(base, {"a": {"y": 2}})

        assert result is base
        assert base == {"a": {"x": 1, "y": 2}}


class TestLoadWithUserOverrides:
    """Test the load_with_user_overrides function."""

    def test_shipped_data_when_running_from_source(self, shipped_file):
        """From source, only the shipped file is read."""
        assert load_with_user_overrides(shipped_file) == SHIPPED_CORES

    def test_shipped_file_errors_are_raised(self, tmp_path):
        """Problems with the shipped file are raised as before, so the callers handle them."""
        with pytest.raises(FileNotFoundError):
            load_with_user_overrides(tmp_path / "missing.json")

        broken = tmp_path / "broken.json"
        broken.write_text("{broken", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_with_user_overrides(broken)

    def test_seeds_empty_user_file(self, frozen_app, shipped_file):
        """The standalone application creates an empty user file on first start."""
        result = load_with_user_overrides(shipped_file)

        assert result == SHIPPED_CORES
        assert json.loads((frozen_app / "core_dimensions.json").read_text(encoding="utf-8")) == {}

    def test_never_overwrites_existing_user_file(self, frozen_app, shipped_file):
        """An existing user file is read, never replaced."""
        frozen_app.mkdir(parents=True)
        user_file = frozen_app / "core_dimensions.json"
        user_file.write_text(json.dumps({"Acme": {"E": {"E1": [1, 2, 3, 4, 5, 6, 0, 0]}}}), encoding="utf-8")
        content = user_file.read_text(encoding="utf-8")

        load_with_user_overrides(shipped_file)

        assert user_file.read_text(encoding="utf-8") == content

    def test_user_file_adds_entries(self, frozen_app, shipped_file):
        """User entries are added and shipped entries are kept."""
        frozen_app.mkdir(parents=True)
        (frozen_app / "core_dimensions.json").write_text(
            json.dumps({"Acme": {"ETD": {"ETD29": [29, 22, 9.8, 11, 7.25, 15.8, 0, 0]}}}), encoding="utf-8"
        )

        result = load_with_user_overrides(shipped_file)

        assert result["Acme"]["ETD"]["ETD29"][0] == 29
        assert result["Ferroxcube"] == SHIPPED_CORES["Ferroxcube"]

    def test_user_file_overrides_entries(self, frozen_app, shipped_file):
        """A user entry with the same name as a shipped one replaces it."""
        frozen_app.mkdir(parents=True)
        new_dims = [11.0, 5.0, 5.0, 5.0, 2.5, 2.5, 0, 0]
        (frozen_app / "core_dimensions.json").write_text(
            json.dumps({"Ferroxcube": {"E": {"E10/5/5": new_dims}}}), encoding="utf-8"
        )

        assert load_with_user_overrides(shipped_file)["Ferroxcube"]["E"]["E10/5/5"] == new_dims

    def test_user_file_matched_by_name(self, frozen_app, tmp_path):
        """Each shipped file only picks up the user file with the same name."""
        shipped = tmp_path / "material_properties.json"
        shipped.write_text(json.dumps({"core": {}}), encoding="utf-8")
        frozen_app.mkdir(parents=True)
        (frozen_app / "core_dimensions.json").write_text(json.dumps({"Acme": {}}), encoding="utf-8")

        assert load_with_user_overrides(shipped) == {"core": {}}

    def test_accepts_utf8_bom(self, frozen_app, shipped_file):
        """User files saved with a byte order mark (for example by Notepad) are read."""
        frozen_app.mkdir(parents=True)
        (frozen_app / "core_dimensions.json").write_bytes(b"\xef\xbb\xbf" + json.dumps({"Acme": {}}).encode())

        assert "Acme" in load_with_user_overrides(shipped_file)

    @pytest.mark.parametrize(
        "content",
        [
            "{broken",  # invalid JSON
            "[1, 2, 3]",  # valid JSON, but not an object
            "[" * 100000 + "]" * 100000,  # nested too deeply to parse
        ],
        ids=["invalid_json", "not_an_object", "too_deep"],
    )
    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_bad_user_file_falls_back_to_shipped(self, mock_logger, frozen_app, shipped_file, content):
        """A user file that can't be used is logged and the shipped data is returned."""
        frozen_app.mkdir(parents=True)
        user_file = frozen_app / "core_dimensions.json"
        user_file.write_text(content, encoding="utf-8")

        assert load_with_user_overrides(shipped_file) == SHIPPED_CORES
        mock_logger.error.assert_called_once()
        assert str(user_file) in mock_logger.error.call_args[0][0]

    @patch("ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager.logger")
    def test_unreadable_user_folder_falls_back_to_shipped(self, mock_logger, frozen_app, shipped_file):
        """If the user folder can't be created, the shipped data is returned."""
        frozen_app.parent.mkdir(parents=True)
        frozen_app.write_text("a file where the folder should be", encoding="utf-8")

        assert load_with_user_overrides(shipped_file) == SHIPPED_CORES
        mock_logger.error.assert_called_once()

    def test_config_dir_is_read(self, tmp_path, shipped_file, monkeypatch):
        """Overrides in PYAEDT_TOOLKIT_CONFIG_DIR/data are applied."""
        config_data = tmp_path / "config" / "data"
        config_data.mkdir(parents=True)
        (config_data / "core_dimensions.json").write_text(json.dumps({"Acme": {}}), encoding="utf-8")
        monkeypatch.setenv(CONFIG_DIR_ENV, str(tmp_path / "config"))

        assert "Acme" in load_with_user_overrides(shipped_file)

    def test_config_dir_is_never_written(self, tmp_path, shipped_file, monkeypatch):
        """The PYAEDT_TOOLKIT_CONFIG_DIR folder is read-only for the toolkit: nothing is seeded."""
        monkeypatch.setenv(CONFIG_DIR_ENV, str(tmp_path / "config"))

        assert load_with_user_overrides(shipped_file) == SHIPPED_CORES
        assert not (tmp_path / "config").exists()

    def test_database_manager_uses_overrides(self, frozen_app):
        """DataBaseManager loads the real shipped databases with the user overrides on top."""
        frozen_app.mkdir(parents=True)
        (frozen_app / "core_dimensions.json").write_text(
            json.dumps({"Acme": {"ETD": {"ETD29": [29, 22, 9.8, 11, 7.25, 15.8, 0, 0]}}}), encoding="utf-8"
        )
        (frozen_app / "material_properties.json").write_text(
            json.dumps({"winding": {"Copper": {"conductivity": 5.6e7}}}), encoding="utf-8"
        )

        db = DataBaseManager()

        assert db.cores_database["Acme"]["ETD"]["ETD29"]["D_1"] == 29
        assert "Ferroxcube" in db.cores_database
        assert db.materials_database["winding"]["Copper"]["conductivity"] == 5.6e7
        assert "mur" in db.materials_database["winding"]["Copper"]