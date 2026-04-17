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

"""Unit tests for the models module."""

import pytest

from ansys.aedt.toolkits.electronic_transformer.ui.models import AirGapConfig
from ansys.aedt.toolkits.electronic_transformer.ui.models import BobbinProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import CircuitProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import Conductor
from ansys.aedt.toolkits.electronic_transformer.ui.models import ConnectionDefinitionProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import CoreGUIProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import CoreProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import ElectricalGUIProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import ExcitationProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import FrequencySweepProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import GUIProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import Insulation
from ansys.aedt.toolkits.electronic_transformer.ui.models import Layer
from ansys.aedt.toolkits.electronic_transformer.ui.models import LayerSideDefinitionProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import Properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import SettingsGUIProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import SettingsProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import Turns
from ansys.aedt.toolkits.electronic_transformer.ui.models import WindingConductorProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import WindingGUIProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import WindingLayerProperties
from ansys.aedt.toolkits.electronic_transformer.ui.models import WindingProperties

pytestmark = [pytest.mark.frontend]


class TestAirGapConfig:
    """Test the AirGapConfig model."""

    def test_default_values(self):
        """Test default values for AirGapConfig."""
        config = AirGapConfig()
        assert config.enabled is False
        assert config.location == "None"
        assert config.height == 0.0

    def test_custom_values(self):
        """Test custom values for AirGapConfig."""
        config = AirGapConfig(enabled=True, location="Center", height=1.5)
        assert config.enabled is True
        assert config.location == "Center"
        assert config.height == 1.5

    def test_validation_assignment(self):
        """Test that validation works on assignment."""
        config = AirGapConfig()
        config.enabled = True
        config.location = "Left"
        config.height = 2.0
        assert config.enabled is True
        assert config.location == "Left"
        assert config.height == 2.0


class TestCoreProperties:
    """Test the CoreProperties model."""

    def test_default_values(self):
        """Test default values for CoreProperties."""
        core = CoreProperties()
        assert core.supplier == ""
        assert core.type == ""
        assert core.model == ""
        assert core.material == ""
        assert isinstance(core.airgap, AirGapConfig)
        assert len(core.dimensions) == 8
        assert all(v == 0.0 for v in core.dimensions.values())

    def test_custom_values(self):
        """Test custom values for CoreProperties."""
        core = CoreProperties(
            supplier="TDK",
            type="EI",
            model="EI30",
            material="N87",
            dimensions={"D_1": 30.0, "D_2": 15.0},
        )
        assert core.supplier == "TDK"
        assert core.type == "EI"
        assert core.model == "EI30"
        assert core.material == "N87"


class TestWindingLayerProperties:
    """Test the WindingLayerProperties model."""

    def test_default_values(self):
        """Test default values for WindingLayerProperties."""
        layer = WindingLayerProperties()
        assert layer.type == ""
        assert layer.number_of_layers == 0
        assert layer.spacing == 0.0
        assert layer.definition_per_layer == {}

    def test_custom_values(self):
        """Test custom values for WindingLayerProperties."""
        layer = WindingLayerProperties(
            type="Wound",
            number_of_layers=3,
            spacing=0.5,
            definition_per_layer={"layer_1": {"conductor": "4"}},
        )
        assert layer.type == "Wound"
        assert layer.number_of_layers == 3
        assert layer.spacing == 0.5
        assert "layer_1" in layer.definition_per_layer


class TestWindingConductorProperties:
    """Test the WindingConductorProperties model."""

    def test_default_values(self):
        """Test default values for WindingConductorProperties."""
        conductor = WindingConductorProperties()
        assert conductor.cross_section == ""
        assert conductor.material == ""
        assert conductor.enabled_skin_depth_mesh is True


class TestWindingProperties:
    """Test the WindingProperties model."""

    def test_default_values(self):
        """Test default values for WindingProperties."""
        winding = WindingProperties()
        assert isinstance(winding.layers, WindingLayerProperties)
        assert isinstance(winding.conductor, WindingConductorProperties)
        assert winding.top_margin == 0.0
        assert winding.side_margin == 0.0


