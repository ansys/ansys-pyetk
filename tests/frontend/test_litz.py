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

"""Tests for Litz input and material assignment."""

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QTreeWidget
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtWidgets import QWidget
import pytest

from ansys.aedt.toolkits.electronic_transformer.backend.models import Bobbin
from ansys.aedt.toolkits.electronic_transformer.backend.models import Conductor
from ansys.aedt.toolkits.electronic_transformer.backend.models import Core
from ansys.aedt.toolkits.electronic_transformer.backend.models import Layer
from ansys.aedt.toolkits.electronic_transformer.backend.models import Material
from ansys.aedt.toolkits.electronic_transformer.backend.models import Settings
from ansys.aedt.toolkits.electronic_transformer.backend.models import Winding as WindingProperties
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding import Winding
from ansys.aedt.toolkits.electronic_transformer.common.conductors import CONDUCTOR_LABELS
from ansys.aedt.toolkits.electronic_transformer.common.validation import Validation
from ansys.aedt.toolkits.electronic_transformer.ui.common.data_manager import DataManager
from ansys.aedt.toolkits.electronic_transformer.ui.models import GUIProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import Properties
from ansys.aedt.toolkits.electronic_transformer.ui.windows.main import main_menu
from ansys.aedt.toolkits.electronic_transformer.ui.windows.main.main_menu import GeometryMenu
from ansys.aedt.toolkits.electronic_transformer.ui.windows.main.main_menu import WindingTreeDelegate
from ansys.aedt.toolkits.electronic_transformer.ui.windows.main.main_page import Ui_Geometry


@pytest.fixture
def litz_data():
    path = Path(__file__).parents[1] / "backend" / "json_files" / "RM_wound_circular.json"
    data = json.loads(path.read_text())
    conductor = data["winding"]["layers"]["layer_1"]["conductor"]
    conductor.update(type="Litz", strand_diameter=0.1, strand_number=100)
    return data


@pytest.mark.parametrize(
    ("conductor_type", "dimensions"),
    [
        ("Rectangular", {"width": 1.5, "height": 0.8}),
        ("Circular", {"diameter": 1.5}),
        ("Litz Rectangular", {"width": 1.5, "height": 0.8, "strand_diameter": 0.1, "strand_number": 40}),
        ("Litz", {"diameter": 1.5, "strand_diameter": 0.1, "strand_number": 40}),
    ],
)
def test_open_and_save_dialog_round_trip(conductor_type, dimensions, litz_data, tmp_path, monkeypatch):
    app = QApplication.instance() or QApplication([])
    manager = DataManager()
    manager.gui_properties = GUIProperties()
    manager.properties = Properties()
    monkeypatch.setattr(main_menu, "data_manager", manager)
    monkeypatch.setattr(main_menu, "gui_properties", manager.gui_properties)
    monkeypatch.setattr(main_menu, "fe_properties", manager.properties)

    pages = QStackedWidget()
    columns = QStackedWidget()
    ui = MagicMock()
    ui.load_pages.pages = pages
    ui.left_column.menus.menus = columns

    def add_page(page_type):
        widget = QWidget()
        page_type().setupUi(widget)
        return pages.addWidget(widget)

    ui.add_page.side_effect = add_page
    window = MagicMock()
    window.ui = ui
    menu = GeometryMenu(window)
    menu.build_combo.setCurrentText("Planar")

    conductor = litz_data["winding"]["layers"]["layer_1"]["conductor"]
    for key in ("diameter", "width", "height", "strand_diameter", "strand_number"):
        conductor.pop(key, None)
    conductor.update(type=conductor_type, **dimensions)
    if conductor_type in ("Litz", "Litz Rectangular"):
        second_conductor = copy.deepcopy(conductor)
        second_conductor.update(material="Aluminium", strand_diameter=0.2, strand_number=20)
        if conductor_type == "Litz":
            second_conductor["diameter"] = 1.6
        else:
            second_conductor.update(width=1.6, height=1.2)
        litz_data["winding"]["layers"]["layer_2"] = copy.deepcopy(litz_data["winding"]["layers"]["layer_1"])
        litz_data["winding"]["layers"]["layer_2"]["conductor"] = second_conductor
        litz_data["circuit"]["connections"] = {"1": {"1": "Layer"}, "2": {"2": "Layer"}}
        litz_data["circuit"]["side_loads"].append(1e-6)
        litz_data["materials"]["Aluminium"] = {"conductivity": 38e6, "mur": 1, "epsr": 1}
    Validation().validate_json(litz_data)
    source = tmp_path / "input.json"
    source.write_text(json.dumps(litz_data))
    target = tmp_path / "saved"
    saved_target = target.with_suffix(".json")
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda **kwargs: (str(source), ""))
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda **kwargs: (str(target), ""))

    menu.example_button_clicked()
    assert menu.cond_type.currentText() == CONDUCTOR_LABELS[conductor_type]
    assert menu.example_name.text() == source.name
    assert menu.conductor_dimension.text() == str(dimensions.get("width", dimensions.get("diameter")))
    if "height" in dimensions:
        assert menu.conductor_height.text() == str(dimensions["height"])
    if "strand_diameter" in dimensions:
        assert menu.strand_diameter.text() == str(dimensions["strand_diameter"])
        assert menu.strand_number.text() == str(dimensions["strand_number"])
    menu.save_button_clicked()
    assert saved_target.is_file()
    saved = json.loads(saved_target.read_text())
    Validation().validate_json(saved)
    saved_conductor = saved["winding"]["layers"]["layer_1"]["conductor"]
    assert saved_conductor["type"] == conductor_type
    for key, value in dimensions.items():
        assert saved_conductor[key] == value
    if conductor_type in ("Litz", "Litz Rectangular"):
        saved_second_conductor = saved["winding"]["layers"]["layer_2"]["conductor"]
        assert saved_second_conductor["material"] == "Aluminium"
        assert saved_second_conductor["strand_diameter"] == 0.2
        assert saved_second_conductor["strand_number"] == 20
    assert {
        key for key in ("diameter", "width", "height", "strand_diameter", "strand_number") if key in saved_conductor
    } == set(dimensions)
    assert menu.example_name.text() == saved_target.name
    menu.cond_type.setCurrentText(CONDUCTOR_LABELS["Circular" if conductor_type != "Circular" else "Rectangular"])
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda **kwargs: (str(saved_target), ""))
    menu.example_button_clicked()
    assert menu.cond_type.currentText() == CONDUCTOR_LABELS[conductor_type]
    assert menu.conductor_dimension.text() == str(dimensions.get("width", dimensions.get("diameter")))
    if conductor_type in ("Litz", "Litz Rectangular"):
        second_side = menu.winding_tree_widget.topLevelItem(1)
        menu.winding_tree_widget.setCurrentItem(second_side)
        assert menu.cond_material_label.text() == "Side 2 Conductor Material"
        assert menu.cond_material.currentText() == "Aluminium"
    if "strand_number" in dimensions:
        expected_strand_count = 20 if conductor_type in ("Litz", "Litz Rectangular") else dimensions["strand_number"]
        assert menu.strand_number.text() == str(expected_strand_count)
    pages.close()
    columns.close()
    assert app is not None


