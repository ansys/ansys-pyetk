# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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
from typing import Any
from typing import Dict


class MaterialPropsCoreLoss:
    """Manages material properties for core loss."""

    cm: float = 0
    x: float = 0
    y: float = 0


class MaterialPropsMuvsFreq:
    """Manages material properties for magnetic permeability versus frequency."""

    data: Dict[float, float] = {}


class MaterialPropsElectric:
    """Manages electric material properties."""

    sigma: float = 0
    rel_permittivity: float = 1


class MaterialPropsMagnetic:
    """Manages magnetic material properties."""

    rel_permeability_vs_freq: Dict[str, Any] = MaterialPropsMuvsFreq()
    rel_permeability: float = 1
    core_loss: MaterialPropsCoreLoss = MaterialPropsCoreLoss()


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
    def magnetic_props(self, value: MaterialPropsMagnetic()):
        self.__magnetic_props = value

    @property
    def electric_props(self):
        """Get the electric properties."""
        return self.__electric_props

    @electric_props.setter
    def electric_props(self, value: MaterialPropsElectric()):
        self.__electric_props = value
