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

import json
import math
from pathlib import Path

from jsonschema import validate


class Validation:
    """Manages the validation of the input data."""

    def __init__(self):
        """Initialize and launch the validation component."""
        self.schema = Path(__file__).resolve().parents[1] / "backend" / "schemas" / "pyetk_schema.json"

    def __validate_core(self, core_properties):
        """Validate core dimensions and parameters.

        This method checks that all core dimensions are valid according to the core type.
        It validates that required dimensions are non-zero and that dimensions have the
        correct relationships (e.g., D_1 > D_2).

        Parameters
        ----------
        core_properties : properties of the core


        Returns
        -------
        list of str
            List of error messages. Empty list if validation passes.
            Each error message describes a specific validation failure.
        """
        d_1 = core_properties.dimensions["D_1"]
        d_2 = core_properties.dimensions["D_2"]
        d_3 = core_properties.dimensions["D_3"]
        d_4 = core_properties.dimensions["D_4"]
        d_5 = core_properties.dimensions["D_5"]
        d_6 = core_properties.dimensions["D_6"]
        d_7 = core_properties.dimensions["D_7"]
        d_8 = core_properties.dimensions["D_8"]

        error_message = []

        if d_1 == 0:
            error_message.append("Wrong core parameters: D_1 cannot be zero")
        if d_2 == 0:
            error_message.append("Wrong core parameters: D_2 cannot be zero")
        if d_3 == 0:
            error_message.append("Wrong core parameters: D_3 cannot be zero")
        if d_4 == 0:
            error_message.append("Wrong core parameters: D_4 cannot be zero")
        if d_5 == 0:
            error_message.append("Wrong core parameters: D_5 cannot be zero")
        if d_1 <= d_2:
            error_message.append("Wrong core parameters: D_1 must be greater than D_2")

        core_type = core_properties.type

        if core_type == "E":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")

        elif core_type == "EC":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")

        elif core_type == "EFD":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")

        elif core_type == "EI":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")

        elif core_type == "EP":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 <= d_7:
                error_message.append("Wrong core parameters: D_6 must be greater than D_7")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")

        elif core_type == "EQ":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 < d_3:
                error_message.append("Wrong core parameters: D_6 must be greater than D_3")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")

        elif core_type == "ER":
            if d_2 <= d_7:
                error_message.append("Wrong core parameters: D_2 must be greater than D_7")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_7 < 2 * math.sqrt((d_2 / 2) ** 2 - (d_6 / 2) ** 2) and d_7 != 0:
                error_message.append("Wrong core parameters: Please check D_7")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")

        elif core_type == "ETD":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")

        elif core_type == "P":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_3 <= d_6:
                error_message.append("Wrong core parameters: D_3 must be greater than D_6")
            if d_8 >= d_2:
                error_message.append("Wrong core parameters: D_8 must be less than D_2")
            if d_8 <= d_3:
                error_message.append("Wrong core parameters: D_8 must be greater than D_3")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")
            if d_8 == 0:
                error_message.append("Wrong core parameters: D_8 cannot be zero")

        elif core_type == "PH":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_3 <= d_6:
                error_message.append("Wrong core parameters: D_3 must be greater than D_6")
            if d_8 >= d_2:
                error_message.append("Wrong core parameters: D_8 must be less than D_2")
            if d_8 <= d_3:
                error_message.append("Wrong core parameters: D_8 must be greater than D_3")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")
            if d_8 == 0:
                error_message.append("Wrong core parameters: D_8 cannot be zero")

        elif core_type == "PQ":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_3 <= d_7:
                error_message.append("Wrong core parameters: D_3 must be greater than D_7")
            if d_6 >= d_1:
                error_message.append("Wrong core parameters: D_6 must be less than D_1")
            if d_6 <= d_3:
                error_message.append("Wrong core parameters: D_6 must be greater than D_3")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")
            if d_8 == 0:
                error_message.append("Wrong core parameters: D_8 cannot be zero")

        elif core_type == "PT":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_3 <= d_6:
                error_message.append("Wrong core parameters: D_3 must be greater than D_6")
            if d_8 >= d_2:
                error_message.append("Wrong core parameters: D_8 must be less than D_2")
            if d_8 <= d_3:
                error_message.append("Wrong core parameters: D_8 must be greater than D_3")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")
            if d_8 == 0:
                error_message.append("Wrong core parameters: D_8 cannot be zero")

        elif core_type == "RM":
            if d_2 <= d_3:
                error_message.append("Wrong core parameters: D_2 must be greater than D_3")
            if d_4 <= d_5:
                error_message.append("Wrong core parameters: D_4 must be greater than D_5")
            if d_3 <= d_6:
                error_message.append("Wrong core parameters: D_3 must be greater than D_6")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")
            if d_8 == 0:
                error_message.append("Wrong core parameters: D_8 cannot be zero")

        elif core_type == "U":
            if d_3 <= d_4:
                error_message.append("Wrong core parameters: D_3 must be greater than D_4")

        elif core_type == "UI":
            if d_3 <= d_4:
                error_message.append("Wrong core parameters: D_3 must be greater than D_4")
            if d_6 == 0:
                error_message.append("Wrong core parameters: D_6 cannot be zero")
            if d_7 == 0:
                error_message.append("Wrong core parameters: D_7 cannot be zero")
            if d_8 == 0:
                error_message.append("Wrong core parameters: D_8 cannot be zero")

        return error_message

    def __validate_winding(self, core_properties, winding_properties, bobbin_properties):
        """Validate winding configuration against core dimensions.

        This method checks whether the winding layers can physically fit within the core
        dimensions. It calculates the maximum width and height required by the winding
        configuration and compares it against the available space in the core.

        The validation handles two layer types:
        - Wound: Traditional wound windings where conductors wrap around the core
        - Planar: Planar windings where conductors are laid flat

        And two conductor types:
        - Rectangular: Conductors with width and height dimensions
        - Circular: Conductors with diameter dimension

        Parameters
        ----------
        core_properties : core properties
            Core model with dimensions and type. Used to determine available space
            for winding accommodation.
        winding_properties : winding properties
            Winding model with layers configuration. Contains:

        bobbin_properties : bobbin properties
            Bobbin model with board thickness. Used in calculating available space.

        Returns
        -------
        list of str
            List of error messages. Empty list if validation passes.
            Typical errors include:
            - "No layers defined in winding"
            - "Cannot accommodate all windings, increase D_5"
            - "Cannot accommodate all windings, increase D_2"
            - "Cannot accommodate all windings, increase D_4"
        """
        error_message = []

        side_margin = winding_properties.side_margin
        bobbin_board_thickness = bobbin_properties.board_thickness
        top_margin = winding_properties.top_margin
        layer_spacing = winding_properties.layer_spacing

        # Get conductor type from first layer (assuming all layers have same type)
        if not winding_properties.layers:
            error_message.append("No layers defined in winding")
            return error_message

        first_layer = next(iter(winding_properties.layers.values()))
        conductor_type = first_layer.conductor.type

        # ---- start checking for wound ---- #
        if winding_properties.layer_type == "Wound":
            # ---- Check possible width for wound---- #
            if conductor_type == "Rectangular":
                # take sum of layer dimensions where one layer is: Width + 2 * Insulation
                maximum_layer = (
                    sum(
                        [
                            layer.conductor.width
                            # do not forget that insulation is on both sides
                            + 2 * layer.insulation.thickness
                            + layer_spacing  # since number of layers - 1 for spacing)
                            for layer in winding_properties.layers.values()
                        ]
                    )
                    - layer_spacing
                )

            else:
                # conductor type: Circular
                maximum_layer = (
                    sum(
                        [
                            (layer.conductor.diameter + 2 * layer.insulation.thickness + layer_spacing)
                            for layer in winding_properties.layers.values()
                        ]
                    )
                    - layer_spacing
                )

            # do not forget that windings are laying on both sides of the core
            maximum_possible_width = 2 * (bobbin_board_thickness + side_margin + maximum_layer)

            # ---- Check possible height for wound---- #
            if conductor_type == "Rectangular":
                # max value from each layer: (Height + 2 * Insulation) * number of turns
                maximum_layer = max(
                    [
                        (
                            (
                                layer.conductor.height
                                # do not forget that insulation is on both sides
                                + 2 * layer.insulation.thickness
                            )
                            * layer.turns.quantity
                        )
                        for layer in winding_properties.layers.values()
                    ]
                )

            elif conductor_type == "Circular":
                maximum_layer = max(
                    [
                        ((layer.conductor.diameter + 2 * layer.insulation.thickness) * layer.turns.quantity)
                        for layer in winding_properties.layers.values()
                    ]
                )

            maximum_possible_height = 2 * bobbin_board_thickness + top_margin + maximum_layer
        # ---- Wound type limit found ---- #

        else:
            # layer type: Planar
            # ---- Check width for planar---- #
            maximum_layer = max(
                [
                    (
                        (
                            layer.conductor.width
                            # in this case it is turn spacing (no need to x2)
                            + layer.insulation.thickness
                        )
                        * layer.turns.quantity
                    )
                    for layer in winding_properties.layers.values()
                ]
            )
            maximum_possible_width = 2 * maximum_layer + 2 * side_margin

            # ---- Check Height for planar ---- #
            maximum_layer = (
                sum(
                    [
                        (layer.conductor.height + bobbin_board_thickness + layer_spacing)
                        for layer in winding_properties.layers.values()
                    ]
                )
                - layer_spacing
            )

            maximum_possible_height = maximum_layer + top_margin
            # ---- Planar type limit found ---- #

        # ---- Check accommodation not depending on layer type ---- #
        # ---- Height ---- #
        if core_properties.type in ["E", "EC", "EFD", "EQ", "ER", "ETD", "PH"]:
            # D_5 is height of one half core
            if maximum_possible_height > 2 * core_properties.dimensions["D_5"]:
                error_message.append("Cannot accommodate all windings, increase D_5")
        elif core_properties.type in ["EI", "EP", "P", "PT", "PQ", "RM"]:
            # D_5 is height of core
            if maximum_possible_height > core_properties.dimensions["D_5"]:
                error_message.append("Cannot accommodate all windings, increase D_5")
        elif core_properties.type == "UI":
            # D_4 is height of core
            if maximum_possible_height > core_properties.dimensions["D_4"]:
                error_message.append("Cannot accommodate all windings, increase D_4")
        elif core_properties.type == "U":
            # D_4 is height of core
            if maximum_possible_height > 2 * core_properties.dimensions["D_4"]:
                error_message.append("Cannot accommodate all windings, increase D_4")

        # ---- Width ---- #
        if core_properties.type not in ["U", "UI"]:
            # D_2 - D_3 is sum of dimensions of two slots for windings (left + right)
            if maximum_possible_width > (core_properties.dimensions["D_2"] - core_properties.dimensions["D_3"]):
                error_message.append("Cannot accommodate all windings, increase D_2")
        else:
            # D_2 is dimension of one side slot for winding
            if maximum_possible_width / 2 > core_properties.dimensions["D_2"]:
                error_message.append("Cannot accommodate all windings, increase D_2")

        return error_message

    def validate_model(self, core_properties, winding_properties, bobbin_properties):
        """Validate the complete transformer model including core and winding.

        This is the main validation method that orchestrates all validation checks
        for the transformer model. It validates both the core dimensions and the
        winding configuration, collecting all error messages from both validations.

        The validation process includes:
        1. Core validation: Checks that all core dimensions are valid for the core type
        2. Winding validation: Checks that windings can physically fit within the core

        Parameters
        ----------
        core_properties : Core properties

        winding_properties : Winding properties

        bobbin_properties : Bobbin properties


        Returns
        -------
        list of str
            List of all error messages from both core and winding validation.
            Empty list if all validations pass. Each error message describes
            a specific validation failure that must be corrected.

        Examples
        --------
        >>> validator = Validation()
        >>> errors = validator.validate_model(properties.core, properties.winding, properties.bobbin)
        >>> if errors:
        ...     print("Validation failed:")
        ...     for error in errors:
        ...         print(f"  - {error}")
        ... else:
        ...     print("Validation passed!")
        """
        error_messages = []

        # Validate core
        core_errors = self.__validate_core(core_properties)
        error_messages.extend(core_errors)

        # Validate winding
        winding_errors = self.__validate_winding(core_properties, winding_properties, bobbin_properties)
        error_messages.extend(winding_errors)

        return error_messages

    def validate_json(self, data):
        """Validate input data from a JSON file.

        Parameters
        ----------
        data : :class:`pathlib.Path`
            Path to the input data in JSON format.
        """
        with self.schema.open("r", encoding="utf-8") as file:
            schema = json.load(file)

        try:
            validate(instance=data, schema=schema)
        except Exception as e:
            raise Exception("Invalid input data:", e)
