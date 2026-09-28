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

from dataclasses import dataclass
from dataclasses import field
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


class MaterialClass:
    """Manages material properties."""

    def __init__(
        self,
        name: str = "",
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
        self.__magnetic_props.core_loss.cm = value.core_loss.cm
        self.__magnetic_props.core_loss.x = value.core_loss.x
        self.__magnetic_props.core_loss.y = value.core_loss.y
        self.__magnetic_props.rel_permeability = value.rel_permeability

    @property
    def conductivity(self):
        """Get the conductivity alias."""
        return self.__electric_props.sigma

    @conductivity.setter
    def conductivity(self, value: float):
        self.__electric_props.sigma = value

    @property
    def epsr(self):
        """Get the relative permittivity alias."""
        return self.__electric_props.rel_permittivity

    @epsr.setter
    def epsr(self, value: float):
        self.__electric_props.rel_permittivity = value

    @property
    def mur(self):
        """Get the relative permeability alias."""
        return self.__magnetic_props.rel_permeability

    @mur.setter
    def mur(self, value: float):
        self.__magnetic_props.rel_permeability = value

    @property
    def mu_vs_freq(self):
        """Get permeability-versus-frequency data as a list of pairs."""
        return list(self.__magnetic_props.rel_permeability_vs_freq.data.items())

    @mu_vs_freq.setter
    def mu_vs_freq(self, value):
        if value is None:
            self.__magnetic_props.rel_permeability_vs_freq.data = {}
        else:
            self.__magnetic_props.rel_permeability_vs_freq.data = dict(value)

    @property
    def power_ferrite_loss_params(self):
        """Get the core-loss alias."""
        return self.__magnetic_props.core_loss

    @power_ferrite_loss_params.setter
    def power_ferrite_loss_params(self, value: MaterialPropsCoreLoss):
        self.__magnetic_props.core_loss.cm = value.cm
        self.__magnetic_props.core_loss.x = value.x
        self.__magnetic_props.core_loss.y = value.y

    @property
    def electric_props(self):
        """Get the electric properties."""
        return self.__electric_props

    @electric_props.setter
    def electric_props(self, value: MaterialPropsElectric):
        self.__electric_props = value
