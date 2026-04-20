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

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.core import Core
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.setup import Setup
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding import Winding


class PostProcessing:
    """Manages post-processing."""

    def __init__(self, aedtapp, core: Core, winding: Winding, setup: Setup, circuit_properties):
        """Initialize and launch the post-processing component.

        Parameters
        ----------
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        core : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.core.Core`
            Core object.
        winding : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding.Winding`
            Winding object.
        setup : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.setup.Setup`
            Setup object.
        circuit_properties : :class:`ansys.aedt.toolkits.common.properties.CircuitProperties`
            Circuit properties.
        """
        self.__core = core
        self.__winding = winding
        self.__setup = setup
        self.__aedt = aedtapp
        self.__circuit_properties = circuit_properties
        self.aedt_test = aedtapp

    def __get_objects_surfaces(self, object_list):
        """Get the surfaces of a list of objects.

        Parameters
        ----------
        object_list : list
            List of objects.

        Returns
        -------
        list
            List of surfaces.
        """
        surf_list = []
        for item in object_list:
            surf_list.append(self.__aedt.modeler.get_object_faces(assignment=item.name))
        flat_surf_list = []
        for xs in surf_list:
            for x in xs:
                flat_surf_list.append(x)

        return flat_surf_list

    def __creat_3d_field_plot(self):
        """Create a 3D field plot."""
        intrinsic_dict = {
            "Freq": str(self.__setup.definitions.analysis_setup.adaptive_frequency) + "Hz",
            "Phase": "0deg",
        }

        # Windings
        surface_list = self.__get_objects_surfaces(self.__winding.objects_list)

        self.__aedt.post.create_fieldplot_surface(
            assignment=surface_list,
            quantity="Mag_J",
            intrinsics=intrinsic_dict,
            plot_name="J",
        )

        ohmic_plot = self.__aedt.post.create_fieldplot_surface(
            assignment=surface_list,
            quantity="Ohmic_Loss",
            intrinsics=intrinsic_dict,
            plot_name="Ohmic_Loss",
        )

        # Core
        surface_list = self.__get_objects_surfaces(self.__core.objects_list)

        self.__aedt.post.create_fieldplot_surface(
            assignment=surface_list,
            quantity="Mag_B",
            intrinsics=intrinsic_dict,
            plot_name="B",
        )

        self.__aedt.post.create_fieldplot_surface(
            assignment=surface_list,
            quantity="Core_Loss",
            intrinsics=intrinsic_dict,
            plot_name="Core_Loss",
        )

        # Save project first before applying log scale to Ohmic_Loss plot from folder_settings.
        self.__aedt.save_project()
        ohmic_plot.folder_settings.scale_settings.log = True
        ohmic_plot.folder_settings.update()

    def create_post_processing(self):
        """Create the post-processing."""
        self.__creat_3d_field_plot()
        self.__create_leakage_plot()

    def __create_leakage_plot(self):
        """Create equations to calculate leakage inductance.

        For an N-winding transformer, there are ``N*(N-1)/2`` equations.
        """
        connections = self.__circuit_properties.connections
        all_leakages = {}

        for key_x, val_x in connections.items():
            next_key = list(val_x.keys())[0]
            if "P" in next_key or "S" in next_key:
                # connection_str_x = "Side"
                x = key_x
            # else:
            # connection_str_x = "Layer"
            # x = next_key

            for key_y, val_y in connections.items():
                next_key = list(val_y.keys())[0]
                if "P" in next_key or "S" in next_key:
                    # connection_str_y = "Side"
                    y = key_y
                # else:
                # connection_str_y = "Layer"
                # y = next_key

                if int(x) < int(y):
                    coupling_coef = f"CplCoef(Side_{x},Side_{y})"
                    equation = f"L(Side_{x},Side_{x})*(1-sqr({coupling_coef}))"
                    all_leakages[f"Leakage_Inductance_Side_{x},Side_{y}"] = equation

        plot_name = "PyETK Leakage_Inductance"
        report = self.aedt_test.post.create_report(
            plot_name=plot_name,
            domain="Sweep",
            expressions=list(all_leakages.values()),
            primary_sweep_variable="Freq",
            plot_type="Data Table",
            context={"Matrix1": "ReducedMatrix1"},
        )

        for key, val in all_leakages.items():
            for each_trace in report.traces:
                if each_trace.name == val:
                    each_trace.curve_properties["Number Format"] = "Scientific"
                    each_trace.name = key
