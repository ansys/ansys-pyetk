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

import copy

from ansys.aedt.core.modules.boundary.maxwell_boundary import MatrixACMagnetic
from ansys.aedt.core.modules.boundary.maxwell_boundary import SourceACMagnetic
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.bobbin import Bobbin
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.core import Core
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding import Winding


class Setup:
    """Manages the model setup, including the AEDT settings."""

    def __init__(self, aedtapp, setup_def, winding_definitions, circuit_properties):
        """Initialize and launch the setup component.

        Parameters
        ----------
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        setup_def : :class:`ansys.aedt.toolkits.common.properties.SetupProperties`
            Setup properties.
        winding_definitions : :class:`ansys.aedt.toolkits.common.properties.WindingProperties`
            Winding properties.
        circuit_properties : :class:`ansys.aedt.toolkits.common.properties.CircuitProperties`
            Circuit properties.
        """
        self.__setup_definitions = setup_def
        self.__aedt = aedtapp
        self.__winding_definitions = winding_definitions
        self.__circuit_properties = circuit_properties
        self.__matrix = None

    @property
    def definitions(self):
        """Get the setup definitions."""
        return self.__setup_definitions

    def create_setup(self):
        """Create the AEDT setup."""
        self.__aedt.solution_type = "EddyCurrent"

        max_num_passes = self.__setup_definitions.analysis_setup.number_passes
        percent_error = self.__setup_definitions.analysis_setup.percentage_error
        adapt_freq = self.__setup_definitions.analysis_setup.adaptive_frequency
        sweep = self.__setup_definitions.analysis_setup.frequency_sweep

        if sweep.frequency_sweep:
            start_frequency = sweep.start_frequency
            stop_frequency = sweep.stop_frequency
            samples = sweep.samples

            if sweep.scale == "Linear":
                sweep_scale = "LinearCount"
            else:
                sweep_scale = "LogScale"

            self.insert_setup(
                max_num_passes=max_num_passes,
                percent_error=percent_error,
                frequency=str(adapt_freq) + "Hz",
                start_sweep_freq=start_frequency,
                stop_sweep_freq=stop_frequency,
                samples=samples,
                sweep_type=sweep_scale,
                frequency_sweep=sweep.frequency_sweep
            )

        else:
            self.insert_setup(max_num_passes=max_num_passes, percent_error=percent_error, frequency=adapt_freq,
                              frequency_sweep=sweep.frequency_sweep)

        return adapt_freq

    def insert_setup(
            self,
            max_num_passes,
            percent_error,
            frequency,
            sweep_type=None,
            start_sweep_freq=None,
            stop_sweep_freq=None,
            samples=None,
            frequency_sweep=False,
    ):
        """Create and configure an analysis setup in AEDT.

        Parameters
        ----------
        max_num_passes : int
            Maximum number of passes.
        percent_error : float
            Percentage of error.
        frequency : str
            Adaptive frequency.
        sweep_type : str, optional
            Type of sweep. The default is ``None``.
        start_sweep_freq : str, optional
            Start frequency for the sweep. The default is ``None``.
        stop_sweep_freq : str, optional
            Stop frequency for the sweep. The default is ``None``.
        samples : int, optional
            Number of samples. The default is ``None``.
         frequency_sweep: bool, optional,
          Whether the setup has a frequency sweep. The default is ``False``.
        """
        setup = self.__aedt.create_setup(name="Setup1")
        setup.props["MinimumPasses"] = 2
        setup.props["MaximumPasses"] = max_num_passes
        setup.props["MinimumConvergedPasses"] = 1
        setup.props["PercentError"] = percent_error
        setup.props["Frequency"] = frequency
        setup.props["PercentRefinement"] = 30
        setup.props["SolveFieldOnly"] = False
        setup.props["SolveMatrixAtLast"] = True
        setup.props["UseIterativeSolver"] = False
        setup.props["RelativeResidual"] = 0.0001
        setup.props["HasSweepSetup"] = frequency_sweep

        if frequency_sweep:
            setup.add_eddy_current_sweep(
                sweep_type=sweep_type,
                start_frequency=start_sweep_freq,
                stop_frequency=stop_sweep_freq,
                step_size=samples,
                units="Hz",
                save_all_fields=True,
            )

    def assign_matrix_winding(self):
        """Assign an RL matrix to a winding group."""
        signal_sources = []
        for n, _ in enumerate(self.__winding_definitions.layers.keys()):
            signal_sources.append(SourceACMagnetic(name=f"Layer_{n + 1}"))

        matrix_args = MatrixACMagnetic(signal_sources=signal_sources, matrix_name="Matrix1")
        self.__matrix = self.__aedt.assign_matrix(matrix_args)
        self.reduce_matrix()

    def reduce_matrix(self):
        """Run the matrix reduction algorithm."""

        def reduce(target_dict):
            """Run matrix reduction to join serial and parallel connections.

            Parameters
            ----------
            target_dict : dict
                Dictionary with the connections.

            Returns
            -------
            str
                Reduction string.
            """
            reduction_list = []
            for key, val in target_dict.items():
                if isinstance(val, dict):
                    new_red_str = reduce(val)
                    reduction_type = "Series" if "S" in key[:1] else "Parallel"
                    name = key.split("_", maxsplit=1)[1] if "Side" in key else key

                    # Includes the matrix reduction
                    new_red_list = new_red_str.split(",")
                    if reduction_type == "Series":
                        self.__matrix.join_series(sources=new_red_list, matrix_name="ReducedMatrix1", join_name=name)
                    elif reduction_type == "Parallel":
                        self.__matrix.join_parallel(sources=new_red_list, matrix_name="ReducedMatrix1", join_name=name)

                    reduction_list.append(key)
                else:
                    reduction_list.append("Layer_" + key)

            reduction_str = ",".join(reduction_list)
            return reduction_str

        # TODO: Decide if there is a need to remove this method or not
        # Note that this decision impacts another method deletion
        # def rename(side_num, side_definition):
        #     """
        #     rename winding and circuit element to be Side_XXX for better UX
        #     :param side_num: transformer side number
        #     :param side_definition: dict with single layer in it
        #     :return:
        #     """
        #     layer = "Layer_" + list(side_definition.keys())[0]
        #     self.__aedt.odesign.ChangeProperty(
        #         [
        #             "NAME:AllTabs",
        #             [
        #                 "NAME:Maxwell3D",
        #                 ["NAME:PropServers", "BoundarySetup:" + layer],
        #                 ["NAME:ChangedProps", ["NAME:Name", "Value:=", "Side_" + side_num]],
        #             ],
        #         ]
        #     )
        #     # self.circuit.change_prop(comp, "name", "Side_" + side_num)
        #     # also rename component in circuit
        #     comp = self.__aedt.oeditor.FindElements(
        #         ["NAME:SearchProps", "Prop:=", ["name", layer, 2]],
        #         [
        #             "NAME:Parameters",
        #             "Filter:=",
        #             2,
        #             "MatchAll:=",
        #             False,
        #             "MatchCase:=",
        #             False,
        #             "SearchSubCkt:=",
        #             True,
        #             "SearchSelectionOnly:=",
        #             False,
        #         ],
        #     )
        #     # comp = self.circuit.get_comp_by_name(layer)[0]
        #     # self.circuit.change_prop(comp, "name", "Side_" + side_num)
        #
        #     netlist_unit = ""
        #     units = ["NetlistUnits:=", netlist_unit] if netlist_unit else []
        #     self.editor.ChangeProperty(
        #         [
        #             "NAME:AllTabs",
        #             [
        #                 "NAME:PassedParameterTab",
        #                 ["NAME:PropServers", comp],
        #                 [
        #                     "NAME:ChangedProps",
        #                     ["NAME:" + "name", "OverridingDef:=", True, "Value:=", "Side_" + side_num + netlist_unit]
        #                     + units,
        #                 ],
        #             ],
        #         ]
        #     )

        connections = copy.deepcopy(self.__circuit_properties.connections)
        for side_num, side_def in connections.items():
            # Replace key and append name of the side for main key, for better UX
            main_connection = list(side_def.keys())[0]
            side_def[main_connection + "_Side_" + side_num] = side_def.pop(main_connection)

            reduce(side_def)

    def apply_symmetry(self, core: Core, winding: Winding, bobbin: Bobbin):
        """Apply symmetry to the model.

        Parameters
        ----------
        core : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.core.Core`
            Core object.
        winding : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding.Winding`
            Winding object.
        bobbin : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.bobbin.Bobbin`
            Bobbin object.
        """
        if not self.__setup_definitions.full_model:
            obs_list = []
            obs_list.extend(core.objects_list)
            obs_list.extend(winding.objects_list)
            obs_list.extend(winding.skin_layers_list)
            obs_list.extend(bobbin.objects_list)

            first_vertex_id_first_terminal = self.__aedt.modeler.get_object_vertices(winding.terminals_list[0])[0]
            x_coord = float(self.__aedt.modeler.get_vertex_position(first_vertex_id_first_terminal)[0])

            if x_coord >= 0:
                self.__aedt.modeler.mirror(assignment=winding.terminals_list, origin=[0, 0, 0], vector=[-1, 0, 0])

            self.__aedt.change_symmetry_multiplier(value=2)
            self.__aedt.modeler.split(assignment=obs_list, plane="YZ", sides="NegativeOnly", tool=None)

            self.__aedt.modeler.change_region_padding("0", padding_type="Percentage Offset", direction="+X")

            self.__aedt.modeler.fit_all()

    def assign_mesh_operations(self, core: Core, winding: Winding):
        """Assign mesh operations to the model.

        Parameters
        ----------
        core : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.core.Core`
            Core object.
        winding : :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding.Winding`
            Winding object.
        """
        dimension_list = []
        for each_dim_val in core.properties.dimensions.values():
            dimension_list.append(float(each_dim_val))
        mesh_op_sz = max(dimension_list) / 20.0

        self.__aedt.mesh.assign_length_mesh(assignment=core.objects_list, maximum_length=mesh_op_sz, name="Core")
        self.__aedt.mesh.assign_length_mesh(
            assignment=winding.objects_list, maximum_length=mesh_op_sz / 2, name="Layers"
        )