@pytest.mark.parametrize(
    ("conductor_type", "dimensions", "missing_field"),
    [
        ("Rectangular", {"width": 1.5, "height": 0.8}, "height"),
        ("Circular", {"diameter": 1.5}, "diameter"),
        ("Litz Rectangular", {"width": 1.5, "height": 0.8, "strand_diameter": 0.1, "strand_number": 40}, "width"),
        ("Litz", {"diameter": 1.5, "strand_diameter": 0.1, "strand_number": 40}, "strand_number"),
    ],
)
def test_conductor_schema_requires_type_specific_fields(litz_data, conductor_type, dimensions, missing_field):
    conductor = litz_data["winding"]["layers"]["layer_1"]["conductor"]
    for key in ("diameter", "width", "height", "strand_diameter", "strand_number"):
        conductor.pop(key, None)
    conductor.update(type=conductor_type, **dimensions)
    Validation().validate_json(litz_data)
    del conductor[missing_field]
    with pytest.raises(Exception, match="Invalid input data"):
        Validation().validate_json(litz_data)


def test_solid_conductor_accepts_default_strand_values_from_backend(litz_data):
    conductor = litz_data["winding"]["layers"]["layer_1"]["conductor"]
    conductor.update(type="Circular", diameter=1.0, strand_diameter=0, strand_number=0)
    Validation().validate_json(litz_data)


def test_rectangular_import_uses_type_when_diameter_is_also_present(litz_data):
    conductor = litz_data["winding"]["layers"]["layer_1"]["conductor"]
    conductor.update(type="Litz Rectangular", width=1.5, height=0.8, diameter=1.0, strand_number=40)
    Validation().validate_json(litz_data)
    manager = DataManager()
    manager.gui_properties = GUIProperties()
    manager.gui_properties.winding.layer_type = "Wound"
    manager._set_layers_from_json(litz_data["winding"]["layers"])
    layer = manager.gui_properties.winding.layers_definition["layer_1"]
    assert layer["conductor_width"] == 1.5
    assert layer["conductor_height"] == 0.8
    assert "conductor_diameter" not in layer


def test_litz_schema_and_winding_consistency(litz_data):
    validator = Validation()
    validator.validate_json(litz_data)
    data = copy.deepcopy(litz_data)
    data["winding"]["layers"]["layer_2"] = copy.deepcopy(data["winding"]["layers"]["layer_1"])
    data["winding"]["layers"]["layer_2"]["conductor"]["strand_number"] = 50
    data["circuit"]["connections"]["1"] = {"S1": {"1": "Layer", "2": "Layer"}}
    with pytest.raises(ValueError, match="same Litz"):
        validator.validate_json(data)
    data["circuit"]["connections"] = {"1": {"1": "Layer"}, "2": {"2": "Layer"}}
    validator.validate_json(data)
    data["winding"]["layers"]["layer_2"]["conductor"]["strand_diameter"] = 10.0
    with pytest.raises(ValueError, match="strand area"):
        validator.validate_json(data)
    data["json_version"] = "0.2"
    with pytest.raises(ValueError, match="Invalid input data"):
        validator.validate_json(data)