class TestBobbinProperties:
    """Test the BobbinProperties model."""

    def test_default_values(self):
        """Test default values for BobbinProperties."""
        bobbin = BobbinProperties()
        assert bobbin.enabled is False
        assert bobbin.thickness == 0.0
        assert bobbin.material == ""

    def test_custom_values(self):
        """Test custom values for BobbinProperties."""
        bobbin = BobbinProperties(enabled=True, thickness=1.6, material="FR4")
        assert bobbin.enabled is True
        assert bobbin.thickness == 1.6
        assert bobbin.material == "FR4"


class TestFrequencySweepProperties:
    """Test the FrequencySweepProperties model."""

    def test_default_values(self):
        """Test default values for FrequencySweepProperties."""
        sweep = FrequencySweepProperties()
        assert sweep.frequency_sweep is True
        assert sweep.start_frequency == 1.0
        assert sweep.start_frequency_unit == "Hz"
        assert sweep.stop_frequency == 100.0
        assert sweep.stop_frequency_unit == "Hz"
        assert sweep.samples == 3
        assert sweep.scale == "Logarithmic"

    def test_custom_values(self):
        """Test custom values for FrequencySweepProperties."""
        sweep = FrequencySweepProperties(
            frequency_sweep=False,
            start_frequency=1000.0,
            start_frequency_unit="kHz",
            stop_frequency=100000.0,
            stop_frequency_unit="MHz",
            samples=50,
            scale="Linear",
        )
        assert sweep.frequency_sweep is False
        assert sweep.start_frequency == 1000.0
        assert sweep.start_frequency_unit == "kHz"
        assert sweep.samples == 50
        assert sweep.scale == "Linear"


class TestExcitationProperties:
    """Test the ExcitationProperties model."""

    def test_default_values(self):
        """Test default values for ExcitationProperties."""
        excitation = ExcitationProperties()
        assert excitation.value == 0
        assert excitation.type == ""

    def test_custom_values(self):
        """Test custom values for ExcitationProperties."""
        excitation = ExcitationProperties(value=10.0, type="Voltage")
        assert excitation.value == 10.0
        assert excitation.type == "Voltage"


class TestCircuitProperties:
    """Test the CircuitProperties model."""

    def test_default_values(self):
        """Test default values for CircuitProperties."""
        circuit = CircuitProperties()
        assert circuit.connections_definition == ConnectionDefinitionProperties(RootModel={})
        assert circuit.layer_side_definition == LayerSideDefinitionProperties(RootModel={})
        assert circuit.side_loads == []
        assert isinstance(circuit.excitation, ExcitationProperties)
        assert circuit.transformer_sides == 0


class TestSettingsProperties:
    """Test the SettingsProperties model."""

    def test_default_values(self):
        """Test default values for SettingsProperties."""
        settings = SettingsProperties()
        assert settings.full_model is False
        assert settings.offset == 0.0
        assert settings.segmentation_angle == 0.0
        assert settings.adaptive_frequency == 0.0
        assert settings.percentage_error == 0.0
        assert settings.number_passes == 0
        assert settings.project_path == ""


class TestInsulation:
    """Test the Insulation model."""

    def test_default_values(self):
        """Test default values for Insulation."""
        insulation = Insulation()
        assert insulation.material == ""
        assert insulation.thickness == 0.05


class TestTurns:
    """Test the Turns model."""

    def test_default_values(self):
        """Test default values for Turns."""
        turns = Turns()
        assert turns.quantity == 10
        assert turns.spacing == ""
        assert turns.distance == 0.0


class TestConductor:
    """Test the Conductor model."""

    def test_default_values(self):
        """Test default values for Conductor."""
        conductor = Conductor()
        assert conductor.draw_skin_layers is True
        assert conductor.material == ""
        assert conductor.width == 54.0
        assert conductor.diameter == 1.0
        assert conductor.height == 34.0
        assert conductor.type == ""


class TestLayer:
    """Test the Layer model."""

    def test_default_values(self):
        """Test default values for Layer."""
        layer = Layer()
        assert layer.conductor == Conductor(
            draw_skin_layers=True, material="", width=54.0, diameter=1.0, height=34.0, type=""
        )
        assert layer.insulation == Insulation(material="", thickness=0.05)
        assert layer.turns == Turns(quantity=10, spacing="", distance=0.0)


