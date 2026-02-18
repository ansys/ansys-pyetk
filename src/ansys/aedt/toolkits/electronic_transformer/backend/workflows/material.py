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


from dataclasses import dataclass, field
from typing import Dict



@dataclass
class MaterialPropsCoreLoss:
    """Manages material properties for core loss."""
    cm: float = 0.0
    x: float = 0.0
    y: float = 0.0



@dataclass
class MaterialPropsMuvsFreq:
    """Manages material properties for magnetic permeability versus frequency."""
    data: Dict[float, float] = field(default_factory=dict)



@dataclass
class MaterialPropsElectric:
    """Manages electric material properties."""
    sigma: float = 0.0
    rel_permittivity: float = 1.0



@dataclass
class MaterialPropsMagnetic:
    """Manages magnetic material properties."""
    rel_permeability_vs_freq: MaterialPropsMuvsFreq = field(default_factory=MaterialPropsMuvsFreq)
    rel_permeability: float = 1.0
    core_loss: MaterialPropsCoreLoss = field(default_factory=MaterialPropsCoreLoss)


class Material:
    """Manages material properties."""

    def __init__(
        self,
        name: str,
    ):
        """Initialize and launch the material component.

        Parameters
        ----------
        name : str
            Name of the material.
        """
        self.__name: str = "ETK_" + name
        self.__magnetic_props: MaterialPropsMagnetic = MaterialPropsMagnetic()
        self.__electric_props: MaterialPropsElectric = MaterialPropsElectric()

    @property
    def name(self):
        """Get the material name."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def magnetic_props(self):
        """Get the magnetic properties."""
        return self.__magnetic_props

    @magnetic_props.setter
    def magnetic_props(self, value: MaterialPropsMagnetic):
        self.__magnetic_props = value

    @property
    def electric_props(self):
        """Get the electric properties."""
        return self.__electric_props

    @electric_props.setter
    def electric_props(self, value: MaterialPropsElectric):
        self.__electric_props = value
