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


from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.bobbin import Bobbin
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.circuit import Circuit
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.core import Core
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.post_processing import PostProcessing
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.region import Region
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.setup import Setup
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding import Winding


class ETK:
    """Manages the whole electroninc transformer creation."""

    def __init__(
        self,
        aedtapp,
        core_properties,
        setup_definitions,
        winding_properties,
        materials,
        bobbin_properties,
        circuit_properties,
    ):
        """Initialize and launch the transformer component.

        Parameters
        ----------
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        core_properties : :class:`ansys.aedt.toolkits.common.properties.CoreProperties`
            Core properties.
        setup_definitions : :class:`ansys.aedt.toolkits.common.properties.SetupProperties`
            Setup properties.
        winding_properties : :class:`ansys.aedt.toolkits.common.properties.WindingProperties`
            Winding properties.
        materials : :class:`ansys.aedt.toolkits.common.properties.MaterialsProperties`
            Materials properties.
        bobbin_properties : :class:`ansys.aedt.toolkits.common.properties.BobbinProperties`
            Bobbin properties.
        circuit_properties : :class:`ansys.aedt.toolkits.common.properties.CircuitProperties`
            Circuit properties.
        """
        self.__aedt = aedtapp
        self.__core_properties = core_properties
        self.__setup_definitions = setup_definitions
        self.__winding_properties = winding_properties
        self.__materials = materials
        self.__bobbin_properties = bobbin_properties
        self.__circuit_properties = circuit_properties

    def create_model(self):
        """Create the transformer model."""
        # ------------------------------------------------------------
        # Setup
        # ------------------------------------------------------------
        osetup = Setup(self.__aedt, self.__setup_definitions, self.__winding_properties, self.__circuit_properties)
        osetup.create_setup()

        # ------------------------------------------------------------
        # Core
        # ------------------------------------------------------------

        ocore = Core("Core", self.__aedt, self.__core_properties, self.__setup_definitions)
        ocore.create_geometry()

        # Sets the core material
        ocore.set_material(self.__materials[self.__core_properties.material])

        if not ocore:
            logger.error("Core not created")
            return False

        # ------------------------------------------------------------
        # Windings
        # ------------------------------------------------------------
        owinding = Winding(
            "Windings",
            self.__aedt,
            self.__winding_properties,
            self.__core_properties,
            self.__setup_definitions,
            self.__bobbin_properties,
            self.__circuit_properties,
        )

        owinding.create_geometry()
        material_name = next(iter(self.__winding_properties.layers.values())).conductor.material
        owinding.set_material(self.__materials[material_name])
        owinding.create_terminal_sections()
        owinding.create_excitations()
        osetup.assign_matrix_winding()

        if not owinding:
            logger.error("Winding not created")
            return False

        # ------------------------------------------------------------
        # Bobbin
        # ------------------------------------------------------------
        # Creates the bobbin material

        obobbin = Bobbin(
            "Bobbin",
            self.__aedt,
            self.__bobbin_properties,
            self.__core_properties,
            self.__winding_properties,
            self.__setup_definitions,
        )

        obobbin.create_geometry()
        obobbin.set_material(self.__materials[self.__bobbin_properties.material])

        if not obobbin:
            logger.error("Bobbin not created")
            return False

        # ------------------------------------------------------------
        # Region
        # ------------------------------------------------------------
        oregion = Region(
            self.__aedt,
            self.__setup_definitions,
        )

        oregion.crete_geometry()

        if not oregion:
            logger.error("Region not created")
            return False

        # ------------------------------------------------------------
        # Mesh operations
        # ------------------------------------------------------------
        osetup.assign_mesh_operations(ocore, owinding)

        # ------------------------------------------------------------
        # Circuit
        # ------------------------------------------------------------
        ocircuit = Circuit(self.__aedt, self.__setup_definitions, self.__circuit_properties)

        ocircuit.create_circuit()

        # ------------------------------------------------------------
        # Symmetry
        # ------------------------------------------------------------
        osetup.apply_symmetry(ocore, owinding, obobbin)

        # ------------------------------------------------------------
        # Post-Processing
        # ------------------------------------------------------------
        opost_processing = PostProcessing(self.__aedt, ocore, owinding, osetup, self.__circuit_properties)
        opost_processing.create_post_processing()

        return True