def test_planar_design_allows_only_rectangular_litz(litz_data):
    data = copy.deepcopy(litz_data)
    data["winding"]["layer_type"] = "Planar"
    with pytest.raises(ValueError, match="rectangular Litz for a planar"):
        Validation().validate_json(data)
    conductor = data["winding"]["layers"]["layer_1"]["conductor"]
    conductor.pop("diameter")
    conductor.update(type="Litz Rectangular", width=1.5, height=0.8)
    Validation().validate_json(data)


def test_planar_build_offers_only_rectangular_conductor_types():
    app = QApplication.instance() or QApplication([])
    menu = GeometryMenu.__new__(GeometryMenu)
    menu.cond_type = QComboBox()
    menu.cond_type.addItems(CONDUCTOR_LABELS.values())
    menu.cond_type.setCurrentText(CONDUCTOR_LABELS["Litz"])
    menu._conductor_type_changed = MagicMock()

    def listed_types():
        labels = [menu.cond_type.itemText(i) for i in range(menu.cond_type.count())]
        return [kind for kind, label in CONDUCTOR_LABELS.items() if label in labels]

    menu._restrict_conductor_types(True)
    assert listed_types() == ["Rectangular", "Litz Rectangular"]
    assert menu._conductor_type() == "Rectangular"
    menu._conductor_type_changed.assert_called_once()
    menu.cond_type.setCurrentText(CONDUCTOR_LABELS["Litz Rectangular"])
    menu._restrict_conductor_types(True)
    assert menu._conductor_type() == "Litz Rectangular"
    menu._restrict_conductor_types(False)
    assert listed_types() == list(CONDUCTOR_LABELS)
    assert menu._conductor_type() == "Litz Rectangular"
    assert app is not None


def test_litz_layers_on_side_must_share_material(litz_data):
    data = copy.deepcopy(litz_data)
    data["winding"]["layers"]["layer_2"] = copy.deepcopy(data["winding"]["layers"]["layer_1"])
    data["winding"]["layers"]["layer_2"]["conductor"]["material"] = "Aluminium"
    data["circuit"]["connections"]["1"] = {"S1": {"1": "Layer", "2": "Layer"}}
    with pytest.raises(ValueError, match="same Litz material"):
        Validation().validate_json(data)


@pytest.mark.parametrize(
    ("field", "value"),
    [("diameter", 0), ("strand_diameter", 0), ("strand_number", 1), ("strand_number", 1.5)],
)
def test_invalid_litz_input_is_reported_on_import(litz_data, tmp_path, field, value):
    litz_data["winding"]["layers"]["layer_1"]["conductor"][field] = value
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(litz_data))
    manager = DataManager()
    manager.gui_properties = GUIProperties()
    message, valid = manager._import_data_from_json(path)
    assert not valid
    assert "Invalid Litz configuration" in message


def test_litz_missing_connected_layer_reports_error(litz_data):
    litz_data["circuit"]["connections"] = {"1": {"S1": {"3": "Layer"}}}
    with pytest.raises(ValueError, match=r"unknown layer\(s\) 3"):
        Validation().validate_json(litz_data)


def test_nested_litz_connections_are_flattened(litz_data):
    litz_data["circuit"]["connections"] = {"1": {"S1": {"P2": {"1": "Layer"}}}}
    Validation().validate_json(litz_data)
    assert DataManager()._flatten_connections(litz_data["circuit"]["connections"]) == {"1": ["1"]}


def test_flatten_connections_preserves_existing_direct_entries():
    assert DataManager()._flatten_connections({"1": {"1": "legacy"}}) == {"1": ["1"]}


@pytest.mark.parametrize("data", [[], {"winding": []}, {"winding": {"layers": []}}])
def test_invalid_non_litz_schema_preserves_original_error(data):
    with pytest.raises(Exception, match="Invalid input data"):
        Validation().validate_json(data)


def test_litz_unconnected_or_duplicated_layer_reports_error(litz_data):
    litz_data["circuit"]["connections"] = {}
    with pytest.raises(ValueError, match="not connected"):
        Validation().validate_json(litz_data)
    litz_data["circuit"]["connections"] = {"1": {"1": "Layer"}, "2": {"1": "Layer"}}
    with pytest.raises(ValueError, match="connected more than once"):
        Validation().validate_json(litz_data)


def test_invalid_litz_save_reports_error_without_writing(litz_data, tmp_path):
    litz_data["winding"]["layers"]["layer_1"]["conductor"]["strand_diameter"] = 0
    menu = GeometryMenu.__new__(GeometryMenu)
    menu._read_ui_data = MagicMock()
    menu.cond_type = MagicMock()
    menu.cond_type.currentText.return_value = "Litz"
    menu.data_manager = MagicMock()
    menu.data_manager.create_backend_data.return_value = litz_data
    menu.ui = MagicMock()
    path = tmp_path / "invalid.json"
    assert not menu._save_model(path)
    assert not path.exists()
    assert "Invalid Litz configuration" in menu.ui.update_logger.call_args.args[0]


