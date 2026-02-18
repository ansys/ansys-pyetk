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
import math

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import ALL_CORES
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import CoreCrossSection
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import GeometryCommon

logger = logging.getLogger(__name__)


class Winding(GeometryCommon):
    """Manages winding geometry."""

    def __init__(
        self,
        name: str,
        aedtapp,
        winding_properties,
        core_properties,
        settings_properties,
        bobbin_properties,
    ):
        """Initialize and launch the winding component.

        Parameters
        ----------
        name : str
            Name of the component.
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        winding_properties : :class:`ansys.aedt.toolkits.common.properties.WindingProperties`
            Winding properties.
        core_properties : :class:`ansys.aedt.toolkits.common.properties.CoreProperties`
            Core properties.
        settings_properties : :class:`ansys.aedt.toolkits.common.properties.SettingsProperties`
            Settings properties.
        bobbin_properties : :class:`ansys.aedt.toolkits.common.properties.BobbinProperties`
            Bobbin properties.
        circuit_properties : :class:`ansys.aedt.toolkits.common.properties.CircuitProperties`
            Circuit properties.
        """
        # The super class contains the Windings properties
        super().__init__(name, aedtapp, winding_properties)

        # If this class requires more properties, those should be private property
        self.__core_properties = core_properties
        self.__settings_properties = settings_properties
        self.__bobbin_properties = bobbin_properties
        self.__list_terminal_sections = []
        # Uses the first layer information
        self.__draw_skin_layers = next(iter(self.properties.layers.values())).conductor.draw_skin_layers
        self.__conductor_type = next(iter(self.properties.layers.values())).conductor.type

    @property
    def terminals_list(self):
        """Get the list of terminal sections."""
        return self.__list_terminal_sections

    @property
    def skin_layers_list(self):
        """Get the list of skin layers."""
        return self.__list_skin_layers

    def create_geometry(self):
        """Create the winding geometry.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        core_type = ALL_CORES[self.__core_properties.type]
        match core_type:
            case "ETDCore" | "RMCore" | "EPCore" | "PCore" | "PQCore":
                self.core_cross_section = CoreCrossSection.circular
            case "ECore" | "UCore" | "EICore" | "EFDCore" | "UICore":
                self.core_cross_section = CoreCrossSection.rectangular
            case _:
                logger.info("Core type not implemented.")
                return False

        list_objects_start = self.aedtapp.modeler.object_list
        self.__create_winding()
        list_objects_end = self.aedtapp.modeler.object_list

        ids_in_start = {obj.name for obj in list_objects_start}
        missing_obs = [obj for obj in list_objects_end if obj.name not in ids_in_start]

        # TODO: Is there an issue associated to this ? If yes, can you add it to be able to track it ?
        # This is due a defect in pyAEDT.
        # self.aedtapp.modeler.object_list returns some Tool objects created during the geometry construction
        list_objs = list(filter(lambda obj: obj.name.find("Tool") == -1, missing_obs))
        list_objs = list(filter(lambda obj: obj.name.find("skin") == -1, list_objs))
        self.__list_skin_layers = list(filter(lambda obj: obj.name.find("skin") != -1, missing_obs))

        self.objects_list_append(list_objs)
        self.compute_volume()

        # Sets the color
        self.set_color(255, 128, 0)

        if self.volume == 0:
            logger.info("Winding not created.")
            return False

        return True

    def __create_single_turn(
        self,
        sweep_path_x,
        sweep_path_y,
        position_z_final,
        layer_number,
        fillet_radius,
        segmentation_angle,
        profile_width=0.0,
        profile_height=0.0,
        profile_diameter=0.0,
        profile_segments_num=8,
        turn_num=0,
    ):
        """Create a single turn of the winding.

        Parameters
        ----------
        sweep_path_x : float
            Sweep path on the X axis.
        sweep_path_y : float
            Sweep path on the Y axis.
        position_z_final : float
            Final position on the Z axis.
        layer_number : int
            Layer number.
        fillet_radius : float
            Fillet radius.
        segmentation_angle : float
            Segmentation angle.
        profile_width : float, optional
            Profile width. The default is ``0.0``.
        profile_height : float, optional
            Profile height. The default is ``0.0``.
        profile_diameter : float, optional
            Profile diameter. The default is ``0.0``.
        profile_segments_num : int, optional
            Number of profile segments. The default is ``8``.
        turn_num : int, optional
            Turn number. The default is ``0``.

        Returns
        -------
        list
            List of object names.
        """
        wire_offset = (profile_height or 0.0) / 2
        if self.core_cross_section == CoreCrossSection.circular:
            path_name = self.__create_sweep_path_circular(
                sweep_path_x,
                sweep_path_y,
                position_z_final + wire_offset,
                fillet_radius,
                layer_number,
                segmentation_angle,
                turn_num,
            )
        elif self.core_cross_section == CoreCrossSection.rectangular:
            path_name = self.__create_sweep_path_rectangular(
                sweep_path_x,
                sweep_path_y,
                position_z_final + wire_offset,
                fillet_radius,
                layer_number,
                segmentation_angle,
                turn_num,
            )

        profile_name = "Layer{}".format(layer_number)
        if turn_num != 0:
            profile_name += "_{}".format(turn_num)

        object_names = []
        if self.__draw_skin_layers:
            self.__create_skin_layers(
                profile_name,
                object_names,
                position_z_final + wire_offset,
                profile_height,
                profile_width,
                sweep_path_x,
                profile_segments_num,
                profile_diameter,
            )
        if self.__conductor_type == "Rectangular":
            profile_name = self.aedtapp.modeler.create_rectangle(
                orientation="Y",
                origin=[(sweep_path_x) / 2 - profile_width / 2, 0, position_z_final],
                sizes=[profile_height, profile_width],
                is_covered=True,
                name=profile_name,
            )
        else:
            profile_name = self.aedtapp.modeler.create_circle(
                orientation="XZ",
                origin=[sweep_path_x / 2, 0, position_z_final],
                radius=profile_diameter / 2,
                num_sides=profile_segments_num,
                name=profile_name,
                is_covered=True,
            )

        object_names.append(profile_name)
        self.aedtapp.modeler.sweep_along_path(assignment=object_names, sweep_object=path_name)
        return object_names

    def __create_skin_layers(
        self,
        profile_name,
        object_names,
        position_z_final=None,
        profile_height=None,
        profile_width=None,
        sweep_path_x=None,
        profile_segments_num=None,
        profile_diameter=None,
    ):
        """Create manual skin layers from sheets.

        Parameters
        ----------
        profile_name : str
            Profile name.
        object_names : list
            List of object names.
        position_z_final : float, optional
            Final position on the Z axis. The default is ``None``.
        profile_height : float, optional
            Profile height. The default is ``None``.
        profile_width : float, optional
            Profile width. The default is ``None``.
        sweep_path_x : float, optional
            Sweep path on the X axis. The default is ``None``.
        profile_segments_num : int, optional
            Number of profile segments. The default is ``None``.
        profile_diameter : float, optional
            Profile diameter. The default is ``None``.
        """
        # TODO: Update it based on the Material class
        frequency = self.__settings_properties.analysis_setup.adaptive_frequency
        sigma = 58000000
        skin_depth = 503.292121 * math.sqrt(1 / (sigma * frequency)) * 1000  # convert to mm
        points = []

        for i in range(1, 3):
            profile_name = "{}_skin_{}".format(profile_name, i)
            if self.__conductor_type == "Rectangular":
                # validate if skin depth is less than 1/3 of conductor height/width (planar/wound)
                if self.properties.layer_type == "Planar":
                    if profile_height < 3 * skin_depth:
                        continue

                    # create horizontal lines to be swept for sheet
                    x_initial = (sweep_path_x - profile_width) / 2
                    z_coord = position_z_final - (profile_height / 2 - i * skin_depth / 2)
                    points.append(self.polyline_point(x=x_initial, y=0, z=z_coord))
                    points.append(self.polyline_point(x=x_initial + profile_width, y=0, z=z_coord))
                    name1 = self.aedtapp.modeler.create_polyline(
                        points=points,
                        segment_type=None,
                        cover_surface=False,
                        close_surface=True,
                        name=profile_name + "_low",
                        xsection_num_seg=12,
                    )

                    points = points[:1]
                    z_coord = position_z_final + (profile_height / 2 - i * skin_depth / 2)
                    points.append(self.polyline_point(x=x_initial, y=0, z=z_coord))
                    points.append(self.polyline_point(x=x_initial + profile_width, y=0, z=z_coord))

                    name2 = self.aedtapp.modeler.create_polyline(
                        points=points,
                        segment_type=None,
                        cover_surface=False,
                        close_surface=True,
                        name=profile_name + "_high",
                        xsection_num_seg=12,
                    )

                else:
                    # layer type Wound
                    if profile_width < 3 * skin_depth:
                        continue
                    # create vertical lines to be swept for sheet
                    x_coord = (sweep_path_x - profile_width) / 2 + i * skin_depth / 2
                    z_initial = position_z_final - profile_height / 2
                    points.clear()

                    points.append(self.polyline_point(x=x_coord, y=0, z=z_initial))
                    points.append(self.polyline_point(x=x_coord, y=0, z=z_initial + profile_height))
                    name1 = self.aedtapp.modeler.create_polyline(
                        points=points,
                        segment_type=None,
                        cover_surface=False,
                        close_surface=False,
                        name=profile_name + "_in",
                        xsection_num_seg=12,
                    )
                    points = points[:0]
                    x_coord = (sweep_path_x + profile_width) / 2 - i * skin_depth / 2
                    points.append(self.polyline_point(x=x_coord, y=0, z=z_initial))
                    points.append(self.polyline_point(x=x_coord, y=0, z=z_initial + profile_height))
                    name2 = self.aedtapp.modeler.create_polyline(
                        points=points,
                        segment_type=None,
                        cover_surface=False,
                        close_surface=False,
                        name=profile_name + "_out",
                        xsection_num_seg=12,
                    )

                points = points[:1]

                object_names.append(name1)
                object_names.append(name2)
            else:
                # conductor type Circle
                if profile_diameter < 3 * skin_depth:
                    continue

                name = self.aedtapp.modeler.create_circle(
                    orientation="XZ",
                    origin=[sweep_path_x / 2, 0, position_z_final],
                    radius=(profile_diameter - skin_depth * i) / 2,
                    num_sides=profile_segments_num,
                    name=profile_name,
                    is_covered=False,
                )

                object_names.append(name)

        # TODO: Is this necessary ?
        # if skin_depth < 0.02 * dimension:
        #     self.add_warning_message(
        #         "Skin layer is too thin, it is recommended to use Impedance Boundary"
        #     )  # TODO: Really how? on the surface of a solid conductor???

    def __create_sweep_path_rectangular(
        self, sweep_path_x, sweep_path_y, position_z, fillet_radius, layer_number, segmentation_angle=0, turn_num=0
    ):
        """Create a rectangular profile of the winding.

        This method sacrifices code size for explicitness. It generates points for each
        quadrant using a polyline that consists of arcs and straight lines.

        Parameters
        ----------
        sweep_path_x : float
            Size of the coil in the X direction.
        sweep_path_y : float
            Size of the coil in the Y direction.
        position_z : float
            Position of the coil on the Z axis.
        fillet_radius : float
            Radius of the fillet to make round corners of the coil.
        layer_number : int
            Layer number for the body name.
        segmentation_angle : float, optional
            Segmentation angle. A true surface would be a mesh overkill. The default is ``0``.
        turn_num : int, optional
            Turn number. It is used for planar transformers to append the path name.
            Otherwise, many warnings are generated in the UI. The default is ``0``.

        Returns
        -------
        str
            Name of the winding body.
        """
        # Six dimensions describing sweep path centroids

        dim1 = sweep_path_x / 2
        dim2 = sweep_path_y / 2
        dim3 = dim1 - (fillet_radius - 0.7071 * fillet_radius)
        dim4 = dim2 - (fillet_radius - 0.7071 * fillet_radius)
        dim5 = dim1 - fillet_radius
        dim6 = dim2 - fillet_radius

        # Coordinates are used to draw a polyline along which coil cross section will be swept.
        p1 = [-dim5, dim2, position_z]
        p2 = [dim5, dim2, position_z]
        p3 = [dim3, dim4, position_z]
        p4 = [dim1, dim6, position_z]
        p5 = [dim1, -dim6, position_z]
        p6 = [dim3, -dim4, position_z]
        p7 = [dim5, -dim2, position_z]
        p8 = [-dim5, -dim2, position_z]
        p9 = [-dim3, -dim4, position_z]
        p10 = [-dim1, -dim6, position_z]
        p11 = [-dim1, dim6, position_z]
        p12 = [-dim3, dim4, position_z]

        # ACT used "AngularArc", here we use "Arc" it creates same geometry but is simpler to implement
        vertices = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p1]
        segment_type = ["Line", "Arc", "Line", "Arc", "Line", "Arc", "Line", "Arc"]

        name = "Tool{}".format(layer_number)
        if turn_num != 0:
            name += "_turn{}".format(turn_num)

        name = self.aedtapp.modeler.create_polyline(
            points=vertices,
            segment_type=segment_type,
            cover_surface=False,
            close_surface=True,
            name=name,
            xsection_num_seg=12,
        )

        return name

    def __create_sweep_path_circular(
        self, sweep_path_x, _sweep_path_y, position_z, _fillet_radius, layer_number, segmentation_angle=0, turn_num=0
    ):
        """Create a round profile of the winding.

        Parameters
        ----------
        sweep_path_x : float
            Size of the coil in the X direction.
        _sweep_path_y :
            Unused. Kept to maintain the signature of the base class.
        position_z : float
            Position of the coil on the Z axis.
        _fillet_radius :
            Unused. Kept to maintain the signature of the base class.
        layer_number : int
            Layer number for the body name.
        segmentation_angle : float, optional
            Segmentation angle. A true surface would be a mesh overkill. The default is ``0``.
        turn_num : int, optional
            Turn number. It is used for planar transformers to append the path name.
            Otherwise, many warnings are generated in the UI. The default is ``0``.

        Returns
        -------
        str
            Name of the winding body.
        """
        name = "Tool{}".format(layer_number)
        if turn_num != 0:
            name += "_turn{}".format(turn_num)

        self.aedtapp.modeler.create_circle(
            orientation="XY",
            origin=[0, 0, position_z],
            radius=sweep_path_x / 2,
            # num_sides=segments_number Causes a parasolid issue: BUG 1317171
            name=name,
            is_covered=False,
        )

        return name

    def __create_winding(self):
        """Create the winding."""
        airgap_both, airgap_center, airgap_side = self.air_gap(self.__core_properties)
        dim_d2 = self.__core_properties.dimensions["D_2"]
        dim_d3 = self.__core_properties.dimensions["D_3"]
        dim_d5 = self.__core_properties.dimensions["D_5"]
        dim_d6 = self.__core_properties.dimensions["D_6"]
        conductor_height = conductor_width = conductor_diameter = segments_number = 0
        layer_type = self.properties.layer_type
        layer_spacing = float(self.properties.layer_spacing)
        top_bottom_margin = float(self.properties.top_margin)
        side_margin = float(self.properties.side_margin)
        bobbin_thickness = float(self.__bobbin_properties.board_thickness)
        winding_parameters_dict = self.properties.layers

        if (
            self.__core_properties.type == "RM"
            or self.__core_properties.type == "EP"
            or self.__core_properties.type == "P"
            or self.__core_properties.type == "PQ"
            or self.__core_properties.type == "PT"
        ):
            dim_d6 = self.__core_properties.dimensions["D_5"] / 2
            dim_d5 = self.__core_properties.dimensions["D_5"] / 2 + airgap_both / 2

        if self.__core_properties.type == "UI":
            dim_d2 = (self.__core_properties.dimensions["D_1"] - dim_d2) / 2 + 2 * self.__core_properties.dimensions[
                "D_2"
            ]
            dim_d3 = (self.__core_properties.dimensions["D_1"] - self.__core_properties.dimensions["D_2"]) / 2
            dim_d5 = self.__core_properties.dimensions["D_4"] / 2 + 2 * airgap_both
            dim_d6 = self.__core_properties.dimensions["D_5"]

        if self.__core_properties.type == "U":
            dim_d2 = (self.__core_properties.dimensions["D_1"] - dim_d2) / 2 + 2 * self.__core_properties.dimensions[
                "D_2"
            ]
            dim_d3 = (self.__core_properties.dimensions["D_1"] - self.__core_properties.dimensions["D_2"]) / 2
            dim_d5 = self.__core_properties.dimensions["D_4"] + airgap_both
            dim_d6 = self.__core_properties.dimensions["D_5"]

        segmentation_angle = self.__settings_properties.segmentation_angle
        winding_parameters_dict = winding_parameters_dict

        if layer_type == "Planar":
            margin = top_bottom_margin

            for layer_name, layer in winding_parameters_dict.items():
                conductor_width = layer.conductor.width
                conductor_height = layer.conductor.height
                num_of_turns = layer.turns.quantity
                turn_spacing = layer.turns.distance
                layer_num = int(layer_name.split("_")[1])

                if self.core_cross_section == CoreCrossSection.circular:
                    position_z = -dim_d5 + margin + bobbin_thickness
                else:
                    position_z = -dim_d5 / 2 + margin + bobbin_thickness

                for turn_num in range(num_of_turns):
                    sweep_path_x = (
                        dim_d3
                        + 2 * side_margin
                        + ((2 * turn_num + 1) * conductor_width)
                        + (2 * turn_num * turn_spacing)
                        + turn_spacing
                    )

                    sweep_path_y = (
                        dim_d6
                        + 2 * side_margin
                        + ((2 * turn_num + 1) * conductor_width)
                        + (2 * turn_num * turn_spacing)
                        + turn_spacing
                    )

                    self.__create_single_turn(
                        sweep_path_x,
                        sweep_path_y,
                        position_z,
                        layer_num,
                        fillet_radius=(sweep_path_x - dim_d3) / 2,
                        segmentation_angle=segmentation_angle,
                        profile_width=conductor_width,
                        profile_height=conductor_height,
                        turn_num=turn_num + 1,
                    )

                margin += layer_spacing + conductor_height + bobbin_thickness

        else:
            # ---- Wound transformer ---- #
            margin = side_margin + bobbin_thickness
            for layer_name, layer in winding_parameters_dict.items():
                num_of_turns = layer.turns.quantity
                insulation_thickness = layer.insulation.thickness
                layer_num = int(layer_name.split("_")[1])

                if self.__conductor_type == "Rectangular":
                    conductor_width = layer.conductor.width
                    conductor_height = layer.conductor.height
                    # factor of 2 is applied due to existence of margin and insulation on both sides
                    conductor_full_size = 2 * margin + conductor_width + 2 * insulation_thickness
                else:
                    conductor_diameter = layer.conductor.diameter
                    segments_number = self.segmentation_angle(self.__settings_properties.segmentation_angle)
                    # factor of 2 is applied due to existence of margin and insulation on both sides
                    conductor_full_size = 2 * margin + conductor_diameter + 2 * insulation_thickness

                conductor_z_position = dim_d5 - top_bottom_margin - bobbin_thickness - insulation_thickness
                sweep_path_x = dim_d3 + conductor_full_size
                sweep_path_y = dim_d6 + conductor_full_size
                fillet_radius = (sweep_path_x - dim_d3) / 2
                if self.__conductor_type == "Rectangular":
                    conductor_z_position -= conductor_height
                    move_vec = 2 * insulation_thickness + conductor_height
                    names = self.__create_single_turn(
                        sweep_path_x,
                        sweep_path_y,
                        conductor_z_position,
                        layer_num,
                        fillet_radius,
                        segmentation_angle,
                        profile_width=conductor_width,
                        profile_height=conductor_height,
                    )
                    margin += layer_spacing + conductor_width + 2 * insulation_thickness
                else:
                    conductor_z_position -= conductor_diameter / 2.0
                    move_vec = 2 * insulation_thickness + conductor_diameter
                    names = self.__create_single_turn(
                        sweep_path_x,
                        sweep_path_y,
                        conductor_z_position,
                        layer_num,
                        fillet_radius,
                        segmentation_angle,
                        profile_diameter=conductor_diameter,
                        profile_segments_num=segments_number,
                    )

                    margin += layer_spacing + conductor_diameter + 2 * insulation_thickness

                if num_of_turns > 1:
                    self.aedtapp.modeler.duplicate_along_line(
                        assignment=names, vector=[0.0, 0.0, -move_vec], clones=num_of_turns
                    )
        self.aedtapp.modeler.fit_all()
        return True

    def create_terminal_sections(self):
        """Create terminal sections for the winding."""
        # only for EFD core not to get an error due to section of winding
        # if "CentralLegCS" in self.editor.GetCoordinateSystems():
        if "CentralLegCS" in self.aedtapp.modeler.coordinate_systems:  # TODO: Check CS system usage for EFD core
            self.aedtapp.modeler.set_working_coordinate_system("CentralLegCS")

        self.aedtapp.modeler.section(assignment=self.objects_list, plane="ZX")

        for each_object in self.objects_list:
            self.aedtapp.modeler.separate_bodies(assignment=each_object.name + "_Section1")
            self.aedtapp.modeler.delete(assignment=each_object.name + "_Section1_Separate1")
            self.__list_terminal_sections.append(each_object.name + "_Section1")

    def create_excitations(self):
        """Create excitations for the winding."""
        counter = 1
        for _, layer in self.properties.layers.items():
            self.aedtapp.assign_winding(
                assignment=None,
                winding_type="External",
                is_solid=True,
                current=0.0,
                resistance=0.0,
                inductance=0.0,
                voltage=0.0,
                parallel_branches=1,
                phase=0,
                name="Layer_" + str(counter),
            )
            counter = counter + 1
        for _, value in enumerate(self.__list_terminal_sections):
            layer = value.split("_")[0]
            layer_num = layer[5:]

            # point_terminal = True
            self.aedtapp.assign_coil(assignment=value, name=value)
            self.aedtapp.add_winding_coils(assignment="Layer_" + layer_num, coils=value)
