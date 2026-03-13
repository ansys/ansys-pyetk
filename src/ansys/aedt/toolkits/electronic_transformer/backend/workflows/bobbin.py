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

import logging

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import ALL_CORES
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import CoreCrossSection
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import GeometryCommon

logger = logging.getLogger(__name__)


class Bobbin(GeometryCommon):
    """Manages bobbin geometry."""

    def __init__(self, name: str, aedtapp, bobbin_properties, core_properties, winding_properties, settings_properties):
        """Initialize and launch the bobbin component.

        Parameters
        ----------
        name : str
            Name of the component.
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        bobbin_properties : :class:`ansys.aedt.toolkits.common.properties.BobbinProperties`
            Bobbin properties.
        core_properties : :class:`ansys.aedt.toolkits.common.properties.CoreProperties`
            Core properties.
        winding_properties : :class:`ansys.aedt.toolkits.common.properties.WindingProperties`
            Winding properties.
        settings_properties : :class:`ansys.aedt.toolkits.common.properties.SettingsProperties`
            Settings properties.
        """
        # The super class contains the Bobbin properties.
        # Note that the Bobbin Properties are defined in the WindingProperties model
        super().__init__(name, aedtapp, bobbin_properties)

        # If this class requires more properties, those should be private property
        self.__core_properties = core_properties
        self.__winding_properties = winding_properties
        self.__segments_number = self.segmentation_angle(settings_properties.segmentation_angle)
        self.aedtapp=aedtapp

    def create_geometry(self):
        """Create the bobbin geometry."""
        # Initialize parameters
        airgap_both, _, _ = self.air_gap(self.__core_properties)
        dim_d1 = self.__core_properties.dimensions["D_1"]
        dim_d2 = self.__core_properties.dimensions["D_2"]
        dim_d3 = self.__core_properties.dimensions["D_3"]
        dim_d5 = self.__core_properties.dimensions["D_5"]
        dim_d6 = self.__core_properties.dimensions["D_6"]
        layer_type = self.__winding_properties.layer_type
        top_bottom_margin = float(self.__winding_properties.top_margin)
        include_bobbin = self.properties.draw_bobbin
        bobbin_board_thickness = float(self.properties.board_thickness)
        layers_definition = self.__winding_properties.layers
        self.__layer_spacing = self.__winding_properties.layer_spacing

        # Get core cross-section depending on core type: Circular or Rectangular
        core_type = ALL_CORES[self.__core_properties.type]
        circular_cores = {"ETDCore", "RMCore", "EPCore", "PCore", "PQCore"}
        rectangular_cores = {"ECore", "UCore", "EICore", "EFDCore", "UICore"}

        if core_type in circular_cores:
            self.core_cross_section = CoreCrossSection.circular
        elif core_type in rectangular_cores:
            self.core_cross_section = CoreCrossSection.rectangular
        else:
            logger.info("Bobbin type not implemented.")
            return False

        # Rescale dimensions according to core shape
        if self.__core_properties.type in {"RM", "EP", "P", "PQ", "PT"}:
            dim_d6 = self.__core_properties.dimensions["D_5"] / 2
            dim_d5 = self.__core_properties.dimensions["D_5"] / 2 + airgap_both / 2

        if self.__core_properties.type == "UI":
            dim_d2 = (dim_d1 - dim_d2) / 2 + 2 * self.__core_properties.dimensions["D_2"]
            dim_d3 = (self.__core_properties.dimensions["D_1"] - self.__core_properties.dimensions["D_2"]) / 2
            dim_d5 = self.__core_properties.dimensions["D_4"] / 2 + 2 * airgap_both
            dim_d6 = self.__core_properties.dimensions["D_5"]

        if self.__core_properties.type == "U":
            dim_d2 = (dim_d1 - dim_d2) / 2 + 2 * self.__core_properties.dimensions["D_2"]
            dim_d3 = (dim_d1 - self.__core_properties.dimensions["D_2"]) / 2
            dim_d5 = self.__core_properties.dimensions["D_4"] + airgap_both
            dim_d6 = self.__core_properties.dimensions["D_5"]

        slot_height = float(dim_d5) * 2

        list_objects_start = self.aedtapp.modeler.object_list
        # Create Board in Planar layers, or Bobbin in Wound layers
        if include_bobbin:
            if layer_type == "Planar":
                self.__draw_board(
                    slot_height=slot_height,
                    dim_d2=dim_d2,
                    dim_d3=dim_d3,
                    dim_d5=dim_d5,
                    dim_d6=dim_d6,
                    margin=top_bottom_margin,
                    board_thickness=bobbin_board_thickness,
                    layers_definition=layers_definition,
                )
            else:
                self.__draw_bobbin(
                    slot_height=slot_height + airgap_both,
                    dim_d2=dim_d2,
                    dim_d3=dim_d3,
                    dim_d6=dim_d6,
                    bobbin_thickness=bobbin_board_thickness,
                )
            list_objects_end = self.aedtapp.modeler.object_list

            ids_in_start = {obj.name for obj in list_objects_start}
            missing_obs = [obj for obj in list_objects_end if obj.name not in ids_in_start]

            self.objects_list_append(missing_obs)
            self.compute_volume()

            self.set_color(255, 255, 0)

            if self.volume == 0:
                logger.info("Bobbin not created.")
                return False

    def __draw_board_rectangular(
        self, slot_height, dim_d2, dim_d3, dim_d5, dim_d6, margin, board_thickness, layers_definition
    ):
        """Draw a rectangular board.

        Parameters
        ----------
        slot_height : float
            Slot height.
        dim_d2 : float
            Dimension D2.
        dim_d3 : float
            Dimension D3.
        dim_d5 : float
            Dimension D5.
        dim_d6 : float
            Dimension D6.
        margin : float
            Margin.
        board_thickness : float
            Board thickness.
        layers_definition : dict
            Layers definition.
        """
        z_position = margin - dim_d5 / 2
        y_size = dim_d6 + (dim_d2 - dim_d3)

        for layer, definition in layers_definition.items():
            self.aedtapp.modeler.create_box(
                origin=[-dim_d2 / 2, -y_size / 2, z_position],
                sizes=[dim_d2, y_size, board_thickness],
                name="Board_{}".format(layer),
            )

            self.aedtapp.modeler.create_box(
                origin=[-dim_d3 / 2, -dim_d6 / 2, z_position],
                sizes=[dim_d3, dim_d6, slot_height],
                name="BoardSlot_{}".format(layer),
            )

            # subtract full slot, no need to calculate precisely
            self.aedtapp.modeler.subtract(
                blank_list="Board_{}".format(layer), tool_list="BoardSlot_{}".format(layer), keep_originals=False
            )

            this_conductor_height = 0
            if definition.conductor.height > definition.conductor.diameter:
                this_conductor_height = definition.conductor.height
            else:
                this_conductor_height = definition.conductor.diameter

            z_position += this_conductor_height + board_thickness + self.__layer_spacing

    def __draw_board_circular(self, slot_height, dim_d2, dim_d3, dim_d5, margin, board_thickness, layers_definition):
        """Draw a circular board.

        Parameters
        ----------
        slot_height : float
            Slot height.
        dim_d2 : float
            Dimension D2.
        dim_d3 : float
            Dimension D3.
        dim_d5 : float
            Dimension D5.
        margin : float
            Margin.
        board_thickness : float
            Board thickness.
        layers_definition : dict
            Layers definition.
        """
        z_position = margin - dim_d5

        for layer, definition in layers_definition.items():
            board = self.aedtapp.modeler.create_cylinder(
                orientation="Z",
                origin=[0, 0, z_position],
                radius=dim_d2 / 2,
                height=board_thickness,
                segments_number=self.__segments_number,
                name="Board_{}".format(layer),
            )

            board_slot = self.aedtapp.modeler.create_cylinder(
                orientation="Z",
                origin=[0, 0, z_position],
                radius=dim_d3 / 2,
                height=slot_height,
                segments_number=self.__segments_number,
                name="BoardSlot_{}".format(layer),
            )
            self.aedtapp.modeler.subtract(board.name, board_slot.name, keep_originals=False)

            this_conductor_height = 0
            if definition.conductor.height > definition.conductor.diameter:
                this_conductor_height = definition.conductor.height
            else:
                this_conductor_height = definition.conductor.diameter

            z_position += this_conductor_height + board_thickness + self.__layer_spacing

    def __draw_bobbin_rectangular(self, slot_height, dim_d2, dim_d3, dim_d6, bobbin_thickness):
        """Draw a rectangular bobbin.

        Parameters
        ----------
        slot_height : float
            Slot height.
        dim_d2 : float
            Dimension D2.
        dim_d3 : float
            Dimension D3.
        dim_d6 : float
            Dimension D6.
        bobbin_thickness : float
            Bobbin thickness.
        """
        fillet_rad = (dim_d2 - dim_d3) / 2

        y_size = dim_d6 + (dim_d2 - dim_d3)

        handle = self.aedtapp.modeler.create_box(
            origin=[-dim_d2 / 2, -y_size / 2, -slot_height / 2], sizes=[dim_d2, y_size, bobbin_thickness], name="Bobbin"
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-dim_d2 / 2, -y_size / 2, slot_height / 2], sizes=[dim_d2, y_size, -bobbin_thickness], name="BobT2"
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-dim_d3 / 2 - bobbin_thickness, -dim_d6 / 2 - bobbin_thickness, -slot_height / 2],
            sizes=[dim_d3 + 2 * bobbin_thickness, dim_d6 + 2 * bobbin_thickness, slot_height],
            name="BobT3",
        )

        self.aedtapp.modeler.unite("Bobbin,BobT2,BobT3")

        self.aedtapp.modeler.create_box(
            origin=[-dim_d3 / 2, -dim_d6 / 2, -slot_height / 2], sizes=[dim_d3, dim_d6, slot_height], name="BobSlot"
        )

        self.aedtapp.modeler.subtract("Bobbin", "BobSlot", keep_originals=False)

        x_edge_pos = dim_d2 / 2
        y_edge_pos = y_size / 2
        z_edge_pos = (slot_height - bobbin_thickness) / 2

        # Fillets
        pos_x = x_edge_pos
        pos_y = y_edge_pos
        pos_z = z_edge_pos
        body_name = "Bobbin"
        radius = fillet_rad

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[-pos_x, -pos_y, -pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[-pos_x, pos_y, -pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, -pos_y, -pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, -pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[-pos_x, -pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[-pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, -pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

    def __draw_bobbin_circular(self, slot_height, dim_d2, dim_d3, bobbin_thickness=0.1):
        """Draw a circular bobbin.

        Parameters
        ----------
        slot_height : float
            Slot height.
        dim_d2 : float
            Dimension D2.
        dim_d3 : float
            Dimension D3.
        bobbin_thickness : float, optional
            Bobbin thickness. The default is ``0.1``.
        """
        # top part
        self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[0, 0, -bobbin_thickness + (slot_height / 2.0)],
            radius=dim_d2 / 2,
            height=bobbin_thickness,
            segments_number=self.__segments_number,
            name="Bobbin",
        )

        self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[0, 0, -(slot_height / 2.0)],
            radius=dim_d2 / 2,
            height=bobbin_thickness,
            segments_number=self.__segments_number,
            name="Bob_bottom",
        )

        self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[0, 0, bobbin_thickness - (slot_height / 2.0)],
            radius=dim_d3 / 2 + bobbin_thickness,
            height=slot_height - 2 * bobbin_thickness,
            segments_number=self.__segments_number,
            name="Bob_central",
        )

        self.aedtapp.modeler.unite("Bobbin,Bob_bottom,Bob_central")
        self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[0, 0, -slot_height / 2.0],
            radius=dim_d3 / 2,
            height=slot_height,
            segments_number=self.__segments_number,
            name="Bob_hollow",
        )

        self.aedtapp.modeler.subtract("Bobbin", "Bob_hollow", keep_originals=False)

    def __draw_bobbin(self, slot_height, dim_d2, dim_d3, bobbin_thickness, dim_d6=0.0):
        """Draw a bobbin.

        Parameters
        ----------
        slot_height : float
            Slot height.
        dim_d2 : float
            Dimension D2.
        dim_d3 : float
            Dimension D3.
        bobbin_thickness : float
            Bobbin thickness.
        dim_d6 : float, optional
            Dimension D6. The default is ``0.0``.
        """
        if self.core_cross_section == CoreCrossSection.circular:
            self.__draw_bobbin_circular(slot_height, dim_d2, dim_d3, bobbin_thickness)
        else:
            self.__draw_bobbin_rectangular(slot_height, dim_d2, dim_d3, dim_d6, bobbin_thickness)
        self.aedtapp.modeler.fit_all()

    def __draw_board(self, slot_height, dim_d2, dim_d3, dim_d5, margin, board_thickness, layers_definition, dim_d6=0.0):
        """Draw a board.

        Parameters
        ----------
        slot_height : float
            Slot height.
        dim_d2 : float
            Dimension D2.
        dim_d3 : float
            Dimension D3.
        dim_d5 : float
            Dimension D5.
        margin : float
            Margin.
        board_thickness : float
            Board thickness.
        layers_definition : dict
            Layers definition.
        dim_d6 : float, optional
            Dimension D6. The default is ``0.0``.
        """
        if self.core_cross_section == CoreCrossSection.circular:
            self.__draw_board_circular(slot_height, dim_d2, dim_d3, dim_d5, margin, board_thickness, layers_definition)
        else:
            self.__draw_board_rectangular(
                slot_height, dim_d2, dim_d3, dim_d5, dim_d6, margin, board_thickness, layers_definition
            )
        self.aedtapp.modeler.fit_all()
