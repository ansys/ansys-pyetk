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

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import GeometryCommon

logger = logging.getLogger(__name__)


class Core(GeometryCommon):
    """Manages core geometry."""

    def __init__(self, name: str, aedtapp, core_properties, settings_properties):
        """Initialize and launch the core component.

        Parameters
        ----------
        name : str
            Name of the component.
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        core_properties : :class:`ansys.aedt.toolkits.common.properties.CoreProperties`
            Core properties.
        settings_properties : :class:`ansys.aedt.toolkits.common.properties.SettingsProperties`
            Settings properties.
        """
        super().__init__(name, aedtapp, core_properties)
        self.all_cores = {
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

        self.__segments_number = self.segmentation_angle(settings_properties.segmentation_angle)

    def create_geometry(self):
        """Create the core geometry.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        list_objects_start = self.aedtapp.modeler.object_list

        if self.all_cores[self.properties.type] == "ETDCore":
            self.__create_etd_core()
        elif self.all_cores[self.properties.type] == "ECore":
            self.__create_e_core()
        elif self.all_cores[self.properties.type] == "RMCore":
            self.__create_rm_core()
        elif self.all_cores[self.properties.type] == "UCore":
            self.__create_u_core()
        elif self.all_cores[self.properties.type] == "EICore":
            self.__create_ei_core()
        elif self.all_cores[self.properties.type] == "EFDCore":
            self.__create_efd_core()
        elif self.all_cores[self.properties.type] == "EPCore":
            self.__create_ep_core()
        elif self.all_cores[self.properties.type] == "PCore":
            self.__create_p_core()
        elif self.all_cores[self.properties.type] == "PQCore":
            self.__create_pq_core()
        elif self.all_cores[self.properties.type] == "UICore":
            self.__create_ui_core()
        else:
            logger.info("Core type not implemented.")
            return False

        list_objects_end = self.aedtapp.modeler.object_list

        ids_in_start = {obj.name for obj in list_objects_start}
        missing_obs = [obj for obj in list_objects_end if obj.name not in ids_in_start]

        self.objects_list_append(missing_obs)
        self.compute_volume()
        self.set_color(165, 42, 42)

        if self.volume == 0:
            logger.info("Core not created.")
            return False

        return True

    def __create_ui_core(self):
        """Create a UI core."""
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]
        dim_d6 = self.properties.dimensions["D_6"]
        dim_d7 = self.properties.dimensions["D_7"]
        dim_d8 = self.properties.dimensions["D_8"]
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        self.aedtapp.modeler.create_box(
            origin=[-(dim_d1 - dim_d2) / 4, -(dim_d5 / 2), (dim_d4 / 2) - dim_d3],
            sizes=[dim_d1, dim_d5, dim_d3],
            name="U_Core",
        )

        self.aedtapp.modeler.create_box(
            origin=[(dim_d1 - dim_d2) / 4, -(dim_d5 / 2), -dim_d4 / 2],
            sizes=[dim_d2, dim_d5, dim_d4],
            name="XSlot",
        )

        self.aedtapp.modeler.subtract(blank_list="U_Core", tool_list="XSlot", keep_originals=False)

        if airgap_center > 0:
            self.aedtapp.modeler.create_box(
                origin=[(dim_d1 - dim_d2) / 4, -dim_d5 / 2, (dim_d4 / 2) - 2 * airgap_center],
                sizes=[-(dim_d1 - dim_d2) / 2, dim_d5, 2 * airgap_center],
                name="AgC",
            )
            self.aedtapp.modeler.subtract(blank_list="U_Core", tool_list="AgC", keep_originals=False)

        if airgap_side > 0:
            self.aedtapp.modeler.create_box(
                origin=[dim_d2 + (dim_d1 - dim_d2) / 4, -dim_d5 / 2, (dim_d4 / 2) - 2 * airgap_side],
                sizes=[(dim_d1 - dim_d2) / 2, dim_d5, 2 * airgap_side],
                name="Ag_S",
            )
            self.aedtapp.modeler.subtract(blank_list="U_Core", tool_list="Ag_S", keep_originals=False)

        self.aedtapp.modeler.create_box(
            origin=[-(dim_d1 - dim_d2) / 4 + (dim_d1 - dim_d6) / 2, -dim_d7 / 2, (dim_d4 / 2) + 2 * airgap_both],
            sizes=[dim_d6, dim_d7, dim_d8],
            name="I_Core",
        )

        self.aedtapp.modeler.fit_all()

    def __create_pq_core(self):
        """Create a PQ core."""
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]
        dim_d6 = self.properties.dimensions["D_6"]
        dim_d7 = self.properties.dimensions["D_7"]
        dim_d8 = self.properties.dimensions["D_8"]
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-dim_d1 / 2, -dim_d8 / 2, -(dim_d4 / 2) - airgap_both],
            sizes=[(dim_d1 - dim_d6) / 2, dim_d8, (dim_d4 / 2) - airgap_side],
            name="PQ_Core_Bottom",
        )
        leg_connection = math.sqrt(((dim_d3 / 2) ** 2) - ((dim_d7 / 2) ** 2))
        vertices1 = [
            [-dim_d6 / 2, -0.4 * dim_d8, -(dim_d4 / 2) - airgap_both],
            [-dim_d6 / 2, 0.4 * dim_d8, -(dim_d4 / 2) - airgap_both],
            [-dim_d7 / 2, +leg_connection, -(dim_d4 / 2) - airgap_both],
            [-dim_d7 / 2, -leg_connection, -(dim_d4 / 2) - airgap_both],
        ]
        vertices1.append(vertices1[0])
        self.aedtapp.modeler.create_polyline(
            points=vertices1,
            segment_type=None,
            cover_surface=True,
            close_surface=True,
            name="Polyline1",
            xsection_num_seg=12,
        )
        self.aedtapp.modeler.sweep_along_vector(assignment="Polyline1", sweep_vector=[0, 0, (dim_d4 / 2) - airgap_side])

        self.aedtapp.modeler.unite(assignment=["PQ_Core_Bottom", "Polyline1"], keep_originals=False)

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -(dim_d5 / 2) - airgap_both,
            ],
            radius=dim_d2 / 2,
            height=dim_d5 / 2,
            num_sides=self.__segments_number,
            name="XCyl1",
        )

        self.aedtapp.modeler.subtract(blank_list="PQ_Core_Bottom", tool_list="XCyl1", keep_originals=False)
        self.aedtapp.modeler.duplicate_and_mirror(assignment="PQ_Core_Bottom", origin=[0, 0, 0], vector=[1, 0, 0])
        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -(dim_d4 / 2) - airgap_both,
            ],
            radius=dim_d3 / 2,
            height=dim_d4 / 2 - airgap_center,
            num_sides=self.__segments_number,
            name="XCyl2",
        )
        self.aedtapp.modeler.unite(assignment=["PQ_Core_Bottom", "PQ_Core_Bottom_1", "XCyl2"], keep_originals=False)
        self.aedtapp.modeler.duplicate_and_mirror(assignment="PQ_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])

        handle = self.aedtapp.modeler["PQ_Core_Bottom_2"]
        handle.name = "PQ_Core_Top"
        self.aedtapp.modeler.fit_all()

    def __create_p_core(self):
        """Create a P core."""
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]
        dim_d6 = self.properties.dimensions["D_6"]
        dim_d7 = self.properties.dimensions["D_7"]
        dim_d8 = self.properties.dimensions["D_8"]
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        if self.properties.type == "PH":
            dim_d4 *= 2
            dim_d5 *= 2

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -(dim_d4 / 2) - airgap_both,
            ],
            radius=dim_d1 / 2,
            height=(dim_d4 / 2) - airgap_side,
            num_sides=self.__segments_number,
            name=self.name + "_Core_Bottom",
        )

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -(dim_d5 / 2) - airgap_both,
            ],
            radius=dim_d2 / 2,
            height=dim_d5 / 2,
            num_sides=self.__segments_number,
            name="XCyl1",
        )
        self.aedtapp.modeler.subtract(blank_list=self.name + "_Core_Bottom", tool_list="XCyl1", keep_originals=False)

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -(dim_d5 / 2) - airgap_both,
            ],
            radius=dim_d3 / 2,
            height=dim_d5 / 2 - airgap_center,
            num_sides=self.__segments_number,
            name="XCyl2",
        )

        self.aedtapp.modeler.unite(assignment=[self.name + "_Core_Bottom", "XCyl2"], keep_originals=False)

        if dim_d6 != 0:
            handle = self.aedtapp.modeler.create_cylinder(
                orientation="Z",
                origin=[
                    0,
                    0,
                    -(dim_d4 / 2),
                ],
                radius=dim_d6 / 2,
                height=dim_d4 / 2,
                num_sides=self.__segments_number,
                name="Tool",
            )
            self.aedtapp.modeler.subtract(blank_list=self.name + "_Core_Bottom", tool_list="Tool", keep_originals=False)
        if dim_d7 != 0:
            handle = self.aedtapp.modeler.create_box(
                origin=[-dim_d1 / 2, -dim_d7 / 2, -(dim_d4 / 2) - airgap_both],
                sizes=[(dim_d1 - dim_d8) / 2, dim_d7, dim_d4 / 2],
                name="Slot1",
            )

            handle = self.aedtapp.modeler.create_box(
                origin=[dim_d1 / 2, -dim_d7 / 2, -(dim_d4 / 2) - airgap_both],
                sizes=[-(dim_d1 - dim_d8) / 2, dim_d7, dim_d4 / 2],
                name="Slot2",
            )
            self.aedtapp.modeler.subtract(
                blank_list=self.name + "_Core_Bottom", tool_list=["Slot1,Slot2"], keep_originals=False
            )
        self.aedtapp.modeler.duplicate_and_mirror(self.name + "_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])
        handle = self.aedtapp.modeler[self.name + "_Core_Bottom_1"]
        handle.name = self.name + "_Core_Top"

        if self.properties.type == "PT":
            handle = self.aedtapp.modeler.create_box(
                origin=[-dim_d1 / 2, -dim_d1 / 2, (dim_d4 / 2) - airgap_both],
                sizes=[(dim_d1 - dim_d8) / 2, dim_d1, dim_d4 / 2],
                name="Slot3",
            )

            handle = self.aedtapp.modeler.create_box(
                origin=[dim_d1 / 2, -dim_d1 / 2, (dim_d4 / 2) - airgap_both],
                sizes=[-(dim_d1 - dim_d8) / 2, dim_d1, dim_d4 / 2],
                name="Slot4",
            )
            self.aedtapp.modeler.subtract(
                blank_list=self.name + "_Core_Top", tool_list=["Slot3,Slot4"], keep_originals=False
            )
        self.aedtapp.modeler.fit_all()

    def __create_ep_core(self):
        """Create an EP core."""
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]
        dim_d6 = self.properties.dimensions["D_6"]
        dim_d7 = self.properties.dimensions["D_7"]
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-(dim_d1 / 2), -(dim_d6 / 2), -dim_d4 / 2 - airgap_both],
            sizes=[dim_d1, dim_d6, dim_d4 / 2 - airgap_side],
            name=self.name + "_Core_Bottom",
        )

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                (dim_d6 / 2) - dim_d7,
                -dim_d5 / 2 - airgap_both,
            ],
            radius=dim_d2 / 2,
            height=dim_d5 / 2,
            num_sides=self.__segments_number,
            name="XCyl1",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-dim_d2 / 2, (dim_d6 / 2) - dim_d7, -dim_d5 / 2 - airgap_both],
            sizes=[
                dim_d2,
                dim_d7,
                dim_d5 / 2,
            ],
            name="Box2",
        )

        self.aedtapp.modeler.unite(assignment="Box2,XCyl1", keep_originals=False)
        self.aedtapp.modeler.subtract(blank_list=self.name + "_Core_Bottom", tool_list="Box2", keep_originals=False)

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                (dim_d6 / 2) - dim_d7,
                -dim_d5 / 2 - airgap_both,
            ],
            radius=dim_d3 / 2,
            height=dim_d5 / 2,
            num_sides=self.__segments_number,
            name="XCyl2",
        )

        self.aedtapp.modeler.unite(assignment=[self.name + "_Core_Bottom", "XCyl2"], keep_originals=False)
        self.aedtapp.modeler.move(assignment=self.name + "_Core_Bottom", vector=[0, (-dim_d6 / 2.0) + dim_d7, 0])

        self.aedtapp.modeler.duplicate_and_mirror(self.name + "_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])
        handle = self.aedtapp.modeler[self.name + "_Core_Bottom_1"]
        handle.name = self.name + "_Core_Top"
        self.aedtapp.modeler.fit_all()

    def __create_efd_core(self):
        """Create an EFD core."""
        core_length = self.properties.dimensions["D_1"]
        core_width = self.properties.dimensions["D_6"]
        core_height = self.properties.dimensions["D_4"]
        side_leg_width = (self.properties.dimensions["D_1"] - self.properties.dimensions["D_2"]) / 2
        center_leg_width = self.properties.dimensions["D_3"]
        slot_depth = self.properties.dimensions["D_5"]
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-(core_length / 2), -(core_width / 2), -core_height - airgap_both],
            sizes=[core_length, core_width, core_height - slot_depth],
            name="E_Core_Bottom",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-(core_length / 2), -(core_width / 2), -core_height - airgap_both],
            sizes=[
                side_leg_width,
                core_width,
                core_height - airgap_side,
            ],
            name="Leg1",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-(center_leg_width / 2), -(core_width / 2), -core_height - airgap_both],
            sizes=[center_leg_width, core_width, core_height - airgap_center],
            name="Leg2",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[(core_length / 2) - side_leg_width, -(core_width / 2), -core_height - airgap_both],
            sizes=[side_leg_width, core_width, core_height - airgap_side],
            name="Leg3",
        )

        self.aedtapp.modeler.unite(assignment="E_Core_Bottom,Leg1,Leg2,Leg3", keep_originals=False)

        self.aedtapp.modeler.duplicate_and_mirror(assignment="E_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])

        handle = self.aedtapp.modeler["E_Core_Bottom_1"]
        handle.name = "E_Core_Top"
        self.aedtapp.modeler.fit_all()

    def __create_ei_core(self):
        """Create an EI core."""
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]
        dim_d6 = self.properties.dimensions["D_6"]
        dim_d7 = self.properties.dimensions["D_7"]
        dim_d8 = self.properties.dimensions["D_8"]

        core_length = dim_d1
        core_width = dim_d6
        core_height = dim_d4
        side_leg_width = (dim_d1 - dim_d2) / 2
        center_leg_width = dim_d3
        slot_depth = dim_d5
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-(core_length / 2), -(core_width / 2), -core_height],
            sizes=[core_length, core_width, (core_height - slot_depth)],
            name="E_Core",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-(core_length / 2), -(core_width / 2), -core_height],
            sizes=[side_leg_width, core_width, core_height - 2 * airgap_side],
            name="Leg1",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-(center_leg_width / 2), -(core_width / 2), -core_height],
            sizes=[center_leg_width, core_width, core_height - 2 * airgap_center],
            name="Leg2",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[(core_length / 2) - side_leg_width, -(core_width / 2), -core_height],
            sizes=[side_leg_width, core_width, core_height - 2 * airgap_side],
            name="Leg3",
        )

        self.aedtapp.modeler.unite(assignment="E_Core,Leg1,Leg2,Leg3", keep_originals=False)

        # Fillets
        pos_x = -dim_d1 / 2
        pos_y = -dim_d6 / 2
        pos_z = -(dim_d4 / 2) - 2 * airgap_both
        body_name = "E_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        pos_x = -dim_d1 / 2
        pos_y = dim_d6 / 2
        pos_z = -(dim_d4 / 2) - 2 * airgap_both
        body_name = "E_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        pos_x = dim_d1 / 2
        pos_y = -dim_d6 / 2
        pos_z = -(dim_d4 / 2) - 2 * airgap_both
        body_name = "E_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        pos_x = dim_d1 / 2
        pos_y = dim_d6 / 2
        pos_z = -(dim_d4 / 2) - 2 * airgap_both
        body_name = "E_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        # scale airgap by 2 due to no symmetry as in cores like in ECore (where due to mirror operation
        # we double airgap)
        handle = self.aedtapp.modeler.create_box(
            origin=[-dim_d1 / 2, -dim_d6 / 2, 2 * airgap_both],
            sizes=[dim_d1, dim_d6, dim_d8],
            name="I_Core",
        )

        # Fillets
        pos_x = -dim_d1 / 2
        pos_y = -dim_d6 / 2
        pos_z = (dim_d8 / 2) - 2 * airgap_both
        body_name = "I_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        pos_x = -dim_d1 / 2
        pos_y = dim_d6 / 2
        pos_z = (dim_d8 / 2) - 2 * airgap_both
        body_name = "I_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        pos_x = dim_d1 / 2
        pos_y = -dim_d6 / 2
        pos_z = (dim_d8 / 2) - 2 * airgap_both
        body_name = "I_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        pos_x = dim_d1 / 2
        pos_y = dim_d6 / 2
        pos_z = (dim_d8 / 2) - 2 * airgap_both
        body_name = "I_Core"
        radius = dim_d7
        edge_id = self.aedtapp.modeler.get_edgeid_from_position(position=[pos_x, pos_y, pos_z], assignment=body_name)
        handle = self.aedtapp.modeler[body_name]
        handle.fillet(edges=[edge_id], radius=radius)

        # TODO: remove it and change the position in the box I_cores
        self.aedtapp.modeler.move(assignment="E_Core,I_Core", vector=[0, 0, dim_d5 / 2])

        self.aedtapp.modeler.fit_all()

    def __create_u_core(self):
        # Local properties
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]

        # Air gap info
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-(dim_d1 - dim_d2) / 4, -(dim_d5 / 2), -dim_d3 - airgap_both],
            sizes=[dim_d1, dim_d5, dim_d3],
            name="U_Core_Bottom",
        )
        handle = self.aedtapp.modeler.create_box(
            origin=[(dim_d1 - dim_d2) / 4, -(dim_d5 / 2), -dim_d4 - airgap_both],
            sizes=[dim_d2, dim_d5, dim_d4],
            name="XSlot",
        )
        self.aedtapp.modeler.subtract(blank_list="U_Core_Bottom", tool_list="XSlot", keep_originals=False)

        if airgap_center > 0:
            handle = self.aedtapp.modeler.create_box(
                origin=[-(dim_d1 - dim_d2) / 4, -(dim_d5 / 2), -airgap_center],
                sizes=[(dim_d1 - dim_d2) / 2, dim_d5, airgap_center],
                name="AgC",
            )
            self.aedtapp.modeler.subtract(blank_list="U_Core_Bottom", tool_list="AgC", keep_originals=False)

        if airgap_side > 0:
            handle = self.aedtapp.modeler.create_box(
                origin=[
                    dim_d2 + (dim_d1 - dim_d2) / 4,
                    -dim_d5 / 2,
                    -airgap_side,
                ],
                sizes=[(dim_d1 - dim_d2) / 2, dim_d5, airgap_side],
                name="Ag_s",
            )
            self.aedtapp.modeler.subtract(blank_list="U_Core_Bottom", tool_list="Ag_s", keep_originals=False)

        self.aedtapp.modeler.duplicate_and_mirror(assignment="U_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])
        handle = self.aedtapp.modeler["U_Core_Bottom_1"]
        handle.name = "U_Core_Top"
        self.aedtapp.modeler.fit_all()

    def __create_rm_core(self):
        # Local properties
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = self.properties.dimensions["D_2"]
        dim_d3 = self.properties.dimensions["D_3"]
        dim_d4 = self.properties.dimensions["D_4"]
        dim_d5 = self.properties.dimensions["D_5"]
        dim_d6 = self.properties.dimensions["D_6"]
        dim_d7 = self.properties.dimensions["D_7"]
        dim_d8 = self.properties.dimensions["D_8"]
        dia = dim_d7 / math.sqrt(2)
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        vertices1 = [[-dim_d1 / 2, (dia - (dim_d1 / 2)), -airgap_side - airgap_both]]
        vertices1.append([-(dia / 2), (dia / 2), -airgap_side - airgap_both])
        vertices1.append([-(dim_d8 / 2), (dim_d8 / 2), -airgap_side - airgap_both])
        vertices1.append([(dim_d8 / 2), (dim_d8 / 2), -airgap_side - airgap_both])
        vertices1.append([(dia / 2), (dia / 2), -airgap_side - airgap_both])
        vertices1.append([dim_d1 / 2, (dia - (dim_d1 / 2)), -airgap_side - airgap_both])
        vertices1.append([dim_d1 / 2, -(dia - (dim_d1 / 2)), -airgap_side - airgap_both])
        vertices1.append([(dia / 2), -(dia / 2), -airgap_side - airgap_both])
        vertices1.append([(dim_d8 / 2), -(dim_d8 / 2), -airgap_side - airgap_both])
        vertices1.append([-(dim_d8 / 2), -(dim_d8 / 2), -airgap_side - airgap_both])
        vertices1.append([-(dia / 2), -(dia / 2), -airgap_side - airgap_both])
        vertices1.append([-dim_d1 / 2, -(dia - (dim_d1 / 2)), -airgap_side - airgap_both])
        vertices1.append(vertices1[0])

        self.aedtapp.modeler.create_polyline(
            points=vertices1,
            segment_type=None,
            cover_surface=True,
            close_surface=True,
            name="RM_Core_Bottom",
            xsection_num_seg=12,
        )

        self.aedtapp.modeler.sweep_along_vector(
            assignment="RM_Core_Bottom", sweep_vector=[0, 0, -(dim_d4 / 2) + airgap_side]
        )

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -(dim_d5 / 2) - airgap_both,
            ],
            radius=dim_d2 / 2,
            height=dim_d5 / 2,
            num_sides=self.__segments_number,
            name="XCyl1",
        )
        self.aedtapp.modeler.subtract(blank_list="RM_Core_Bottom", tool_list="XCyl1", keep_originals=False)

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[0, 0, -(dim_d5 / 2) - airgap_both],
            radius=dim_d3 / 2,
            height=dim_d5 / 2 - airgap_center,
            num_sides=self.__segments_number,
            name="XCyl2",
        )
        self.aedtapp.modeler.unite(assignment="RM_Core_Bottom,XCyl2", keep_originals=False)

        if dim_d6 != 0:
            handle = self.aedtapp.modeler.create_cylinder(
                orientation="Z",
                origin=[0, 0, -(dim_d4 / 2) - airgap_both],
                radius=dim_d6 / 2,
                height=dim_d4 / 2,
                num_sides=self.__segments_number,
                name="XCyl3",
            )
            self.aedtapp.modeler.subtract(blank_list="RM_Core_Bottom", tool_list="XCyl3", keep_originals=False)

        self.aedtapp.modeler.duplicate_and_mirror(assignment="RM_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])
        handle = self.aedtapp.modeler["RM_Core_Bottom_1"]
        handle.name = "RM_Core_Top"
        self.aedtapp.modeler.fit_all()

    def __create_e_core(self):
        # Local properties
        core_length = self.properties.dimensions["D_1"]
        core_width = self.properties.dimensions["D_6"]
        core_height = self.properties.dimensions["D_4"]
        side_leg_width = (self.properties.dimensions["D_1"] - self.properties.dimensions["D_2"]) / 2
        center_leg_width = self.properties.dimensions["D_3"]
        slot_depth = self.properties.dimensions["D_5"]

        # Air gap info
        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-(core_length / 2), -(core_width / 2), -core_height - airgap_both],
            sizes=[core_length, core_width, (core_height - slot_depth)],
            name="E_Core_Bottom",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[-(core_length / 2), -(core_width / 2), -core_height - airgap_both],
            sizes=[side_leg_width, core_width, core_height - airgap_side],
            name="Leg1",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[
                -(center_leg_width / 2),
                -(core_width / 2),
                -core_height - airgap_both,
            ],
            sizes=[
                center_leg_width,
                core_width,
                core_height - airgap_center,
            ],
            name="Leg2",
        )

        handle = self.aedtapp.modeler.create_box(
            origin=[(core_length / 2) - side_leg_width, -(core_width / 2), -core_height - airgap_both],
            sizes=[side_leg_width, core_width, core_height - airgap_side],
            name="Leg3",
        )

        self.aedtapp.modeler.unite(assignment="E_Core_Bottom,Leg1,Leg2,Leg3", keep_originals=False)
        self.aedtapp.modeler.duplicate_and_mirror(assignment="E_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1])
        handle = self.aedtapp.modeler["E_Core_Bottom_1"]
        handle.name = "E_Core_Top"
        self.aedtapp.modeler.fit_all()

    def __create_etd_core(self):
        # Local variables
        name = self.name
        dim_d1 = self.properties.dimensions["D_1"]
        dim_d2 = float(self.properties.dimensions["D_2"])
        dim_d3 = float(self.properties.dimensions["D_3"])
        dim_d4 = float(self.properties.dimensions["D_4"])
        dim_d5 = float(self.properties.dimensions["D_5"])
        dim_d6 = float(self.properties.dimensions["D_6"])
        dim_d7 = float(self.properties.dimensions["D_7"])

        airgap_both, airgap_center, airgap_side = self.air_gap(self.properties)

        handle = self.aedtapp.modeler.create_box(
            origin=[-(dim_d1 / 2), -(dim_d6 / 2), -dim_d4 - airgap_both],
            sizes=[dim_d1, dim_d6, dim_d4 - airgap_side],
            name=name + "_Core_Bottom",
        )

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[0, 0, -dim_d5 - airgap_both],
            radius=dim_d2 / 2,
            height=dim_d5,
            num_sides=self.__segments_number,
            name="XCyl1",
        )

        self.aedtapp.modeler.subtract(blank_list=name + "_Core_Bottom", tool_list="XCyl1", keep_originals=False)

        if self.properties.type == "ER" and dim_d7 > 0:
            handle = self.aedtapp.modeler.create_box(
                origin=[-dim_d7 / 2, -dim_d6 / 2, -dim_d5 - airgap_both], sizes=[dim_d7, dim_d6, dim_d5], name="Tool"
            )

            self.aedtapp.modeler.subtract(blank_list=self.name + "_Core_Bottom", tool_list="Tool", keep_originals=False)

        handle = self.aedtapp.modeler.create_cylinder(
            orientation="Z",
            origin=[
                0,
                0,
                -dim_d5 - airgap_both,
            ],
            radius=dim_d3 / 2,
            height=dim_d5 - airgap_center,
            num_sides=self.__segments_number,
            name="XCyl2",
        )

        self.aedtapp.modeler.unite(assignment=name + "_Core_Bottom,XCyl2", keep_originals=False)
        self.aedtapp.modeler.duplicate_and_mirror(
            assignment=self.name + "_Core_Bottom", origin=[0, 0, 0], vector=[0, 0, 1]
        )
        handle = self.aedtapp.modeler[name + "_Core_Bottom_1"]
        handle.name = str(name + "_Core_Top")
        self.aedtapp.modeler.fit_all()
