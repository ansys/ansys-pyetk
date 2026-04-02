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


import os
from pathlib import Path
import sys

from pydantic import BaseModel
from pydantic import Field

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from typing import Any
from typing import Dict
from typing import List

from ansys.aedt.toolkits.common.ui.models import UIProperties
from ansys.aedt.toolkits.common.ui.models import general_settings


class AirGapConfig(BaseModel, validate_assignment=True):
    """Manages airgap configuration."""

    enabled: bool = False
    location: str = "None"
    height: float = 0.0


class CoreProperties(BaseModel, validate_assignment=True):
    """Manages FE core properties."""

    supplier: str = ""
    type: str = ""
    model: str = ""
    material: str = ""
    airgap: AirGapConfig = AirGapConfig()
    dimensions: dict[str, float] = {
        "D_1": 0.0,
        "D_2": 0.0,
        "D_3": 0.0,
        "D_4": 0.0,
        "D_5": 0.0,
        "D_6": 0.0,
        "D_7": 0.0,
        "D_8": 0.0,
    }


class WindingLayerProperties(BaseModel, validate_assignment=True):
    """Manages FE layers properties."""

    type: str = ""  # layer_type: Wound, Planar
    number_of_layers: int = 0  # number_of_layer
    spacing: float = 0.0  # layer_spacing
    definition_per_layer: dict = Field(default_factory=dict)  # layers_definition = {layer_1 : {conductor_* : "4", }}


class WindingConductorProperties(BaseModel, validate_assignment=True):
    """Manages FE winding conductor properties."""

    cross_section: str = ""  # Rectangular, Circular
    material: str = ""
    enabled_skin_depth_mesh: bool = True


class WindingProperties(BaseModel, validate_assignment=True):
    """Manages FE winding properties."""

    layers: WindingLayerProperties = WindingLayerProperties()
    conductor: WindingConductorProperties = WindingConductorProperties()
    top_margin: float = 0.0
    side_margin: float = 0.0


class BobbinProperties(BaseModel, validate_assignment=True):
    """Manages FE bobbin properties."""

    enabled: bool = False
    thickness: float = 0.0
    material: str = ""


class FrequencySweepProperties(BaseModel, validate_assignment=True):
    """Manages FE frequency sweep properties."""

    frequency_sweep: bool = True
    start_frequency: float = 1.0
    start_frequency_unit: str = "Hz"
    stop_frequency: float = 100.0
    stop_frequency_unit: str = "Hz"
    samples: int = 3
    scale: str = "Logarithmic"


class LayerSideDefinitionProperties(BaseModel, validate_assignment=True):
    """Manages FE layer definition properties."""

    RootModel: Dict[str, List[str]] = Field(default_factory=dict)


class ConnectionDefinitionProperties(BaseModel, validate_assignment=True):
    """Manages FE connection definition properties."""

    RootModel: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class SettingsProperties(BaseModel, validate_assignment=True):
    """Manages FE settings properties."""

    full_model: bool = False
    offset: float = 0.0
    segmentation_angle: float = 0.0
    adaptive_frequency: float = 0.0
    percentage_error: float = 0.0
    number_passes: int = 0
    project_path: str = ""
    frequency_sweep_definition: Dict[str, Any] = FrequencySweepProperties()


class ExcitationProperties(BaseModel, validate_assignment=True):
    """Manages excitation types."""

    value: float = 0
    type: str = ""


class CircuitProperties(BaseModel, validate_assignment=True):
    """Manages circuits properties."""

    connections_definition: Dict[str, Any] = ConnectionDefinitionProperties()
    layer_side_definition: Dict[str, Any] = LayerSideDefinitionProperties()
    side_loads: list[float] = Field(default_factory=list)
    excitation: ExcitationProperties = ExcitationProperties()
    transformer_sides: int = 0


class Insulation(BaseModel, validate_assignment=True):
    """Manages insulation properties."""

    material: str = ""
    thickness: float = 0.05


class Turns(BaseModel, validate_assignment=True):
    """Manages turns properties."""

    quantity: int = 10
    spacing: str = ""
    distance: float = 0.0


class Conductor(BaseModel, validate_assignment=True):
    """Manages conductor properties."""

    draw_skin_layers: bool = True
    material: str = ""
    width: float = 54.0
    diameter: float = 1.0
    height: float = 34.0
    type: str = ""


class Layer(BaseModel, validate_assignment=True):
    """Manages layer properties."""

    conductor: Dict[str, Any] = Conductor()
    insulation: Dict[str, Any] = Insulation()
    turns: Dict[str, Any] = Turns()


