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

## Perform imports and define constants
from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import auto

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.material import Material

ALL_CORES = {
    "E": "ECore",
    "EI": "EICore",
    "U": "UCore",
    "UI": "UICore",
    "PQ": "PQCore",
    "ETD": "ETDCore",
    "EQ": "ETDCore",
    "EC": "ETDCore",
    "RM": "RMCore",
    "EP": "EPCore",
    "EFD": "EFDCore",
    "ER": "ETDCore",
    "P": "PCore",
    "PT": "PCore",
    "PH": "PCore",
}
"""Mapping of core types to their corresponding core names."""


# Dedicated interface for geometry creation requirement
class GeometryCreatable(ABC):
    """Interface to enforce the presence of a create_geometry method.

    Any class that inherits from GeometryCreatable must implement create_geometry.
    """

    @abstractmethod
    def create_geometry(self):
        """Create the geometry for the component."""
        pass


class CoreCrossSection(Enum):
    """Manages core cross section."""

    NONE = auto()
    circular = auto()
    rectangular = auto()


class GeometryCommon(GeometryCreatable):
    """Manages common geometry.

    Any subclass that inherits from GeometryCommon must implement a
    ``create_geometry`` method, which is responsible for creating the geometry
    specific to that component.
    """

    def __init__(
        self,
        name: str,
        aedtapp,
        properties=None,
    ):
        """Initialize and launch the common geometry component.

        Parameters
        ----------
        name : str
            Name of the component.
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        properties :
            Properties of the component.
        """
        self.__name = name
        self.__properties = properties
        self.__volume = 0
        self.__core_cross_section = CoreCrossSection.NONE
        self.__color = [0, 0, 0]
        self.__objects_list = []
        self.__material = Material

    @property
    def core_cross_section(self):
        """Get the core cross section.

        Returns
        -------
        :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common.CoreCrossSection`
            Core cross section.
        """
        return self.__core_cross_section

    @core_cross_section.setter
    def core_cross_section(self, value: CoreCrossSection):
        self.__core_cross_section = value

    @property
    def name(self):
        """Get the component name.

        Returns
        -------
        str
            Name of the component.
        """
        return self.__name

    @property
    def properties(self):
        """Get the component properties.

        Returns
        -------
        object
            Component properties.
        """
        return self.__properties

    @property
    def volume(self):
        """Get the component volume.

        Returns
        -------
        float
            Component volume.
        """
        return self.__volume

    @volume.setter
    def volume(self, value: float):
        self.__volume = value


    @property
    def color(self):
        """Get the component color.

        Returns
        -------
        list
            RGB values for the component color.
        """
        return self.__color

    @property
    def objects_list(self):
        """Get the list of objects.

        Returns
        -------
        list
            List of objects.
        """
        return self.__objects_list

    def objects_list_append(self, this_object):
        """Append an object to the list of objects.

        Parameters
        ----------
        this_object :
            Object to append to the list.
        """
        self.__objects_list.extend(this_object)

    def set_color(self, r: int, g: int, b: int):
        """Set the component color.

        Parameters
        ----------
        r : int
            Red value.
        g : int
            Green value.
        b : int
            Blue value.
        """
        self.__color = [r, g, b]
        for each_object in self.__objects_list:
            each_object.color = "({0} {1} {2})".format(r, g, b)
            each_object.transparency = 0

    @property
    def material(self):
        """Get the material.

        Returns
        -------
        :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.material.Material`
            Material.
        """
        return self.__material

    def set_material(self, material: Material):
        """Set the material to a given object.

        Parameters
        ----------
        material : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.material.Material`
            Material to set.
        """
        self.__material = material

        material_name = self.__material.name + "_pyETK"

        # Creates the material
        mat = self.aedtapp.materials.add_material(material_name)
        mat.conductivity = self.__material.conductivity

        # Handles the magnetic permeability
        if len(self.__material.mu_vs_freq_list) > 0:
            # Creates the data set
            listx, listy = [], []
            for freq, mu in self.__material.mu_vs_freq_list:
                listx.append(freq)
                listy.append(mu)
            dataset_name = "Mu_" + material_name
            self.aedtapp.create_dataset(name=dataset_name, x=listx, y=listy)
            mat.permeability = "pwl($" + dataset_name + ",Freq)"
        else:
            mat.permeability = self.__material.mur

        # Core loss
        if (
            self.__material.power_ferrite_loss_params.x != 0
            or self.__material.power_ferrite_loss_params.y != 0
            or self.__material.power_ferrite_loss_params.cm != 0
        ):
            # Sets core loss parameters
            mat.set_power_ferrite_coreloss(
                cm=self.__material.power_ferrite_loss_params.cm,
                x=self.__material.power_ferrite_loss_params.x,
                y=self.__material.power_ferrite_loss_params.y,
            )

        # Assign material to objects
        self.aedtapp.assign_material(assignment=self.__objects_list, material=material_name)

    @staticmethod
    def air_gap(core_properties):
        """Get the air gap.

        Parameters
        ----------
        core_properties : :class:`ansys.aedt.toolkits.common.properties.CoreProperties`
            Core properties.

        Returns
        -------
        tuple
            airgap_both, airgap_center, and airgap_side.
        """
        airgap = core_properties.airgap
        airgap_side = 0
        airgap_center = 0
        airgap_both = 0
        if airgap.define_airgap:
            airgap_size = float(airgap.airgap_value) / 2.0
            if airgap.airgap_on_leg == "Center":
                airgap_center = airgap_size
            elif airgap.airgap_on_leg == "Side":
                airgap_side = airgap_size
            else:
                airgap_both = airgap_size
        return airgap_both, airgap_center, airgap_side

    @staticmethod
    def segmentation_angle(segmentation_angle):
        """Get the number of segments from the segmentation angle.

        Parameters
        ----------
        segmentation_angle : float
            Segmentation angle.

        Returns
        -------
        int
            Number of segments.
        """
        segments_number = 0 if segmentation_angle == 0 else int(360 / segmentation_angle)
        return segments_number

    @staticmethod
    def polyline_point(x=0, y=0, z=0):
        """Get the polyline point.

        This method passes through coordinates due to migration to PyAEDT.

        Parameters
        ----------
        x : float, optional
            X coordinate. The default is ``0``.
        y : float, optional
            Y coordinate. The default is ``0``.
        z : float, optional
            Z coordinate. The default is ``0``.

        Returns
        -------
        list
            List of coordinates.
        """
        # Just pass through coordinates due to migration to PyAEDT
        point = [x, y, z]
        return point

    def compute_volume(self):
        """Compute the volume of the component."""
        self.__volume = 0
        for each_object in self.__objects_list:
            self.__volume += each_object.volume