class TestCoreGUIProperties:
    """Test the CoreGUIProperties model."""

    def test_default_values(self):
        """Test default values for CoreGUIProperties."""
        core_gui = CoreGUIProperties()
        assert core_gui.supplier == "Ferroxcube"
        assert core_gui.type == "E"
        assert core_gui.model == "E5.3/2.7/2"
        assert core_gui.material == "3C81"
        assert isinstance(core_gui.airgap, AirGapConfig)
        assert len(core_gui.dimensions) > 0


class TestElectricalGUIProperties:
    """Test the ElectricalGUIProperties model."""

    def test_default_values(self):
        """Test default values for ElectricalGUIProperties."""
        electrical = ElectricalGUIProperties()
        assert electrical.adaptive_frequency == 100.0
        assert electrical.excitation_strategy == "Voltage"
        assert electrical.voltage == 1.0
        assert electrical.current == 2.0
        assert electrical.excitation_value == 3.0


class TestSettingsGUIProperties:
    """Test the SettingsGUIProperties model."""

    def test_default_values(self):
        """Test default values for SettingsGUIProperties."""
        settings = SettingsGUIProperties()
        assert settings.draw_skin_layers is True
        assert settings.full_model is False
        assert settings.include_bobbin is True
        assert settings.number_passes == 5
        assert settings.percentage_error == 1.0
        assert settings.segmentation_angle == 10.0
        assert settings.offset == 50
        assert settings.project_path == ""
        assert settings.segments_number == 8
        assert isinstance(settings.frequency_sweep_definition, FrequencySweepProperties)


class TestWindingGUIProperties:
    """Test the WindingGUIProperties model."""

    def test_default_values(self):
        """Test default values for WindingGUIProperties."""
        winding = WindingGUIProperties()
        assert winding.layer_type == ""
        assert winding.layers_definition == {}
        assert winding.number_of_layers == 0
        assert winding.layer_spacing == 0.0
        assert winding.conductor_material == "Copper"
        assert winding.insulation_material == "material_insulation"
        assert winding.turn_spacing == 0.29
        assert isinstance(winding.layer, Layer)


class TestGUIProperties:
    """Test the GUIProperties model."""

    def test_default_values(self):
        """Test default values for GUIProperties."""
        gui_props = GUIProperties()
        assert isinstance(gui_props.core, CoreGUIProperties)
        assert isinstance(gui_props.electrical, ElectricalGUIProperties)
        assert isinstance(gui_props.winding, WindingGUIProperties)
        assert isinstance(gui_props.settings, SettingsGUIProperties)
        assert gui_props.materials == {}


class TestProperties:
    """Test the Properties model."""

    def test_default_values(self):
        """Test default values for Properties."""
        props = Properties()
        assert isinstance(props.core, CoreProperties)
        assert isinstance(props.winding, WindingProperties)
        assert isinstance(props.bobbin, BobbinProperties)
        assert isinstance(props.circuit, CircuitProperties)
        assert isinstance(props.settings, SettingsProperties)
        assert props.materials == {}

    def test_nested_property_updates(self):
        """Test updating nested properties."""
        props = Properties()

        # Update core properties
        props.core.supplier = "Ferroxcube"
        props.core.type = "E"
        props.core.model = "E30"

        assert props.core.supplier == "Ferroxcube"
        assert props.core.type == "E"
        assert props.core.model == "E30"

    def test_airgap_configuration(self):
        """Test airgap configuration in Properties."""
        props = Properties()

        props.core.airgap.enabled = True
        props.core.airgap.location = "Center"
        props.core.airgap.height = 2.5

        assert props.core.airgap.enabled is True
        assert props.core.airgap.location == "Center"
        assert props.core.airgap.height == 2.5

    def test_winding_configuration(self):
        """Test winding configuration in Properties."""
        props = Properties()

        props.winding.layers.type = "Rectangular"
        props.winding.layers.spacing = 0.5
        props.winding.top_margin = 1.0
        props.winding.side_margin = 0.8

        assert props.winding.layers.type == "Rectangular"
        assert props.winding.layers.spacing == 0.5

    def test_circuit_excitation_types(self):
        """Test different excitation types in circuit."""
        props = Properties()

        # Test voltage excitation
        props.circuit.excitation.type = "Voltage"
        props.circuit.excitation.value = 10.0
        assert props.circuit.excitation.type == "Voltage"
        assert props.circuit.excitation.value == 10.0

        # Test current excitation
        props.circuit.excitation.type = "Current"
        props.circuit.excitation.value = 5.0
        assert props.circuit.excitation.type == "Current"
        assert props.circuit.excitation.value == 5.0

    def test_materials_dictionary(self):
        """Test materials dictionary handling."""
        props = Properties()

        props.materials = {
            "N87": {"permeability": 2200},
            "Copper": {"conductivity": 5.8e7},
        }

        assert "N87" in props.materials
        assert "Copper" in props.materials
        assert props.materials["N87"]["permeability"] == 2200