class CoreGUIProperties(BaseModel, validate_assignment=True):
    """Manages UI core menu properties."""

    supplier: str = "Ferroxcube"
    type: str = "E"
    model: str = "E5.3/2.7/2"
    material: str = "3C81"
    dimensions: dict = {"D_1": 5.25, "D_2": 3.8, "D_3": 1.4, "D_4": 2.65, "D_5": 1.9, "D_6": 2, "D_7": 0, "D_8": 0}
    airgap: AirGapConfig = AirGapConfig()


class BobbinBoardAndMarginGUIProperties(BaseModel, validate_assignment=True):
    """Manages UI bobbin menu properties."""

    thickness: float = 0.1
    top_margin: float = 0.0
    side_margin: float = 0.0
    material: str = "material_bobbin"


class ElectricalGUIProperties(BaseModel, validate_assignment=True):
    """Manages UI electrical menu properties."""

    adaptive_frequency: float = 100.0
    excitation_strategy: str = "Voltage"
    voltage: float = 1.0
    current: float = 2.0
    excitation_value: float = 3.0


class SettingsGUIProperties(BaseModel, validate_assignment=True):
    """Manages UI settings menu properties."""

    draw_skin_layers: bool = True
    full_model: bool = False
    include_bobbin: bool = True
    number_passes: int = 2
    percentage_error: float = 1.0
    segmentation_angle: float = 13.0
    offset: float = 50.3
    project_path: str = ""
    segments_number: int = 8
    frequency_sweep_definition: FrequencySweepProperties = FrequencySweepProperties()


class WindingGUIProperties(BaseModel, validate_assignment=True):
    """Manages UI winding menu properties."""

    layer_type: str = ""
    layers_definition: dict = Field(default_factory=dict)
    number_of_layers: int = 0
    layer_spacing: float = 0.0
    layer_side_definition: dict = Field(default_factory=dict)
    side_loads: list = Field(default_factory=list)

    conductor_type: str = ""
    conductor_material: str = "Copper"
    insulation_material: str = "material_insulation"
    turn_spacing: float = 0.29
    connections_definition: Dict[str, Any] = Field(default_factory=dict)
    layer: Layer = Layer()


class GUIProperties(UIProperties, validate_assignment=True):
    """Manages Geometry Menu properties."""

    core: CoreGUIProperties = CoreGUIProperties()
    bobbin_board_and_margin: BobbinBoardAndMarginGUIProperties = BobbinBoardAndMarginGUIProperties()
    electrical: ElectricalGUIProperties = ElectricalGUIProperties()
    winding: WindingGUIProperties = WindingGUIProperties()
    settings: SettingsGUIProperties = SettingsGUIProperties()
    materials: Dict[str, Any] = Field(default_factory=dict)


class Properties(UIProperties, validate_assignment=True):
    """Store all properties."""

    core: CoreProperties = CoreProperties()
    winding: WindingProperties = WindingProperties()
    bobbin: BobbinProperties = BobbinProperties()
    circuit: CircuitProperties = CircuitProperties()
    settings: SettingsProperties = SettingsProperties()
    materials: Dict[str, Any] = Field(default_factory=dict)


# Set logo and icon for the toolkit
images_dir = Path(__file__).parent / "windows" / "images"
general_settings.icon=str(images_dir / "pyetk_icon.png")
general_settings.logo=str(images_dir / "pyetk_logo.svg")

frontend_properties = {}
if "PYAEDT_TOOLKIT_CONFIG_DIR" in os.environ:
    local_dir = Path(os.environ["PYAEDT_TOOLKIT_CONFIG_DIR"]).absolute()
    frontend_config = Path(local_dir) / "frontend_properties.toml"
    if frontend_config.is_file():
        with frontend_config.open(mode="rb") as file_handler:
            frontend_properties = tomllib.load(file_handler)

if not frontend_properties and (Path(__file__).parent / "frontend_properties.toml").is_file():
    with (Path(__file__).parent / "frontend_properties.toml").open(mode="rb") as file_handler:
        frontend_properties = tomllib.load(file_handler)

toolkit_property = {}
if frontend_properties:
    for frontend_key in frontend_properties:
        if frontend_key == "defaults":
            for toolkit_key in frontend_properties["defaults"]:
                if hasattr(general_settings, toolkit_key):
                    setattr(general_settings, toolkit_key, frontend_properties["defaults"][toolkit_key])
        else:
            toolkit_property[frontend_key] = frontend_properties[frontend_key]

new_common_properties = {}
for common_key in general_settings:
    new_common_properties[common_key[0]] = common_key[1]

fe_properties = Properties(**toolkit_property, **new_common_properties)
gui_properties = GUIProperties(**toolkit_property, **new_common_properties)
