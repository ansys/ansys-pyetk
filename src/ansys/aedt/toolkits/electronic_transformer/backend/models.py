# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

from enum import Enum
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import ConfigDict

from ansys.aedt.toolkits.common.backend.models import CommonProperties


# Supported source types
class ExcitationType(str, Enum):
    """Manages excitation types."""

    none = "none"
    voltage = "voltage"
    current = "current"


# Bobbin
class Bobbin(BaseModel, validate_assignment=True):
    """Manages bobbin properties."""

    draw_bobbin: bool = False
    material: str = ""
    board_thickness: float = 0.0


# Core and its components
class AirGap(BaseModel, validate_assignment=True):
    """Manages air gap properties."""

    define_airgap: bool = False
    airgap_on_leg: str = ""
    airgap_value: float = 0.0


class Core(BaseModel, validate_assignment=True):
    """Manages core properties."""

    supplier: str = ""
    type: str = ""
    model: str = ""
    material: str = ""
    airgap: AirGap = AirGap()
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


# Winding and its components
class Insulation(BaseModel, validate_assignment=True):
    """Manages insulation properties."""

    material: str = ""
    thickness: float = 0.0


class Turns(BaseModel, validate_assignment=True):
    """Manages turns properties."""

    quantity: int = 0
    spacing: str = ""
    distance: float = 0


class Conductor(BaseModel, validate_assignment=True):
    """Manages conductor properties."""

    draw_skin_layers: bool = True
    material: str = ""
    width: float = 0.0
    diameter: float = 0.0
    height: float = 0.0
    type: str = ""


class Layer(BaseModel, validate_assignment=True):
    """Manages layer properties."""

    conductor: Dict[str, Any] = Conductor()
    insulation: Dict[str, Any] = Insulation()
    turns: Dict[str, Any] = Turns()


class Winding(BaseModel, validate_assignment=True):
    """Manages winding properties."""

    layer_type: str = ""
    layer_spacing: float = 0.0
    top_margin: float = 0.0
    side_margin: float = 0.0
    layers: Dict[str, Layer] = {}


class Excitation(BaseModel, validate_assignment=True):
    """Manages excitation properties."""

    model_config = ConfigDict(use_enum_values=True)

    value: float = 0
    type: ExcitationType = ExcitationType.none


class Circuit(BaseModel, validate_assignment=True):
    """Manages circuit properties."""

    connections: Dict[str, Any] = {}
    side_loads: List[float] = []
    excitation: Excitation = Excitation()


# Settings and its components
class FrequencySweep(BaseModel, validate_assignment=True):
    """Manages frequency sweep properties."""

    frequency_sweep: bool = False
    start_frequency: int = 0
    stop_frequency: int = 0
    samples: int = 0
    scale: str = ""


class AnalysisSetup(BaseModel, validate_assignment=True):
    """Manages analysis setup properties."""

    adaptive_frequency: float = 0.0
    percentage_error: float = 0.0
    number_passes: int = 0
    frequency_sweep: FrequencySweep = FrequencySweep()


class Settings(BaseModel, validate_assignment=True):
    """Manages settings properties."""

    full_model: bool = False
    region_offset: float = 0.0
    segmentation_angle: int = 0
    analysis_setup: AnalysisSetup = AnalysisSetup()


# Material
class PowerFerriteLossParams(BaseModel, validate_assignment=True):
    """Manages power ferrite loss parameters."""

    cm: float = 0.0
    x: float = 0.0
    y: float = 0.0


class Material(BaseModel, validate_assignment=True):
    """Manages material properties."""

    conductivity: float = 0.0
    power_ferrite_loss_params: Dict[str, Any] = PowerFerriteLossParams()
    density: float = 0.0
    mur: float = 0.0
    epsr: float = 0.0
    mu_vs_freq_list: List[Any] = []
    name: str = ""


class JsonVersion(BaseModel, validate_assignment=True):
    """Json."""

    json_vertsion: str = ""


# All properties
class BackendResetProperties:
    def __init__(self):
        self.winding: Winding = Winding()
        self.core: Core = Core()
        self.bobbin: Bobbin = Bobbin()
        self.materials: Dict[str, Material] = {}
        self.settings: Settings = Settings()
        self.circuit: Circuit = Circuit()
        self.json_version: str = JsonVersion()


# All properties
class Properties(CommonProperties, validate_assignment=True):
    """Manages all properties."""

    winding: Winding = Winding()
    core: Core = Core()
    bobbin: Bobbin = Bobbin()
    materials: Dict[str, Material] = {}
    settings: Settings = Settings()
    circuit: Circuit = Circuit()
    json_version: str = JsonVersion()


properties = Properties()
layer = Layer()