class TestFrequencySweepPropertiesAdvanced:
    """Test advanced FrequencySweepProperties functionality."""

    def test_linear_scale(self):
        """Test linear scale configuration."""
        sweep = FrequencySweepProperties(scale="Linear")
        assert sweep.scale == "Linear"

    def test_logarithmic_scale(self):
        """Test logarithmic scale configuration."""
        sweep = FrequencySweepProperties(scale="Logarithmic")
        assert sweep.scale == "Logarithmic"

    def test_frequency_units(self):
        """Test different frequency units."""
        sweep = FrequencySweepProperties(start_frequency_unit="kHz", stop_frequency_unit="MHz")
        assert sweep.start_frequency_unit == "kHz"
        assert sweep.stop_frequency_unit == "MHz"

    def test_large_sample_count(self):
        """Test with large sample count."""
        sweep = FrequencySweepProperties(samples=1000)
        assert sweep.samples == 1000

    def test_disabled_sweep(self):
        """Test disabled frequency sweep."""
        sweep = FrequencySweepProperties(frequency_sweep=False)
        assert sweep.frequency_sweep is False


class TestCoreDimensionsHandling:
    """Test core dimensions handling across models."""

    def test_core_dimensions_update(self):
        """Test updating core dimensions."""
        core = CoreProperties()

        core.dimensions = {
            "D_1": 30.0,
            "D_2": 15.0,
            "D_3": 10.0,
            "D_4": 5.0,
            "D_5": 2.5,
            "D_6": 1.0,
            "D_7": 0.5,
            "D_8": 0.25,
        }

        assert len(core.dimensions) == 8
        assert core.dimensions["D_1"] == 30.0
        assert core.dimensions["D_8"] == 0.25

    def test_partial_dimensions_update(self):
        """Test partial dimensions update."""
        core = CoreProperties()

        core.dimensions["D_1"] = 50.0
        core.dimensions["D_2"] = 25.0

        assert core.dimensions["D_1"] == 50.0
        assert core.dimensions["D_2"] == 25.0
        # Other dimensions should still be 0.0
        assert core.dimensions["D_3"] == 0.0


class TestComplexWindingConfiguration:
    """Test complex winding configurations."""

    def test_multiple_layer_definition(self):
        """Test multiple layer definitions."""
        winding = WindingLayerProperties()

        winding.definition_per_layer = {
            "layer_1": {"turns": 10, "width": 2.0},
            "layer_2": {"turns": 15, "width": 1.5},
            "layer_3": {"turns": 20, "width": 1.0},
        }
        winding.number_of_layers = 3

        assert winding.number_of_layers == 3
        assert len(winding.definition_per_layer) == 3
        assert winding.definition_per_layer["layer_2"]["turns"] == 15

    def test_conductor_skin_depth_mesh(self):
        """Test conductor skin depth mesh setting."""
        conductor = WindingConductorProperties()

        conductor.enabled_skin_depth_mesh = False
        conductor.cross_section = "Circular"
        conductor.material = "Copper"

        assert conductor.enabled_skin_depth_mesh is False
        assert conductor.cross_section == "Circular"
