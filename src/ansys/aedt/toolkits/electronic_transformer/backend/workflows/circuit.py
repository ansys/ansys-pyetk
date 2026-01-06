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

from pathlib import PurePath

from ansys.aedt.core import MaxwellCircuit
from ansys.aedt.toolkits.electronic_transformer.backend.models import ExcitationType


class Circuit:
    """Manages circuit creation."""

    def __init__(self, aedtapp, setup_properties, circuit_properties):
        """Initialize and launch the circuit component.

        Parameters
        ----------
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        setup_properties : :class:`ansys.aedt.toolkits.common.properties.SetupProperties`
            Setup properties.
        circuit_properties : :class:`ansys.aedt.toolkits.common.properties.CircuitProperties`
            Circuit properties.
        """
        self.__aedt = aedtapp
        self.__excitation_type: ExcitationType = circuit_properties.excitation.type
        self.__excitation_value: float = circuit_properties.excitation.value
        self.__setup_properties = setup_properties
        self.__circuit_properties = circuit_properties

        self.__grid_cell_size = 0.00254
        self._id = 1000
        self.__page = 1
        self.__design_name = self.__aedt.design_name
        self.__maxwell_circuit_editor = MaxwellCircuit(design="circuit_" + self.__design_name)
        self.__schematic = self.__maxwell_circuit_editor.modeler.schematic
        self.__winding_connection = self.__circuit_properties.connections
        self.__resistance_list = self.__circuit_properties.side_loads
        self.__frequency = self.__setup_properties.analysis_setup.adaptive_frequency

    @staticmethod
    def __run_connection_reduction(connections):
        """Create a connection definition dictionary.

        This method unpacks nested elements of the same type. For example, a serial
        connection of a nested serial group is the same as all elements in series.

        Parameters
        ----------
        connections : dict
            Dictionary with the connection definitions.
        """

        def dict_walk(target_dict, conn_type=""):
            """Walk through the dictionary."""
            conn_type = conn_type[:1]
            for key, val in target_dict.items():
                if isinstance(val, dict):
                    if key[:1] == conn_type:
                        new_dict = target_dict.pop(key)
                        target_dict.update(new_dict)
                        return
                    else:
                        dict_walk(val, key)

        # loop until dictionaries after change are not the same
        dict2 = {}
        while dict2 != connections:
            dict2 = connections
            dict_walk(connections)

    @staticmethod
    def __validate_dict(target_dict):
        """Validate the dictionary to allow a single layer per transformer side.

        This method makes the current script compatible by assigning the layer to a
        serial connection.

        Parameters
        ----------
        target_dict : dict
            Dictionary where the layer may exist.
        """
        if len(target_dict) == 1:
            for key, val in target_dict.items():
                if not isinstance(val, dict):
                    target_dict.pop(key)
                    target_dict["S99999"] = {key: "Layer"}
                    break

    def get_comp_by_name(self, name):  # TODO: Needed for renaming of sides
        """Search for a component by its name.

        Parameters
        ----------
        name : str
            Name of the component.

        Returns
        -------
        list
            List of instance IDs.
        """
        result = self.editor.FindElements(
            ["NAME:SearchProps", "Prop:=", ["name", name, 2]],
            [
                "NAME:Parameters",
                "Filter:=",
                2,
                "MatchAll:=",
                False,
                "MatchCase:=",
                False,
                "SearchSubCkt:=",
                True,
                "SearchSelectionOnly:=",
                False,
            ],
        )
        return result

    def create_winding(self, winding_number, x, y):
        """Create a winding component and assign it a name.

        The name is the same as in the excitation.

        Parameters
        ----------
        winding_number : int
            Number of the winding to give the component a name.
        x : float
            Position on the X axis (unitless).
        y : float
            Position on the Y axis (unitless).

        Returns
        -------
        :class:`pyaedt.modeler.schematic.ObjectInSchematic`
            Winding component.
        """
        x *= self.__grid_cell_size * 4
        y *= self.__grid_cell_size * 3
        # component_name = schematic.create_winding(name="Layer_" + str(winding_number),
        # location=[x,y], angle=0, use_instance_id_netlist=False)

        component_name = self.__schematic.create_component(
            component_library="Dedicated Elements",
            component_name="Winding",
            location=[x, y],
            angle=0,
            page=("Page{}".format(self.__page)),
        )
        component_name.set_property("Name", "Layer_" + str(winding_number))
        return component_name

    def create_source_or_load(self, source_type, max_x):
        """Create a source or a load.

        Parameters
        ----------
        source_type : str
            Type of the source. Options are ``"Voltage"``, ``"Current"``, and ``"Load"``.
        max_x : float
            Maximum position on the X axis.
        """
        if source_type == "Voltage":
            x = 0
            y = -1
            x *= self.__grid_cell_size * 4
            y *= self.__grid_cell_size * 3
            component_name = self.__schematic.create_component(
                component_library="Sources",
                component_name="VSin",
                location=[x, y],
                angle=-90,
                page=("Page{}".format(self.__page)),
            )
            # TODO: Change to Voltage source when PyAEDT updated
            # component_name = schematic.create_resistor(name="VSin",location=[x,y],angle=-90)
        elif source_type == "Current":
            x = 0
            y = -1
            x *= self.__grid_cell_size * 4
            y *= self.__grid_cell_size * 3

            component_name = self.__schematic.create_component(
                component_library="Sources",
                component_name="ISin",
                location=[x, y],
                angle=90,
                page=("Page{}".format(self.__page)),
            )
        else:
            x = 0
            y = -1
            x *= self.__grid_cell_size * 4
            y *= self.__grid_cell_size * 3
            component_name = self.__schematic.create_component(
                component_library="Passive Elements",
                component_name="Res",
                location=[x, y],
                angle=0,
                page=("Page{}".format(self.__page)),
            )

        x_init = 1
        if source_type == "Voltage":
            component_name.parameters["Va"] = str(self.__excitation_value) + "V"
            component_name.parameters["VFreq"] = str(self.__frequency)
            component_name.parameters["Phase"] = str(0) + "deg"
            x = 1
            y = -1
            x *= self.__grid_cell_size * 4
            y *= self.__grid_cell_size * 3
            component_name = self.__schematic.create_component(
                component_library="Passive Elements",
                component_name="Res",
                location=[x, y],
                angle=0,
                page=("Page{}".format(self.__page)),
            )
            component_name.set_property("Name", "R")
            component_name.parameters["R"] = self.__resistance_list[self.__page - 1]

            x_init = 2
        elif source_type == "Current":  # TODO: Move these lines to initial setup of VSin and ISin components above
            component_name.parameters["Ia"] = str(self.__excitation_value) + "A"
            component_name.parameters["IFreq"] = self.__frequency
            component_name.parameters["Phase"] = str(0) + "deg"
        else:
            component_name.parameters["R"] = self.__resistance_list[self.__page - 1]

        self.__wire(x1=0, y1=-1, x2=0, y2=0)
        self.__wire(x1=max_x, y1=-1, x2=max_x, y2=0)
        self.__wire(x1=x_init, y1=-1, x2=max_x, y2=-1)

    def __wire(self, x1, y1, x2, y2):
        """Create a wire between two coordinates.

        Parameters
        ----------
        x1 : float
            Initial position on the X axis.
        y1 : float
            Initial position on the Y axis.
        x2 : float
            Final position on the X axis.
        y2 : float
            Final position on the Y axis.
        """
        x1 *= self.__grid_cell_size * 4
        y1 *= self.__grid_cell_size * 3
        x2 *= self.__grid_cell_size * 4
        y2 *= self.__grid_cell_size * 3

        x1 -= self.__grid_cell_size * 2
        x2 -= self.__grid_cell_size * 2

        (self.__schematic.create_wire(name="", points=[[x1, y1], [x2, y2]], page=("Page{}".format(self.__page))),)

    def __calc_xy(self, target_dict, conn_type=""):
        """Calculate the X and Y sizes of the connections dictionary.

        A serial connection adds to X, and a parallel connection adds to Y.
        The ``x_size`` is the number of serial elements, and ``y_size`` is the
        number of parallel elements.

        Parameters
        ----------
        target_dict : dict
            Dictionary with the reduced connections.
        conn_type : str, optional
            Type of the parent connection. The default is ``""``.

        Returns
        -------
        tuple
            X and Y coordinates (unitless) calculated for the nested circuit.
        """
        x = y = 0
        conn_type = conn_type[:1]
        for key, val in target_dict.items():
            if isinstance(val, dict):
                new_x, new_y = self.__calc_xy(val, key)

                if "S" in conn_type:
                    y = max(new_y, y)
                    x += new_x
                elif "P" in conn_type:
                    x = max(new_x, x)
                    y += new_y
            else:
                if "S" in conn_type:
                    x += 1
                elif "P" in conn_type:
                    y += 1

        # components take at least one cell, so add 1 if 0
        if x == 0:
            x += 1

        if y == 0:
            y += 1

        target_dict["x_size"] = x
        target_dict["y_size"] = y
        return x, y

    def __draw_circuit(self, target_dict, conn_type="", x=0, y=0, max_x=0):
        """Generate a circuit of parallel and serial windings, including nested circuits.

        Parameters
        ----------
        target_dict : dict
            Connections dictionary.
        conn_type : str, optional
            Connection type for the recursion cycle. The default is ``""``.
        x : float, optional
            Winding position on the X axis. The default is ``0``.
        y : float, optional
            Winding position on the Y axis. The default is ``0``.
        max_x : float, optional
            Maximum coordinate reached on the X axis. The default is ``0``.
        """
        conn_type = conn_type[:1]
        rel_x_pos = x  # save X coordinate as new relative origin

        def sort_func(arg):
            """Sort elements by XY sizes (serial/parallel).

            Parameters
            ----------
            arg : str
                Dictionary key.

            Returns
            -------
            int
                Value for sorting.
            """
            if "size" in arg:
                # size keys go to the beginning
                return -1

            if not isinstance(target_dict[arg], dict):
                # if it is just layer goes to the end
                return 1e5

            # and dictionaries sort by XY size
            if "P" in conn_type:
                return target_dict[arg]["x_size"]
            elif "S" in conn_type:
                return target_dict[arg]["y_size"]
            else:
                return 0

        # sort all keys the way that first come windings, then dictionaries by descending size order.
        # all work of function is based that serial/parallel branches are in descending size order
        all_keys = sorted(target_dict.keys(), key=sort_func, reverse=True)

        if "P" in conn_type:
            # if parallel connection we need to draw a vertical wire at the beginning of nested circuit and at the end
            self.__wire(x, y, x, y + target_dict["y_size"] - 1)
            self.__wire(x + 2 * target_dict["x_size"], y, x + 2 * target_dict["x_size"], y + target_dict["y_size"] - 1)
            max_x = target_dict["x_size"]  # save max_x in case if there are nested serial circuits inside

        for i, key in enumerate(all_keys):
            val = target_dict[key]

            if isinstance(val, dict):
                if i > 0:
                    prev_elem = target_dict[all_keys[i - 1]]
                    if isinstance(prev_elem, dict):
                        # if previous item is dictionary then we need to make an offset according to nested circuit size
                        if "P" in conn_type:
                            y += prev_elem["y_size"]
                        else:
                            x += prev_elem["x_size"] * 2  # factor of 2 due to number of windings + wire for each
                self.__draw_circuit(val, key, x, y, max_x)  # go into recursion

                if i == len(target_dict) - 3:
                    # last element in dict (last two are sizes)
                    if "S" in conn_type:
                        if x < 2 * (rel_x_pos + max_x - 1):
                            # draw horizontal wire (direction: right) till the end of nested circuit
                            self.__wire(x + 1, y, rel_x_pos + 2 * max_x, y)

            elif isinstance(val, str) and val.lower() == "layer":
                # if it is layer value then just draw winding
                self.create_winding(key, x, y)

                if "P" in conn_type:
                    if i != len(target_dict) - 3:
                        # if not last element draw one vertical wire 1 unit height at the beginning of component
                        self.__wire(x, y, x, y + 1)

                    if i < len(target_dict) - 3:
                        if target_dict["x_size"] > 1:
                            # if our function has nested serial circuits with size X we need to draw a horizontal wire
                            # Example:
                            # --~~~-------  # second parallel branch
                            # |          |  # connection between layers
                            # --~~~--~~~--  # first parallel branch with nested serial circuit
                            self.__wire(x + 2 * target_dict["x_size"], y, x + 2 * target_dict["x_size"], y + 1)

                            # and vertical wire at the end of nested circuit
                            self.__wire(x + 1, y, x + 2 * target_dict["x_size"], y)
                        else:
                            # if not, just draw one vertical wire at the end of component
                            self.__wire(x + 1, y, x + 1, y + 1)

                    if i == 0:
                        # first element is always the longest, draw one horizontal wire to the right
                        self.__wire(x + 1, y, x + 2, y)

                    y += 1  # increase Y since parallel connection
                elif "S" in conn_type:
                    x += 2
                    self.__wire(x - 1, y, x, y)

        self.__maxwell_circuit_editor.modeler.zoom_to_fit()

    def create_circuit(self):
        """Create a circuit for each side."""
        # sort by winding side first and iterate
        for winding, definition in sorted(self.__winding_connection.items(), key=lambda x: int(x[0])):
            self.__page = int(winding)  # set new page for each side: Primary, Secondary, etc
            if self.__page > 1:
                self.__maxwell_circuit_editor.modeler.oeditor.CreatePage("Page{}".format(self.__page))

            definition = dict(definition)
            self.__validate_dict(definition)
            self.__run_connection_reduction(definition)
            self.__calc_xy(definition)
            self.__draw_circuit(definition)

            for key, val in definition.items():
                if "S" in key or "P" in key:
                    max_x = val["x_size"]  # get maximum size of main circuit
                    break

            if self.__page == 1:
                source = "Voltage" if self.__excitation_type == ExcitationType.voltage else "Current"
                self.create_source_or_load(source, max_x * 2)
            else:
                self.create_source_or_load("Load", max_x * 2)

            self.__schematic.create_gnd(
                location=[-2 * self.__grid_cell_size, -4 * self.__grid_cell_size], page=("Page{}".format(self.__page))
            )

            circuit_design_name = "circuit_" + self.__design_name
            circuit_path = str(PurePath(self.__maxwell_circuit_editor.project_path) / str(circuit_design_name + ".sph"))

        self.__maxwell_circuit_editor.export_netlist_from_schematic(circuit_path)

        self.__aedt.edit_external_circuit(netlist_file_path=circuit_path, schematic_design_name=circuit_design_name)
