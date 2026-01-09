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


from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

import json

from ansys.aedt.toolkits.common.backend.api import AEDTCommon
from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.electronic_transformer.backend.models import BackendResetProperties
from ansys.aedt.toolkits.electronic_transformer.backend.models import ExcitationType
from ansys.aedt.toolkits.electronic_transformer.backend.models import Layer
from ansys.aedt.toolkits.electronic_transformer.backend.models import Material
from ansys.aedt.toolkits.electronic_transformer.backend.models import properties
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.bobbin import Bobbin
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.core import Core
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.etk import ETK
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.validation import Validation
from ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding import Winding


class ToolkitBackend(AEDTCommon):
    """Control the toolkit workflow.

    This class provides methods to connect to a selected design and create geometries.

    Examples
    --------
    >>> from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend
    >>> toolkit_api = ToolkitBackend()
    >>> toolkit_api.launch_aedt()
    >>> toolkit_api.wait_to_be_idle()
    >>> toolkit_api.create_core_geometry()
    """

    def __init__(self):
        """Initialize the ``ToolkitBackend`` class."""
        self.__reset_transformer_properties()
        AEDTCommon.__init__(self, properties)
        self.__input_props = None
        self.__validator = Validation()

    def __reset_transformer_properties(self):
        be_properties = BackendResetProperties()

        properties.core = be_properties.core
        properties.winding = be_properties.winding
        properties.bobbin = be_properties.bobbin
        properties.settings = be_properties.settings
        properties.materials = be_properties.materials
        properties.circuit = be_properties.circuit

        # properties.aedt_version: str = DEFAULT_AEDT_VERSION
        properties.non_graphical = False
        properties.active_project = ""
        properties.active_design = ""
        properties.project_list = []
        properties.design_list = {}
        properties.selected_process = 0
        properties.use_grpc = True
        properties.is_toolkit_busy = False
        properties.url = "127.0.0.1"
        properties.port = 5001
        properties.debug = True
        properties.toolkit_name = "common"
        properties.log_file = "common_backend.log"
        properties.state = ""
        properties.progress = 0

    def __read_core_properties(self):
        """Read core properties from the input data."""
        core_props = self.__input_props["core"]

        self.properties.core.supplier = core_props["supplier"]
        self.properties.core.type = core_props["type"]
        self.properties.core.model = core_props["model"]
        self.properties.core.material = core_props["material"]
        self.properties.core.dimensions = core_props["dimensions"]
        self.properties.core.airgap.define_airgap = core_props["airgap"]["define_airgap"]

        if self.properties.core.airgap.define_airgap:
            self.properties.core.airgap.airgap_on_leg = core_props["airgap"]["airgap_on_leg"]
            self.properties.core.airgap.airgap_value = core_props["airgap"]["airgap_value"]

    def __read_material_properties(self):
        """Read material properties from the input data."""
        materials = self.__input_props["materials"]

        for key_material, value_material in materials.items():
            # Creates a default material
            this_material = Material()

            this_material.name = key_material

            # Updates the default material only if there is data in the json file
            if "conductivity" in value_material:
                this_material.conductivity = float(value_material["conductivity"])

            if "density" in value_material:
                this_material.density = float(value_material["density"])

            if "mur" in value_material:
                if float(value_material["mur"]) == 0:
                    this_material.mur = 1.0
                else:
                    this_material.mur = float(value_material["mur"])

            if "epsr" in value_material:
                this_material.epsr = float(value_material["epsr"])

            if "power_ferrite_loss_params" in value_material:
                this_material.power_ferrite_loss_params.cm = float(value_material["power_ferrite_loss_params"]["cm"])
                this_material.power_ferrite_loss_params.x = float(value_material["power_ferrite_loss_params"]["x"])
                this_material.power_ferrite_loss_params.y = float(value_material["power_ferrite_loss_params"]["y"])

            if "mu(freq)" in value_material:
                this_material.mu_vs_freq_list = value_material["mu(freq)"]

            self.properties.materials[key_material] = this_material

    def __read_winding_properties(self):
        """Read winding properties from the input data."""
        winding_props = self.__input_props["winding"]

        self.properties.winding.layer_type = winding_props["layer_type"]
        self.properties.winding.layer_spacing = winding_props["layer_spacing"]
        self.properties.winding.top_margin = winding_props["top_margin"]
        self.properties.winding.side_margin = winding_props["side_margin"]

        # Layers
        for key_layer, value_layer in winding_props["layers"].items():
            this_layer = Layer()

            if "insulation" in value_layer:
                this_layer.insulation.material = value_layer["insulation"]["material"]
                this_layer.insulation.thickness = value_layer["insulation"]["thickness"]

            this_layer.conductor.draw_skin_layers = value_layer["conductor"]["draw_skin_layers"]
            this_layer.conductor.material = value_layer["conductor"]["material"]
            this_layer.conductor.type = value_layer["conductor"]["type"]

            if this_layer.conductor.type == "Rectangular":
                this_layer.conductor.height = value_layer["conductor"]["height"]
                this_layer.conductor.width = value_layer["conductor"]["width"]
            elif this_layer.conductor.type == "Circular":
                this_layer.conductor.diameter = value_layer["conductor"]["diameter"]

            this_layer.turns.quantity = value_layer["turns"]["quantity"]
            this_layer.turns.spacing = value_layer["turns"]["spacing"]
            this_layer.turns.distance = value_layer["turns"]["distance"]

            self.properties.winding.layers[key_layer] = this_layer

    def __read_bobbin_properties(self):
        """Read bobbin properties from the input data."""
        bobbin_props = self.__input_props["bobbin"]

        self.properties.bobbin.draw_bobbin = bobbin_props["draw_bobbin"]
        self.properties.bobbin.material = bobbin_props["material"]
        self.properties.bobbin.board_thickness = bobbin_props["board_thickness"]

    def __read_settings_properties(self):
        """Read settings properties from the input data."""
        setup_props = self.__input_props["settings"]

        self.properties.settings.full_model = setup_props["full_model"]
        self.properties.settings.region_offset = setup_props["region_offset"]
        self.properties.settings.segmentation_angle = setup_props["segmentation_angle"]
        self.properties.settings.analysis_setup.adaptive_frequency = setup_props["analysis_setup"]["adaptive_frequency"]
        self.properties.settings.analysis_setup.percentage_error = setup_props["analysis_setup"]["percentage_error"]
        self.properties.settings.analysis_setup.number_passes = setup_props["analysis_setup"]["number_passes"]
        self.properties.settings.analysis_setup.frequency_sweep.frequency_sweep = setup_props["analysis_setup"][
            "frequency_sweep"
        ]["frequency_sweep"]
        self.properties.settings.analysis_setup.frequency_sweep.start_frequency = setup_props["analysis_setup"][
            "frequency_sweep"
        ]["start_frequency"]
        self.properties.settings.analysis_setup.frequency_sweep.stop_frequency = setup_props["analysis_setup"][
            "frequency_sweep"
        ]["stop_frequency"]
        self.properties.settings.analysis_setup.frequency_sweep.samples = setup_props["analysis_setup"][
            "frequency_sweep"
        ]["samples"]
        self.properties.settings.analysis_setup.frequency_sweep.scale = setup_props["analysis_setup"][
            "frequency_sweep"
        ]["scale"]

    def __read_circuit_properties(self):
        """Read circuit properties from the input data."""
        circuit_props = self.__input_props["circuit"]

        self.properties.circuit.connections = circuit_props["connections"]
        self.properties.circuit.side_loads = circuit_props["side_loads"]

        self.properties.circuit.excitation.value = circuit_props["excitation"]["value"]

        if circuit_props["excitation"]["type"].lower() == "voltage":
            self.properties.circuit.excitation.type = ExcitationType.voltage
        elif circuit_props["excitation"]["type"].lower() == "current":
            self.properties.circuit.excitation.type = ExcitationType.current

    def __read_json_version(self):
        """Read circuit properties from the input data."""
        self.properties.json_version = self.__input_props["json_version"]

    def read_props_from_json(self, file_path):
        """Read properties from a JSON file.

        Parameters
        ----------
        file_path : str
            Path to the JSON file.
        """
        with Path.open(file_path) as f:
            json_read = json.load(f)
            self.__input_props = json_read

        self.__validator.validate_json(self.__input_props)
        self.__read_core_properties()
        self.__read_winding_properties()
        self.__read_bobbin_properties()
        self.__read_settings_properties()
        self.__read_material_properties()
        self.__read_circuit_properties()
        self.__read_json_version()

    def __read_props_from_frontend(self, frontend_properties):
        """Read properties from a the frontend.

        Parameters
        ----------
        frontend_properties : dict
           Dictionary with the FE data.
        """
        self.__input_props = {
            "json_version": frontend_properties["json_version"],
            "winding": frontend_properties["winding"],
            "core": frontend_properties["core"],
            "bobbin": frontend_properties["bobbin"],
            "settings": frontend_properties["settings"],
            "materials": frontend_properties["materials"],
            "circuit": frontend_properties["circuit"],
        }

        self.__validator.validate_json(self.__input_props)
        self.__read_core_properties()
        self.__read_winding_properties()
        self.__read_bobbin_properties()
        self.__read_settings_properties()
        self.__read_material_properties()
        self.__read_circuit_properties()
        self.__read_json_version()

    def create_core_geometry(self, frontend_properties=None):
        """Create the core geometry.

        Parameters
        ----------
        frontend_properties : dict, optional
            Frontend properties. The default is ``None``.

        Returns
        -------
        :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.core.Core`
            Core object.
        """
        if frontend_properties:
            self.__read_props_from_frontend(frontend_properties)

        self.connect_design("Maxwell3D")
        if self.aedtapp is None:
            logger.error("Not connected")
            return False

        ocore = Core("Core", self.aedtapp, properties.core, properties.settings)
        ocore.create_geometry()
        self.release_aedt()

        if not ocore:
            logger.error("Core not created")
            return False
        return ocore

    def create_winding_geometry(self, frontend_properties=None):
        """Create the winding geometry.

        Parameters
        ----------
        frontend_properties : dict, optional
            Frontend properties. The default is ``None``.

        Returns
        -------
        :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding.Winding`
            Winding object.
        """
        # Updates the backend data structure
        if frontend_properties:
            self.__read_props_from_frontend(frontend_properties)

        self.connect_design("Maxwell3D")
        if self.aedtapp is None:
            logger.error("Not connected")
            return False

        owinding = Winding(
            "Windings",
            self.aedtapp,
            properties.winding,
            properties.core,
            properties.settings,
            properties.bobbin,
            properties.circuit,
        )

        owinding.create_geometry()
        self.release_aedt()

        if not owinding:
            logger.error("Windings not created")
            return False
        return owinding

    def create_bobbin_geometry(self, frontend_properties=None):
        """Create the bobbin geometry.

        Parameters
        ----------
        frontend_properties : dict, optional
            Frontend properties. The default is ``None``.

        Returns
        -------
        :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.bobbin.Bobbin`
            Bobbin object.
        """
        # Updates the backend data structure
        if frontend_properties:
            self.__read_props_from_frontend(frontend_properties)

        self.connect_design("Maxwell3D")
        if self.aedtapp is None:
            logger.error("Not connected")
            return False

        obobbin = Bobbin(
            "Bobbin", self.aedtapp, properties.bobbin, properties.core, properties.winding, properties.settings
        )

        obobbin.create_geometry()
        self.release_aedt()

        if not obobbin:
            logger.error("Bobbin not created")
            return False
        return obobbin

    def create_model(self, frontend_properties=None):
        """Create the complete model.

        Parameters
        ----------
        frontend_properties : dict, optional
            Frontend properties. The default is ``None``.

        Returns
        -------
        :class:`ansys.aedt.toolkits.electronic_transformer.backend.workflows.etk.ETK`
            ETK object.
        """
        # Updates the backend data structure
        if frontend_properties:
            self.__read_props_from_frontend(frontend_properties)

        self.connect_design("Maxwell3D")
        if self.aedtapp is None:
            logger.error("Not connected")
            return False

        oetk = ETK(
            self.aedtapp,
            properties.core,
            properties.settings,
            properties.winding,
            properties.materials,
            properties.bobbin,
            properties.circuit,
        )

        oetk.create_model()
        self.release_aedt()

        if not oetk:
            logger.error("Model not created")
            return False
        return True

    def validate_json(self, data):
        validator = Validation()
        validator.validate_json(data)
