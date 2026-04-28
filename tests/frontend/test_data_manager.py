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

"""Unit tests for the DataManager class."""

import json
from pathlib import Path

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.common.data_manager import DataManager
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import gui_properties

pytestmark = [pytest.mark.frontend]


class TestDataManager:
    """Test the DataManager class."""

    def test_init(self):
        """Test DataManager initialization."""
        dm = DataManager()
        assert dm.supported_json == "0.1.0"
        assert dm.properties is not None
        assert dm.gui_properties is not None
        assert dm.database_manager is not None

    def test_create_backend_data_structure(self):
        """Test backend data structure creation."""
        dm = DataManager()

        # Set some sample properties
        dm.properties.core.supplier = "TDK"
        dm.properties.core.type = "EI"
        dm.properties.core.model = "EI30"
        dm.properties.core.material = "N87"
        dm.properties.core.airgap.enabled = False
        dm.properties.core.airgap.location = "None"
        dm.properties.core.airgap.height = 0.0

        dm.properties.winding.layers.type = "Wound"
        dm.properties.winding.layers.spacing = 0.5
        dm.properties.winding.top_margin = 1.0
        dm.properties.winding.side_margin = 1.0
        dm.properties.winding.layers.definition_per_layer = {}

        dm.properties.bobbin.enabled = True
        dm.properties.bobbin.thickness = 1.6
        dm.properties.bobbin.material = "FR4"

        dm.properties.circuit.connections_definition = {}
        dm.properties.circuit.side_loads = []
        dm.properties.circuit.excitation.type = "Voltage"
        dm.properties.circuit.excitation.value = 10.0

        dm.properties.settings.adaptive_frequency = 100000.0
        dm.properties.settings.frequency_sweep_definition = {
            "frequency_sweep": True,
            "samples": 50,
            "scale": "Logarithmic",
            "start_frequency": 1000.0,
            "stop_frequency": 1000000.0,
        }
        dm.properties.settings.number_passes = 5
        dm.properties.settings.percentage_error = 1.0
        dm.properties.settings.full_model = False
        dm.properties.settings.offset = 50.0
        dm.properties.settings.segmentation_angle = 13.0
        dm.properties.materials = {}

        result = dm.create_backend_data()

        # Verify structure
        assert "json_version" in result
        assert result["json_version"] == "0.1.0"

        assert "core" in result
        assert result["core"]["supplier"] == "TDK"
        assert result["core"]["type"] == "EI"
        assert result["core"]["model"] == "EI30"
        assert result["core"]["material"] == "N87"
        assert "airgap" in result["core"]
        assert result["core"]["airgap"]["define_airgap"] is False

        assert "winding" in result
        assert result["winding"]["layer_type"] == "Wound"
        assert result["winding"]["layer_spacing"] == 0.5
        assert result["winding"]["top_margin"] == 1.0
        assert result["winding"]["side_margin"] == 1.0

        assert "bobbin" in result
        assert result["bobbin"]["draw_bobbin"] is True
        assert result["bobbin"]["board_thickness"] == 1.6
        assert result["bobbin"]["material"] == "FR4"

        assert "circuit" in result
        assert result["circuit"]["excitation"]["type"] == "voltage"
        assert result["circuit"]["excitation"]["value"] == 10.0

        assert "settings" in result
        assert result["settings"]["analysis_setup"]["adaptive_frequency"] == 100000.0
        assert result["settings"]["full_model"] is False

        assert "materials" in result

    def test_format_input_version_current(self):
        """Test formatting input with current version."""
        dm = DataManager()

        data = {
            "json_version": "0.1.0",
            "core": {
                "supplier": "TDK",
                "type": "EI",
                "model": "EI30",
                "material": "N87",
                "dimensions": {"D_1": 30.0, "D_2": 15.0},
                "airgap": {
                    "define_airgap": False,
                    "airgap_on_leg": "None",
                    "airgap_value": 0.0,
                },
            },
            "bobbin": {
                "draw_bobbin": True,
                "board_thickness": 1.6,
                "material": "FR4",
            },
            "winding": {
                "layer_type": "Wound",
                "layer_spacing": 0.5,
                "top_margin": 1.0,
                "side_margin": 1.0,
                "layers": {},
            },
            "circuit": {
                "connections": {},
                "side_loads": [],
                "excitation": {
                    "type": "Voltage",
                    "value": 10.0,
                },
            },
            "settings": {
                "full_model": False,
                "region_offset": 50.0,
                "segmentation_angle": 13.0,
                "analysis_setup": {
                    "adaptive_frequency": 100000.0,
                    "percentage_error": 1.0,
                    "number_passes": 5,
                    "frequency_sweep": {
                        "frequency_sweep": True,
                        "samples": 50,
                        "scale": "Logarithmic",
                        "start_frequency": 1000.0,
                        "stop_frequency": 1000000.0,
                    },
                },
            },
        }

        result = dm._format_input_version(data)

        assert "Working with .json version" in result
        assert dm.gui_properties.core.supplier == "TDK"
        assert dm.gui_properties.core.type == "EI"
        assert dm.gui_properties.core.model == "EI30"
        assert dm.gui_properties.core.material == "N87"
        assert dm.gui_properties.settings.include_bobbin is True
        assert dm.gui_properties.bobbin_board_and_margin.thickness == 1.6
        assert dm.gui_properties.electrical.adaptive_frequency == 100000.0

    def test_format_input_version_voltage_excitation(self):
        """Test formatting input with voltage excitation."""
        dm = DataManager()

        data = {
            "json_version": "0.1.0",
            "core": {
                "supplier": "TDK",
                "type": "EI",
                "model": "EI30",
                "material": "N87",
                "dimensions": {},
                "airgap": {"define_airgap": False, "airgap_on_leg": "None", "airgap_value": 0.0},
            },
            "bobbin": {"draw_bobbin": False, "board_thickness": 1.6, "material": "FR4"},
            "winding": {
                "layer_type": "Wound",
                "layer_spacing": 0.5,
                "top_margin": 1.0,
                "side_margin": 1.0,
                "layers": {},
            },
            "circuit": {
                "connections": {},
                "side_loads": [],
                "excitation": {"type": "voltage", "value": 12.0},
            },
            "settings": {
                "full_model": False,
                "region_offset": 50.0,
                "segmentation_angle": 13.0,
                "analysis_setup": {
                    "adaptive_frequency": 100000.0,
                    "percentage_error": 1.0,
                    "number_passes": 5,
                    "frequency_sweep": {
                        "frequency_sweep": True,
                        "samples": 50,
                        "scale": "Logarithmic",
                        "start_frequency": 1000.0,
                        "stop_frequency": 1000000.0,
                    },
                },
            },
        }

        _ = dm._format_input_version(data)

        assert dm.gui_properties.electrical.excitation_strategy == "voltage"
        assert dm.gui_properties.electrical.voltage == 12.0
        assert dm.gui_properties.electrical.current == 0
        assert dm.gui_properties.electrical.excitation_value == 12.0

    def test_format_input_version_current_excitation(self):
        """Test formatting input with current excitation."""
        dm = DataManager()

        data = {
            "json_version": "0.1.0",
            "core": {
                "supplier": "TDK",
                "type": "EI",
                "model": "EI30",
                "material": "N87",
                "dimensions": {},
                "airgap": {"define_airgap": False, "airgap_on_leg": "None", "airgap_value": 0.0},
            },
            "bobbin": {"draw_bobbin": False, "board_thickness": 1.6, "material": "FR4"},
            "winding": {
                "layer_type": "Wound",
                "layer_spacing": 0.5,
                "top_margin": 1.0,
                "side_margin": 1.0,
                "layers": {},
            },
            "circuit": {
                "connections": {},
                "side_loads": [],
                "excitation": {"type": "current", "value": 5.0},
            },
            "settings": {
                "full_model": False,
                "region_offset": 50.0,
                "segmentation_angle": 13.0,
                "analysis_setup": {
                    "adaptive_frequency": 100000.0,
                    "percentage_error": 1.0,
                    "number_passes": 5,
                    "frequency_sweep": {
                        "frequency_sweep": True,
                        "samples": 50,
                        "scale": "Logarithmic",
                        "start_frequency": 1000.0,
                        "stop_frequency": 1000000.0,
                    },
                },
            },
        }

        _ = dm._format_input_version(data)

        assert dm.gui_properties.electrical.excitation_strategy == "current"
        assert dm.gui_properties.electrical.current == 5.0
        assert dm.gui_properties.electrical.voltage == 0
        assert dm.gui_properties.electrical.excitation_value == 5.0

    def test_format_input_version_legacy(self):
        """Test formatting input with legacy format."""
        dm = DataManager()

        data = {
            "core_dimensions": {
                "supplier": "TDK",
                "core_type": "EI",
                "core_model": "EI30",
                "dimensions": {"D_1": 30.0},
                "airgap": {"define_airgap": False},
                "segmentation_angle": 13.0,
            },
            "winding_definition": {
                "material_name": "Copper",
                "draw_skin_layers": True,
                "layer_type": "Wound",
                "number_of_layers": 2,
                "layer_spacing": 0.5,
                "bobbin_board_thickness": 1.6,
                "top_margin": 1.0,
                "side_margin": 1.0,
                "conductor_type": "Rectangular",
                "include_bobbin": True,
                "layers_definition": {},
            },
            "setup_definition": {
                "core_material": "N87",
                "adaptive_frequency": 100000.0,
                "percentage_error": 1.0,
                "number_passes": 5,
                "side_loads": [],
                "excitation_strategy": "Voltage",
                "voltage": 10.0,
                "current": 0.0,
                "offset": 50.0,
                "full_model": False,
                "frequency_sweep_definition": {},
                "connections_definition": {},
                "layer_side_definition": {},
            },
        }

        result = dm._format_input_version(data)

        assert "Legacy Format" in result
        assert dm.gui_properties.core.supplier == "TDK"
        assert dm.gui_properties.core.type == "EI"
        assert dm.gui_properties.core.model == "EI30"
        assert dm.gui_properties.winding.conductor_material == "Copper"
        assert dm.gui_properties.settings.draw_skin_layers is True

    def test_create_backend_data_voltage_excitation(self):
        """Test backend data creation with voltage excitation."""
        dm = DataManager()

        dm.properties.circuit.excitation.type = "VOLTAGE"
        dm.properties.circuit.excitation.value = 12.0

        result = dm.create_backend_data()

        assert result["circuit"]["excitation"]["type"] == "voltage"
        assert result["circuit"]["excitation"]["value"] == 12.0

    def test_create_backend_data_current_excitation(self):
        """Test backend data creation with current excitation."""
        dm = DataManager()

        dm.properties.circuit.excitation.type = "Current"
        dm.properties.circuit.excitation.value = 5.0

        result = dm.create_backend_data()

        assert result["circuit"]["excitation"]["type"] == "current"
        assert result["circuit"]["excitation"]["value"] == 5.0

    def test_create_backend_data_airgap_enabled(self):
        """Test backend data creation with airgap enabled."""
        dm = DataManager()

        dm.properties.core.airgap.enabled = True
        dm.properties.core.airgap.location = "Center"
        dm.properties.core.airgap.height = 1.5

        result = dm.create_backend_data()

        assert result["core"]["airgap"]["define_airgap"] is True
        assert result["core"]["airgap"]["airgap_on_leg"] == "Center"
        assert result["core"]["airgap"]["airgap_value"] == 1.5

    def test_create_backend_data_frequency_sweep(self):
        """Test backend data creation with frequency sweep settings."""
        dm = DataManager()

        dm.properties.settings.frequency_sweep_definition = {
            "frequency_sweep": True,
            "samples": 100,
            "scale": "Linear",
            "start_frequency": 10000.0,
            "stop_frequency": 500000.0,
        }

        result = dm.create_backend_data()

        sweep = result["settings"]["analysis_setup"]["frequency_sweep"]
        assert sweep["frequency_sweep"] is True
        assert sweep["samples"] == 100
        assert sweep["scale"] == "Linear"
        assert sweep["start_frequency"] == 10000.0
        assert sweep["stop_frequency"] == 500000.0

    def test_create_backend_data_full_model(self):
        """Test backend data creation with full model enabled."""
        dm = DataManager()

        dm.properties.settings.full_model = True
        dm.properties.settings.offset = 75.0
        dm.properties.settings.segmentation_angle = 15.0

        result = dm.create_backend_data()

        assert result["settings"]["full_model"] is True
        assert result["settings"]["region_offset"] == 75.0
        assert result["settings"]["segmentation_angle"] == 15.0

    def test_create_backend_data_with_materials(self):
        """Test backend data creation with material definitions."""
        dm = DataManager()

        dm.properties.materials = {
            "N87": {"permeability": 2200, "conductivity": 0.0},
            "Copper": {"permeability": 1, "conductivity": 5.8e7},
        }

        result = dm.create_backend_data()

        assert "materials" in result
        assert "N87" in result["materials"]
        assert "Copper" in result["materials"]

    def test_create_backend_data_with_connections(self):
        """Test backend data creation with circuit connections."""
        dm = DataManager()

        dm.properties.circuit.connections_definition = {
            "primary": {"layers": ["layer_1", "layer_2"]},
            "secondary": {"layers": ["layer_3"]},
        }
        dm.properties.circuit.side_loads = [100.0, 50.0]

        result = dm.create_backend_data()

        assert result["circuit"]["connections"] == dm.properties.circuit.connections_definition
        assert result["circuit"]["side_loads"] == [100.0, 50.0]

    def test_create_backend_data_complete_winding(self):
        """Test backend data creation with complete winding configuration."""
        dm = DataManager()

        dm.properties.winding.layers.type = "Rectangular"
        dm.properties.winding.layers.spacing = 0.3
        dm.properties.winding.top_margin = 2.0
        dm.properties.winding.side_margin = 1.5
        dm.properties.winding.layers.definition_per_layer = {
            "layer_1": {"turns": 10, "width": 2.0},
            "layer_2": {"turns": 15, "width": 1.5},
        }

        result = dm.create_backend_data()

        winding = result["winding"]
        assert winding["layer_type"] == "Rectangular"
        assert winding["layer_spacing"] == 0.3
        assert winding["top_margin"] == 2.0
        assert winding["side_margin"] == 1.5
        assert "layer_1" in winding["layers"]
        assert "layer_2" in winding["layers"]

    def test_create_backend_data_lowercase_and_disabled(self):
        """Test lowercase conversion of excitation and disabled bobbin branch."""
        dm = DataManager()
        dm.properties.circuit.excitation.type = "VOLTAGE"  # Test .lower()
        dm.properties.bobbin.enabled = False  # Test boolean mapping

        result = dm.create_backend_data()

        assert result["circuit"]["excitation"]["type"] == "voltage"
        assert result["bobbin"]["draw_bobbin"] is False

    def test_format_input_version_unsupported(self):
        """Test branch: if data["json_version"] < self.supported_json."""
        dm = DataManager()
        # Version lower than 0.1.0
        unsupported_json_model = (
            Path(__file__).parent / "versioned_json" / "not_supported" / "not_supported_version.json"
        )
        with unsupported_json_model.open("rb") as f:
            data = json.load(f)
        result = dm._format_input_version(data)

        assert "Version 0.0.1 Not Supported" == result

    def test_format_input_version_legacy_act(self):
        """Test branch: if "json_version" not in data.keys()."""
        dm = DataManager()
        # Data missing the json_version key entirely
        act_json_model = Path(__file__).parent / "act_json" / "demo_IEEE.json"
        with act_json_model.open("rb") as f:
            data = json.load(f)
        result = dm._format_input_version(data)

        # This triggers the outer 'else' block for legacy ACT format
        assert "Input in Legacy Format. Save data in new format." == result

    def test_format_input_version_current_exact(self):
        """Ensure boundary condition for version comparison is covered."""
        dm = DataManager()
        versioned_json_model = Path(__file__).parent / "versioned_json" / "v0_1_0" / "EI_planar_rectangular.json"
        with versioned_json_model.open("rb") as f:
            data = json.load(f)

        result = dm._format_input_version(data)
        assert result == "Working with .json version: 0.1.0"

    def test_import_data_from_json(self):
        """Import data only if valid."""
        dm = DataManager()
        versioned_json_model = Path(__file__).parent / "versioned_json" / "v0_1_0" / "EI_planar_rectangular.json"
        not_supported_json = Path(__file__).parent / "not_supported_json" / "not_supported_version.json"

        msg, is_valid = dm._import_data_from_json(versioned_json_model)
        assert is_valid is True
        assert msg == "Working with .json version: 0.1.0"

        msg, is_valid = dm._import_data_from_json(not_supported_json)
        assert is_valid is False
        assert msg == "Incompatible/Not Selected JSON file"

    def test_create_layers_for_backend(self):
        """Create layers in same data structure as backend needs it."""
        dm = DataManager()

        versioned_json_model = Path(__file__).parent / "versioned_json" / "v0_1_0" / "EI_planar_rectangular.json"
        with versioned_json_model.open("rb") as f:
            versioned_json = json.load(f)

        _ = dm._format_input_version(versioned_json)
        dm._set_layers_from_json(versioned_json["winding"]["layers"])
        backend_layers = dm._create_layers_for_backend(gui_properties.winding.layers_definition)

        # compare output against versioned json file format
        versioned_json_layers = versioned_json["winding"]["layers"]
        assert backend_layers["layer_1"] == versioned_json_layers["layer_1"]

    def test_update_frontend_properties(self):
        """Load model and ensure that the properties sent to the backend are the same as the UI."""
        dm = DataManager()
        versioned_json_model = Path(__file__).parent / "versioned_json" / "v0_1_0" / "EI_planar_rectangular.json"
        _ = dm._import_data_from_json(versioned_json_model)
        dm._update_frontend_properties()
        assert fe_properties.core.type == gui_properties.core.type
        assert fe_properties.core.model == gui_properties.core.model