def test_litz_layer_round_trip(litz_data):
    manager = DataManager()
    manager.gui_properties = GUIProperties()
    manager.gui_properties.winding.layer_type = "Wound"
    manager._set_layers_from_json(litz_data["winding"]["layers"])
    layers = manager.gui_properties.winding.layers_definition
    assert layers["layer_1"]["conductor_diameter"] == 2.05
    assert layers["layer_1"]["strand_diameter"] == 0.1
    assert layers["layer_1"]["strand_number"] == 100
    restored = manager._create_layers_for_backend(layers)["layer_1"]["conductor"]
    assert restored["type"] == "Litz"
    assert restored["diameter"] == 2.05
    assert restored["strand_diameter"] == 0.1
    assert restored["strand_number"] == 100


def test_rectangular_litz_round_trip_and_validation(litz_data, tmp_path):
    conductor = litz_data["winding"]["layers"]["layer_1"]["conductor"]
    conductor.pop("diameter")
    conductor.update(type="Litz Rectangular", width=2.0, height=1.0, strand_diameter=0.1, strand_number=100)
    Validation().validate_json(litz_data)
    manager = DataManager()
    manager.gui_properties = GUIProperties()
    manager.gui_properties.winding.layer_type = "Wound"
    manager._set_layers_from_json(litz_data["winding"]["layers"])
    restored = manager._create_layers_for_backend(manager.gui_properties.winding.layers_definition)["layer_1"][
        "conductor"
    ]
    assert restored["type"] == "Litz Rectangular"
    assert (restored["width"], restored["height"], restored["strand_diameter"], restored["strand_number"]) == (
        2.0,
        1.0,
        0.1,
        100,
    )
    path = tmp_path / "rectangular_litz.json"
    path.write_text(json.dumps(litz_data))
    manager.properties = Properties()
    message, valid = manager._import_data_from_json(path)
    assert valid, message
    manager._update_frontend_properties()
    output = manager.create_backend_data()
    Validation().validate_json(output)
    assert output["json_version"] == manager.supported_json
    assert output["winding"]["layers"]["layer_1"]["conductor"]["type"] == "Litz Rectangular"
    conductor["strand_number"] = 300
    with pytest.raises(ValueError, match="strand area"):
        Validation().validate_json(litz_data)
    conductor.update(width=10, height=0.05, strand_number=2)
    with pytest.raises(ValueError, match="strand diameter exceeds"):
        Validation().validate_json(litz_data)


def test_rectangular_litz_uses_rectangular_profile_and_stranded_excitation():
    from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import CoreCrossSection

    app = MagicMock()
    layers = {
        "layer_1": Layer(
            conductor=Conductor(
                type="Litz Rectangular",
                width=2.0,
                height=1.0,
                strand_diameter=0.1,
                strand_number=50,
            )
        )
    }
    winding = Winding("Windings", app, WindingProperties(layers=layers), Core(), Settings(), Bobbin())
    winding.core_cross_section = CoreCrossSection.circular
    winding._Winding__create_sweep_path_circular = MagicMock(return_value="path")
    winding._Winding__create_single_turn(10, 10, 0, 1, 1, profile_width=2, profile_height=1)
    app.modeler.create_rectangle.assert_called_once()
    app.modeler.create_circle.assert_not_called()
    winding.create_excitations()
    assert app.assign_winding.call_args.kwargs["is_solid"] is False


def test_litz_multi_side_json_round_trip(litz_data, tmp_path):
    second_layer = copy.deepcopy(litz_data["winding"]["layers"]["layer_1"])
    second_layer["conductor"].update(material="Aluminium", diameter=1.5, strand_diameter=0.2, strand_number=20)
    litz_data["winding"]["layers"]["layer_2"] = second_layer
    litz_data["materials"]["Aluminium"] = {"conductivity": 38e6, "mur": 1, "epsr": 1}
    litz_data["circuit"]["connections"] = {"1": {"1": "Layer"}, "2": {"2": "Layer"}}
    litz_data["circuit"]["side_loads"].append(1e-6)
    path = tmp_path / "input.json"
    path.write_text(json.dumps(litz_data))
    manager = DataManager()
    manager.gui_properties = GUIProperties()
    manager.properties = Properties()
    message, valid = manager._import_data_from_json(path)
    assert valid, message
    assert manager.gui_properties.winding.layer_side_definition == {"1": ["1"], "2": ["2"]}
    manager._update_frontend_properties()
    output = manager.create_backend_data()
    Validation().validate_json(output)
    assert output["materials"]["Aluminium"]["conductivity"] == 38e6
    for layer in ("layer_1", "layer_2"):
        expected = litz_data["winding"]["layers"][layer]["conductor"]
        actual = output["winding"]["layers"][layer]["conductor"]
        for field in ("material", "diameter", "strand_diameter", "strand_number"):
            assert actual[field] == expected[field]


@pytest.mark.parametrize("conductor_type", ["Litz", "Litz Rectangular"])
def test_litz_assigns_materials_and_stranded_excitations(conductor_type):
    app = MagicMock()
    materials = []

    def add_material(name):
        mat = SimpleNamespace(name=name)
        materials.append(mat)
        return mat

    app.materials.add_material.side_effect = add_material
    layers = {
        "layer_1": Layer(conductor=Conductor(type=conductor_type, diameter=2, strand_diameter=0.1, strand_number=50)),
        "layer_2": Layer(conductor=Conductor(type=conductor_type, diameter=2, strand_diameter=0.1, strand_number=50)),
        "layer_3": Layer(conductor=Conductor(type=conductor_type, diameter=2, strand_diameter=0.2, strand_number=20)),
    }
    winding = Winding("Windings", app, WindingProperties(layers=layers), Core(), Settings(), Bobbin())
    objects = [SimpleNamespace(name="Layer1"), SimpleNamespace(name="Layer2_1"), SimpleNamespace(name="Layer3")]
    winding.objects_list_append(objects)
    connections = {"1": {"S1": {"1": "Layer", "2": "Layer"}}, "2": {"3": "Layer"}}
    winding.set_material(Material(name="Copper", conductivity=58e6, mur=1), connections)
    assert [(m.stacking_type, m.wire_type, m.wire_diameter, m.strand_number) for m in materials] == [
        ("Litz Wire", "Round", "0.1mm", 50),
        ("Litz Wire", "Round", "0.2mm", 20),
    ]
    assert app.assign_material.call_count == 2
    app.assign_material.assert_any_call(assignment=objects[:2], material=materials[0].name)
    app.assign_material.assert_any_call(assignment=objects[2:], material=materials[1].name)
    app.eddy_effects_on.assert_called_once_with(assignment=["Layer1", "Layer2_1", "Layer3"], enable_eddy_effects=False)
    winding.create_excitations()
    assert all(call.kwargs["is_solid"] is False for call in app.assign_winding.call_args_list)


@pytest.mark.parametrize(
    ("connections", "message"),
    [
        (None, "requires side connections"),
        ({"1": {"2": "Layer"}}, "unknown winding"),
        ({"1": {"1": "Layer"}, "2": {"1": "Layer"}}, "connected more than once"),
        ({"1": {"S1": {}}}, "no winding layers"),
    ],
)
def test_litz_material_assignment_rejects_invalid_sides(connections, message):
    app = MagicMock()
    layers = {"layer_1": Layer(conductor=Conductor(type="Litz", diameter=2, strand_diameter=0.1, strand_number=50))}
    winding = Winding("Windings", app, WindingProperties(layers=layers), Core(), Settings(), Bobbin())
    winding.objects_list_append([SimpleNamespace(name="Layer1")])
    with pytest.raises(ValueError, match=message):
        winding.set_material(Material(name="Copper", conductivity=58e6, mur=1), connections)
    app.materials.add_material.assert_not_called()


def test_litz_material_assignment_uses_each_side_base_material():
    app = MagicMock()
    created_materials = []

    def add_material(name):
        material = SimpleNamespace(name=name)
        created_materials.append(material)
        return material

    app.materials.add_material.side_effect = add_material
    layers = {
        "layer_1": Layer(conductor=Conductor(type="Litz", material="Copper", strand_diameter=0.1, strand_number=50)),
        "layer_2": Layer(conductor=Conductor(type="Litz", material="Aluminum", strand_diameter=0.1, strand_number=50)),
    }
    winding = Winding("Windings", app, WindingProperties(layers=layers), Core(), Settings(), Bobbin())
    winding.objects_list_append([SimpleNamespace(name="Layer1"), SimpleNamespace(name="Layer2")])
    winding.set_material(
        Material(name="Copper", conductivity=58e6, mur=1),
        {"1": {"1": "Layer"}, "2": {"2": "Layer"}},
        {
            "Copper": Material(name="Copper", conductivity=58e6, mur=1),
            "Aluminum": Material(name="Aluminum", conductivity=35e6, mur=1),
        },
    )
    assert created_materials[0].name.lower().startswith("copper_pyetk_litz_side_1")
    assert created_materials[1].name.lower().startswith("aluminum_pyetk_litz_side_2")
    assert [material.conductivity for material in created_materials] == [58e6, 35e6]


def test_new_layers_use_side_dimensions_without_per_layer_copies():
    app = QApplication.instance() or QApplication([])
    menu = GeometryMenu.__new__(GeometryMenu)
    menu.gui_properties = GUIProperties()
    menu.winding_tree_widget = QTreeWidget()
    menu.connections_tree_widget = QTreeWidget()
    menu.cond_type = QComboBox()
    menu.cond_type.addItems(["Rectangular", "Circular", "Litz", "Litz Rectangular"])
    menu.cond_type.setCurrentText("Litz")
    menu.conductor_segments = QLineEdit("8")
    menu._turn_number = 15
    menu._insulation_thickness = 0.05
    menu._conductor_diameter = 1.0
    menu._segments_number = 8
    menu._commit_connection_to_UserData = MagicMock()
    menu.update_connections_def = MagicMock()
    menu._display_connection_scheme = MagicMock()
    side = QTreeWidgetItem(["Side1"])
    side.setData(
        0,
        Qt.UserRole,
        {
            "type": "Winding",
            "side": 1,
            "conductor": {"width": 0.4, "height": 0.1, "diameter": 1.5},
            "strand_diameter": 0.2,
            "strand_number": 20,
        },
    )
    menu.winding_tree_widget.addTopLevelItem(side)
    menu.winding_tree_widget.setCurrentItem(side)
    menu._add_layer()
    menu._add_layer()
    layers = menu._update_layers_definition()
    assert len(layers) == 2
    assert all(layer["conductor_diameter"] == 1.5 and layer["strand_number"] == 20 for layer in layers.values())
    assert all("conductor" not in side.child(index).data(0, Qt.UserRole) for index in range(2))
    assert app is not None


def test_litz_winding_table_preserves_side_settings():
    app = QApplication.instance() or QApplication([])
    menu = GeometryMenu.__new__(GeometryMenu)
    menu.gui_properties = GUIProperties()
    menu.gui_properties.winding.layer_type = "Wound"
    menu.cond_type = QComboBox()
    menu.cond_type.addItems(["Rectangular", "Circular", "Litz", "Litz Rectangular"])
    menu.cond_type.setCurrentText("Litz")
    menu.build_combo = QComboBox()
    menu.build_combo.addItem("Wound")
    menu.winding_tree_widget = QTreeWidget()
    menu.winding_tree_widget.setColumnCount(5)
    menu.winding_tree_widget.setItemDelegate(WindingTreeDelegate(menu.winding_tree_widget))
    menu.conductor_segments = QLineEdit("8")
    menu.side_load_label = QLabel()
    menu.side_load = QLineEdit()
    menu.conductor_dimension_label = QLabel()
    menu.conductor_dimension = QLineEdit()
    menu.conductor_height = QLineEdit()
    menu.strand_diameter_label = QLabel()
    menu.strand_diameter = QLineEdit()
    menu.strand_number_label = QLabel()
    menu.strand_number = QLineEdit()
    menu.cond_material = QComboBox()
    menu.cond_material.addItems(["Copper", "Aluminium"])
    menu.cond_material_label = QLabel()
    menu.cond_material.currentTextChanged.connect(menu._conductor_material_changed)
    menu.ui = MagicMock()
    menu._default_side_load = 1e-6
    menu._turn_number = 15
    menu._conductor_diameter = 1.0
    menu._conductor_width = 0.4
    menu._conductor_height = 0.1
    menu._insulation_thickness = 0.05
    menu._segments_number = 8
    layers = {
        "layer_1": {
            "conductor_diameter": 1.0,
            "strand_diameter": 0.1,
            "strand_number": 10,
            "conductor_material": "Copper",
        },
        "layer_2": {
            "conductor_diameter": 1.2,
            "strand_diameter": 0.1,
            "strand_number": 10,
            "conductor_material": "Copper",
        },
        "layer_3": {
            "conductor_diameter": 1.5,
            "strand_diameter": 0.2,
            "strand_number": 20,
            "conductor_material": "Aluminium",
        },
    }
    menu._populate_layers_from_definition(layers, {"1": ["1", "2"], "2": ["3"]}, [1.0, 2.0])
    menu._conductor_type_changed()
    first_side = menu.winding_tree_widget.topLevelItem(0)
    second_side = menu.winding_tree_widget.topLevelItem(1)
    menu.winding_tree_widget.setCurrentItem(first_side)
    menu._show_conductor_dimensions()
    assert menu._update_layers_definition()["layer_2"]["conductor_diameter"] == 1.0
    assert menu.cond_material_label.text() == "Side 1 Conductor Material"
    assert menu.cond_material.currentText() == "Copper"
    menu.cond_material.setCurrentText("Aluminium")
    assert menu._update_layers_definition()["layer_1"]["conductor_material"] == "Aluminium"
    assert menu._update_layers_definition()["layer_2"]["conductor_material"] == "Aluminium"
    menu.winding_tree_widget.setCurrentItem(second_side)
    menu._show_conductor_dimensions()
    menu.cond_material.setCurrentText("Copper")
    output = menu._update_layers_definition()
    assert output["layer_1"]["conductor_material"] == output["layer_2"]["conductor_material"] == "Aluminium"
    assert output["layer_3"]["conductor_material"] == "Copper"
    menu.cond_material.setCurrentText("Aluminium")
    menu.winding_tree_widget.setCurrentItem(first_side.child(0))
    menu._show_conductor_dimensions()
    assert menu.side_load_label.text() == "Side 1 Load (ohm)"
    assert menu.side_load.text() == "1.0"
    menu.side_load.setText("3.5")
    menu._side_load_changed()
    assert menu.gui_properties.winding.side_loads == [3.5, 2.0]
    menu.side_load.setText("invalid")
    menu._side_load_changed()
    assert menu.side_load.text() == "3.5"
    menu.ui.update_logger.assert_any_call("Side load must be a finite number.")
    assert menu.conductor_dimension.text() == "1.0"
    assert menu.strand_diameter.text() == "0.1"
    assert menu.strand_number.text() == "10"
    menu.strand_diameter.setText("0.12")
    menu.strand_number.setText("15")
    menu._strand_settings_changed()
    menu.conductor_dimension.setText("1.3")
    menu._conductor_dimensions_changed()
    output = menu._update_layers_definition()
    assert output["layer_1"]["conductor_diameter"] == output["layer_2"]["conductor_diameter"] == 1.3
    assert output["layer_3"]["conductor_diameter"] == 1.5
    menu.conductor_dimension.setText("")
    menu._conductor_dimensions_changed()
    assert menu.conductor_dimension.text() == "1.3"
    menu.ui.update_logger.assert_any_call("Conductor dimensions must be positive numbers.")
    menu.winding_tree_widget.setCurrentItem(second_side)
    menu._show_conductor_dimensions()
    assert menu.cond_material_label.text() == "Side 2 Conductor Material"
    assert menu.cond_material.currentText() == "Aluminium"
    assert menu.conductor_dimension.text() == "1.5"
    assert menu.side_load_label.text() == "Side 2 Load (ohm)"
    assert menu.side_load.text() == "2.0"
    menu.side_load.setText("4e-3")
    menu._side_load_changed()
    assert menu.gui_properties.winding.side_loads == [3.5, 0.004]
    assert menu.strand_diameter.text() == "0.2"
    assert menu.strand_number.text() == "20"
    menu.ui.update_logger.assert_any_call("Side 1: using conductor dimensions from its first layer.")
    output = menu._update_layers_definition()
    assert output["layer_1"]["strand_number"] == output["layer_2"]["strand_number"] == 15
    assert output["layer_1"]["strand_diameter"] == output["layer_2"]["strand_diameter"] == 0.12
    assert output["layer_3"]["strand_number"] == 20
    assert output["layer_3"]["conductor_diameter"] == 1.5
    assert first_side.data(0, Qt.UserRole)["strand_number"] == 15
    menu.strand_number.setText("1")
    menu._strand_settings_changed()
    assert menu.strand_number.text() == "20"
    menu.cond_type.setCurrentText("Rectangular")
    menu._conductor_type_changed()
    menu.winding_tree_widget.setCurrentItem(first_side)
    menu._show_conductor_dimensions()
    menu.conductor_dimension.setText("0.8")
    menu.conductor_height.setText("0.6")
    menu._conductor_dimensions_changed()
    rectangular = menu._update_layers_definition()
    assert rectangular["layer_1"]["conductor_width"] == rectangular["layer_2"]["conductor_width"] == 0.8
    assert rectangular["layer_1"]["conductor_height"] == rectangular["layer_2"]["conductor_height"] == 0.6
    assert rectangular["layer_3"]["conductor_width"] == 0.4
    menu.cond_type.setCurrentText("Litz Rectangular")
    menu._conductor_type_changed()
    rectangular_litz = menu._update_layers_definition()
    assert rectangular_litz["layer_1"]["conductor_width"] == 0.8
    assert rectangular_litz["layer_1"]["conductor_height"] == 0.6
    assert rectangular_litz["layer_1"]["strand_diameter"] == 0.12
    assert rectangular_litz["layer_1"]["strand_number"] == 15
    menu.cond_type.setCurrentText("Litz")
    menu._conductor_type_changed()
    assert menu._update_layers_definition()["layer_1"]["strand_number"] == 15
    assert menu._update_layers_definition()["layer_1"]["conductor_diameter"] == 1.3
    assert app is not None


def test_conductor_dimensions_controls_exist_in_main_page():
    app = QApplication.instance() or QApplication([])
    widget = QWidget()
    page = Ui_Geometry()
    page.setupUi(widget)
    assert widget.findChild(QLineEdit, "conductor_dimension") is not None
    assert widget.findChild(QLineEdit, "side_load") is not None
    assert widget.findChild(QLineEdit, "conductor_height") is not None
    assert widget.findChild(QLineEdit, "strand_diameter") is not None
    assert widget.findChild(QLineEdit, "strand_number") is not None
    assert app is not None


def test_conductor_type_switch_keeps_winding_layout_stable():
    app = QApplication.instance() or QApplication([])
    widget = QWidget()
    page = Ui_Geometry()
    page.setupUi(widget)
    menu = GeometryMenu.__new__(GeometryMenu)
    for name in (
        "winding_tree_widget",
        "cond_type",
        "conductor_dimension_label",
        "conductor_dimension",
        "conductor_height",
        "strand_diameter_label",
        "strand_diameter",
        "strand_number_label",
        "strand_number",
        "side_load_label",
        "side_load",
        "cond_material",
    ):
        setattr(menu, name, getattr(page, name))
    menu.cond_material_label = page.conductor_material_label
    widget.resize(1400, 900)
    widget.show()
    geometries = []
    strand_geometries = {}
    menu.geometry_menu_widget = widget
    assert [page.cond_type.itemText(i) for i in range(page.cond_type.count())] == list(CONDUCTOR_LABELS.values())
    for conductor_type in ("Rectangular", "Circular", "Litz", "Litz Rectangular", "Litz", "Rectangular"):
        page.cond_type.setCurrentText(CONDUCTOR_LABELS[conductor_type])
        menu._show_conductor_dimensions()
        for _ in range(3):
            app.processEvents()
        label = page.label_7
        assert page.cond_type.x() == label.geometry().right() + 1 + page.gridLayout_5.horizontalSpacing()
        if app.platformName() == "windows":
            assert (
                page.conductor_dimension_label.fontMetrics().horizontalAdvance(page.conductor_dimension_label.text())
                <= page.conductor_dimension_label.width()
            )
            table_left = page.winding_tree_widget.mapTo(page.groupBox_2, page.winding_tree_widget.rect().topLeft()).x()
            connection_left = page.connections_tree_widget.mapTo(
                page.groupBox_2, page.connections_tree_widget.rect().topLeft()
            ).x()
            combo_left = page.cond_type.mapTo(page.groupBox_2, page.cond_type.rect().topLeft()).x()
            assert table_left == connection_left == combo_left
            assert page.winding_tree_widget.width() == page.connections_tree_widget.width() == 440
            assert table_left + page.winding_tree_widget.width() <= page.groupBox_2.width() - 9
        geometries.append(
            tuple(
                item.geometry().getRect()
                for item in (
                    page.cond_type,
                    page.conductor_dimension_label,
                    page.side_load,
                    page.winding_tree_widget,
                )
            )
        )
        assert page.strand_diameter.isVisible() == (conductor_type in ("Litz", "Litz Rectangular"))
        assert page.conductor_height.isVisible() == (conductor_type in ("Rectangular", "Litz Rectangular"))
        if conductor_type in ("Rectangular", "Litz Rectangular"):
            assert page.conductor_dimension_label.text() == "Size (W x H) (mm)"
            width_pos = page.conductor_dimension.mapTo(widget, page.conductor_dimension.rect().topLeft())
            height_pos = page.conductor_height.mapTo(widget, page.conductor_height.rect().topLeft())
            assert width_pos.y() == height_pos.y()
            assert width_pos.x() < height_pos.x()
        if conductor_type in ("Litz", "Litz Rectangular"):
            strand_geometries[conductor_type] = tuple(
                (item.mapTo(widget, item.rect().topLeft()), item.size())
                for item in (
                    page.strand_diameter_label,
                    page.strand_diameter,
                    page.strand_number_label,
                    page.strand_number,
                )
            )
        if conductor_type == "Litz":
            assert page.conductor_dimension_label.text() == "Bundle Dia (mm)"
            assert page.strand_number.isVisible()
            dimension_pos = page.conductor_dimension.mapTo(widget, page.conductor_dimension.rect().topLeft())
            diameter_pos = page.strand_diameter.mapTo(widget, page.strand_diameter.rect().topLeft())
            count_pos = page.strand_number.mapTo(widget, page.strand_number.rect().topLeft())
            assert dimension_pos.x() == diameter_pos.x() == count_pos.x()
            assert dimension_pos.y() < diameter_pos.y() < count_pos.y()
            assert page.strand_number_label.mapTo(widget, page.strand_number_label.rect().topLeft()).x() == (
                page.strand_diameter_label.mapTo(widget, page.strand_diameter_label.rect().topLeft()).x()
            )
            assert dimension_pos.x() - page.cond_type.mapTo(widget, page.cond_type.rect().topLeft()).x() == 0
    assert strand_geometries["Litz"] == strand_geometries["Litz Rectangular"]
    assert all(geometry == geometries[0] for geometry in geometries)
    widget.close()


@pytest.mark.parametrize("litz", [True, False])
def test_winding_tree_aligned_at_top_of_grid_cell(litz):
    app = QApplication.instance() or QApplication([])
    widget = QWidget()
    page = Ui_Geometry()
    page.setupUi(widget)
    for field in (page.strand_diameter, page.strand_diameter_label, page.strand_number, page.strand_number_label):
        field.setVisible(litz)
    widget.resize(1400, 900)
    widget.show()
    app.processEvents()
    tree = page.winding_tree_widget
    assert tree.minimumHeight() <= tree.maximumHeight()
    assert tree.y() == page.gridLayout_5.cellRect(5, 1).top()
    preceding = page.strand_diameter if litz else page.conductor_height
    assert tree.mapTo(widget, tree.rect().topLeft()).y() >= preceding.mapTo(widget, preceding.rect().bottomLeft()).y()
    widget.close()


def test_connection_label_and_stashed_connections_follow_selected_side():
    app = QApplication.instance() or QApplication([])
    menu = GeometryMenu.__new__(GeometryMenu)
    menu.gui_properties = GUIProperties()
    menu.winding_tree_widget = QTreeWidget()
    menu.connections_tree_widget = QTreeWidget()
    menu.connection_label = QLabel()
    menu._connection_side = ""
    menu._importing_connections = False
    for number in (1, 2):
        side = QTreeWidgetItem([f"Side{number}"])
        side.setData(0, Qt.UserRole, {"side": number, "type": "Winding"})
        menu.winding_tree_widget.addTopLevelItem(side)
    side1 = menu.winding_tree_widget.topLevelItem(0)
    side2 = menu.winding_tree_widget.topLevelItem(1)
    menu.winding_tree_widget.setCurrentItem(side1)
    menu._stash_connections()
    assert menu.connection_label.text() == "Connect Side1 in:"
    menu.connections_tree_widget.addTopLevelItem(menu._connection_to_item({"type": "Layer", "id": "1"}))
    menu.winding_tree_widget.setCurrentItem(side2)
    menu._stash_connections()
    assert menu.connection_label.text() == "Connect Side2 in:"
    assert side1.data(0, Qt.UserRole)["conn_saved"]["id"] == "1"
    menu.winding_tree_widget.setCurrentItem(side1)
    menu._stash_connections()
    assert menu.connection_label.text() == "Connect Side1 in:"
    assert menu.connections_tree_widget.topLevelItem(0).data(0, Qt.UserRole)["id"] == "1"
    assert app is not None
