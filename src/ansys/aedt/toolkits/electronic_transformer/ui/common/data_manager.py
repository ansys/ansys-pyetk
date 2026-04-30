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

from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import database_manager
from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import freq_scale
from ansys.aedt.toolkits.electronic_transformer.ui.models import AirGapConfig
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import gui_properties


class DataManager:
    def __init__(self):
        self.properties = fe_properties
        self.gui_properties = gui_properties
        self.supported_json = "0.1.0"
        self.database_manager = database_manager

    def create_backend_data(self):
        """Collate data from the UI and organize it in a structure that the BE consumes."""
        # Initialize model to be sent to the backend
        model = {}

        # Build each section of the data separately
        version_update = {"json_version": self.supported_json}

        core_update = {
            "core": {
                "supplier": self.properties.core.supplier,
                "type": self.properties.core.type,
                "model": self.properties.core.model,
                "material": self.properties.core.material,
                "dimensions": self.properties.core.dimensions,
                "airgap": {
                    "define_airgap": self.properties.core.airgap.enabled,
                    "airgap_on_leg": self.properties.core.airgap.location,
                    "airgap_value": self.properties.core.airgap.height,
                },
            }
        }

        winding_update = {
            "winding": {
                "layer_type": self.properties.winding.layers.type,
                "layer_spacing": self.properties.winding.layers.spacing,
                "top_margin": self.properties.winding.top_margin,
                "side_margin": self.properties.winding.side_margin,
                "layers": self.properties.winding.layers.definition_per_layer,
            }
        }

        bobbin_update = {
            "bobbin": {
                "draw_bobbin": self.properties.bobbin.enabled,
                "board_thickness": self.properties.bobbin.thickness,
                "material": self.properties.bobbin.material,
            }
        }

        circuit_update = {
            "circuit": {
                "connections": self.properties.circuit.connections_definition,
                "side_loads": self.properties.circuit.side_loads,
                "excitation": {
                    "type": self.properties.circuit.excitation.type.lower(),
                    "value": self.properties.circuit.excitation.value,
                },
            }
        }

        settings_update = {
            "settings": {
                "analysis_setup": {
                    "adaptive_frequency": self.properties.settings.adaptive_frequency,
                    "frequency_sweep": {
                        "frequency_sweep": self.properties.settings.frequency_sweep_definition["frequency_sweep"],
                        "samples": self.properties.settings.frequency_sweep_definition["samples"],
                        "scale": self.properties.settings.frequency_sweep_definition["scale"],
                        "start_frequency": self.properties.settings.frequency_sweep_definition["start_frequency"],
                        "stop_frequency": self.properties.settings.frequency_sweep_definition["stop_frequency"],
                    },
                    "number_passes": self.properties.settings.number_passes,
                    "percentage_error": self.properties.settings.percentage_error,
                },
                "full_model": self.properties.settings.full_model,
                "region_offset": self.properties.settings.offset,
                "segmentation_angle": self.properties.settings.segmentation_angle,
            }
        }

        material_update = {"materials": self.properties.materials}

        # Build model main dictionary
        model.update(version_update)
        model.update(core_update)
        model.update(winding_update)
        model.update(bobbin_update)
        model.update(circuit_update)
        model.update(settings_update)
        model.update(material_update)

        return model

    def _format_input_version(self, data):
        """Format the json input version.

        The json input file is versioned. This method handles the input into the UI.
        It also handles the legacy ACT json format.
        Args:
            data (dict): The input data.

        Returns
        -------
            str: Message informing data version used.

        """
        if "json_version" in data.keys():
            if data["json_version"] >= self.supported_json:
                self.gui_properties.core.supplier = data["core"]["supplier"]
                self.gui_properties.core.type = data["core"]["type"]
                self.gui_properties.core.model = data["core"]["model"]
                self.gui_properties.core.material = data["core"]["material"]
                self.gui_properties.core.dimensions = data["core"]["dimensions"]
                self.gui_properties.core.airgap.enabled = data["core"]["airgap"]["define_airgap"]
                self.gui_properties.core.airgap.height = data["core"]["airgap"]["airgap_value"]
                self.gui_properties.core.airgap.location = data["core"]["airgap"]["airgap_on_leg"]

                self.gui_properties.settings.include_bobbin = data["bobbin"]["draw_bobbin"]
                self.gui_properties.bobbin_board_and_margin.thickness = data["bobbin"]["board_thickness"]
                self.gui_properties.bobbin_board_and_margin.material = data["bobbin"]["material"]
                self.gui_properties.winding.layer_type = data["winding"]["layer_type"]
                self.gui_properties.winding.layer_spacing = data["winding"]["layer_spacing"]
                self.gui_properties.bobbin_board_and_margin.top_margin = data["winding"]["top_margin"]
                self.gui_properties.bobbin_board_and_margin.side_margin = data["winding"]["side_margin"]

                self.gui_properties.settings.full_model = data["settings"]["full_model"]
                self.gui_properties.settings.offset = data["settings"]["region_offset"]
                self.gui_properties.settings.segmentation_angle = data["settings"]["segmentation_angle"]
                self.gui_properties.electrical.adaptive_frequency = data["settings"]["analysis_setup"][
                    "adaptive_frequency"
                ]
                self.gui_properties.settings.percentage_error = data["settings"]["analysis_setup"]["percentage_error"]
                self.gui_properties.settings.number_passes = data["settings"]["analysis_setup"]["number_passes"]
                self.gui_properties.settings.frequency_sweep_definition = data["settings"]["analysis_setup"][
                    "frequency_sweep"
                ]
                self.gui_properties.settings.frequency_sweep_definition.start_frequency_unit = "Hz"
                self.gui_properties.settings.frequency_sweep_definition.stop_frequency_unit = "Hz"

                self.gui_properties.electrical.excitation_strategy = data["circuit"]["excitation"]["type"]
                if self.gui_properties.electrical.excitation_strategy.lower() == "voltage":
                    self.gui_properties.electrical.voltage = data["circuit"]["excitation"]["value"]
                    self.gui_properties.electrical.current = 0
                    self.gui_properties.electrical.excitation_value = data["circuit"]["excitation"]["value"]
                else:
                    self.gui_properties.electrical.current = data["circuit"]["excitation"]["value"]
                    self.gui_properties.electrical.voltage = 0
                    self.gui_properties.electrical.excitation_value = data["circuit"]["excitation"]["value"]

                self.gui_properties.winding.connections_definition = data["circuit"]["connections"]
                self.gui_properties.winding.layer_side_definition = self._flatten_connections(
                    self.gui_properties.winding.connections_definition
                )
                self._set_layers_from_json(data["winding"]["layers"])
                self.gui_properties.winding.side_loads = data["circuit"]["side_loads"]

                msg = "Working with .json version: " + str(data["json_version"])
                return msg
            else:
                return ".json version " + str(data["json_version"]) + " Not Supported"

        else:
            self.gui_properties.core.supplier = data["core_dimensions"]["supplier"]
            self.gui_properties.core.type = data["core_dimensions"]["core_type"]
            self.gui_properties.core.model = data["core_dimensions"]["core_model"]
            self.gui_properties.core.dimensions = {
                "D_1": data["core_dimensions"]["D_1"],
                "D_2": data["core_dimensions"]["D_2"],
                "D_3": data["core_dimensions"]["D_3"],
                "D_4": data["core_dimensions"]["D_4"],
                "D_5": data["core_dimensions"]["D_5"],
                "D_6": data["core_dimensions"]["D_6"],
                "D_7": data["core_dimensions"]["D_7"],
                "D_8": data["core_dimensions"]["D_8"],
            }

            _airgap = AirGapConfig()
            _airgap.enabled = data["core_dimensions"]["airgap"].get("define_airgap", False)
            _airgap.location = data["core_dimensions"]["airgap"].get("airgap_on_leg", "None")
            _airgap.height = data["core_dimensions"]["airgap"].get("airgap_value", 0.0)
            self.gui_properties.core.airgap = _airgap

            self.gui_properties.settings.segmentation_angle = data["core_dimensions"]["segmentation_angle"]
            self.gui_properties.winding.conductor_material = data["setup_definition"]["coil_material"]
            self.gui_properties.settings.draw_skin_layers = data["setup_definition"]["draw_skin_layers"]
            self.gui_properties.winding.layer_type = data["winding_definition"]["layer_type"]
            self.gui_properties.winding.number_of_layers = data["winding_definition"]["number_of_layers"]
            self.gui_properties.winding.layer_spacing = data["winding_definition"]["layer_spacing"]
            self.gui_properties.bobbin_board_and_margin.thickness = data["winding_definition"]["bobbin_board_thickness"]
            self.gui_properties.bobbin_board_and_margin.top_margin = data["winding_definition"]["top_margin"]
            self.gui_properties.bobbin_board_and_margin.side_margin = data["winding_definition"]["side_margin"]
            self.gui_properties.winding.conductor_type = data["winding_definition"]["conductor_type"]
            self.gui_properties.settings.include_bobbin = data["winding_definition"]["include_bobbin"]
            self.gui_properties.winding.layers_definition = data["winding_definition"]["layers_definition"]

            self.gui_properties.core.material = data["setup_definition"]["core_material"]
            self.gui_properties.electrical.adaptive_frequency = data["setup_definition"]["adaptive_frequency"]
            self.gui_properties.settings.percentage_error = data["setup_definition"]["percentage_error"]
            self.gui_properties.settings.number_passes = data["setup_definition"]["number_passes"]
            self.gui_properties.winding.side_loads = data["setup_definition"]["side_loads"]
            self.gui_properties.electrical.excitation_strategy = data["setup_definition"]["excitation_strategy"]
            if self.gui_properties.electrical.excitation_strategy.lower() == "voltage":
                self.gui_properties.electrical.voltage = data["setup_definition"]["voltage"]
                self.gui_properties.electrical.excitation_value = data["setup_definition"]["voltage"]
                self.gui_properties.electrical.current = 0
            else:
                self.gui_properties.electrical.current = data["setup_definition"]["current"]
                self.gui_properties.electrical.excitation_value = data["setup_definition"]["current"]
                self.gui_properties.electrical.voltage = 0
            self.gui_properties.settings.offset = data["setup_definition"]["offset"]
            self.gui_properties.settings.full_model = data["setup_definition"]["full_model"]
            self.gui_properties.settings.frequency_sweep_definition = data["setup_definition"][
                "frequency_sweep_definition"
            ]

            self.gui_properties.winding.connections_definition = data["setup_definition"]["connections_definition"]
            self.gui_properties.winding.layer_side_definition = data["setup_definition"]["layer_side_definition"]

            msg = "Input in Legacy Format. Save data in new format."
            return msg

    def _set_layers_from_json(self, data):
        """Set winding layers from a JSON file.

        Args:
            data (dict): The JSON data.

        """
        # Layers
        layers = {}
        for i, (key_layer, value_layer) in enumerate(data.items()):
            layers[key_layer] = {
                "turns_number": value_layer["turns"]["quantity"],
                "segments_number": self.gui_properties.settings.segments_number,
            }

            if self.gui_properties.winding.layer_type.lower() == "wound":
                layers[key_layer].update(
                    {"insulation_thickness": value_layer.get("insulation", {}).get("thickness", 0.0)}
                )
            if self.gui_properties.winding.layer_type.lower() == "planar":
                layers[key_layer].update({"turn_spacing": value_layer["turns"].get("distance", 0.0)})

            if value_layer["conductor"].get("diameter", 0.0) != 0.0:
                layers[key_layer].update({"conductor_diameter": value_layer["conductor"]["diameter"]})
            else:
                layers[key_layer].update({"conductor_width": value_layer["conductor"]["width"]})
                layers[key_layer].update({"conductor_height": value_layer["conductor"]["height"]})

            if i == 0:
                self.gui_properties.winding.conductor_type = value_layer["conductor"]["type"]
                self.gui_properties.settings.draw_skin_layers = value_layer["conductor"]["draw_skin_layers"]
                self.gui_properties.winding.conductor_material = value_layer["conductor"]["material"]
                self.gui_properties.winding.insulation_material = value_layer.get("insulation", {}).get("material", "")
        self.gui_properties.winding.layers_definition = layers

    def _flatten_connections(self, connections_def):
        """Flatten the connections definition for easy manipulation.

        Args:
            connections_def (dict): The connections definition.

        Returns
        -------
            dict: The flattened connections definition.

        """
        flattened_connections = {}
        for outer_key, inner_dict in connections_def.items():
            collected_keys = []
            for subdict_key, subdict in inner_dict.items():
                if isinstance(subdict, dict):
                    for k, v in subdict.items():
                        if v == "Layer":
                            collected_keys.append(k)
                else:
                    collected_keys.append(subdict_key)
            flattened_connections[outer_key] = collected_keys
        return flattened_connections

    def _import_data_from_json(self, file):
        """Import data from a JSON file.

        Args:
            file (pathlib.Path): The path to the JSON file.

        Returns
        -------
            str: Message informing validity of input data.

        """
        if file.is_file():
            with file.open("r") as f:
                data = json.load(f)
                msg = self._format_input_version(data)
                is_valid = True

        else:
            msg = "Incompatible/Not Selected JSON file"
            is_valid = False

        return msg, is_valid

    def _create_layers_for_backend(self, layers):
        """Create a layers dictionary for the backend format.

        Args:
            layers (dict): The layers dictionary from the frontend.

        Returns
        -------
            dict: The layers dictionary for the backend.
        """
        be_layers = {}
        nlayers = len(layers)
        for n in range(1, nlayers + 1):
            be_layers[f"layer_{n}"] = {
                "conductor": {
                    "draw_skin_layers": self.gui_properties.settings.draw_skin_layers,
                    "material": self.gui_properties.winding.conductor_material,
                    "type": self.gui_properties.winding.conductor_type,
                },
                "turns": {
                    "quantity": layers[f"layer_{n}"]["turns_number"],
                    "spacing": "top",
                    "distance": layers[f"layer_{n}"].get("turn_spacing", 0.0),
                },
            }

            # update insulation only if available in model
            if self.gui_properties.winding.conductor_type.lower() == "wound":
                layers[f"layer_{n}"].update(
                    {
                        "insulation": {
                            "thickness": layers[f"layer_{n}"].get("insulation_thickness", 0.0),
                            "material": self.gui_properties.winding.insulation_material,
                        }
                    }
                )

            # depending on conductor cross section populate dimensions
            if self.gui_properties.winding.conductor_type.lower() == "circular":
                be_layers[f"layer_{n}"]["conductor"].update({"diameter": layers[f"layer_{n}"]["conductor_diameter"]})

            if self.gui_properties.winding.conductor_type.lower() == "rectangular":
                be_layers[f"layer_{n}"]["conductor"].update({"width": layers[f"layer_{n}"]["conductor_width"]})
                be_layers[f"layer_{n}"]["conductor"].update({"height": layers[f"layer_{n}"]["conductor_height"]})
        return be_layers

    def _update_frontend_properties(self):
        """Update frontend properties with current UI entries.

        This method fetches data from the UI and populates the frontend ``Property`` data structure.
        """
        # Core Properties from UI
        self.properties.core.supplier = self.gui_properties.core.supplier
        self.properties.core.type = self.gui_properties.core.type
        self.properties.core.model = self.gui_properties.core.model

        # Populate front end properties core dimensions with float
        self.properties.core.dimensions = {
            key: float(value) for key, value in self.gui_properties.core.dimensions.items()
        }

        self.properties.core.material = self.gui_properties.core.material
        self.properties.core.airgap.enabled = (
            self.gui_properties.core.airgap.location != "None"
        )  # Center, Side, or Both
        self.properties.core.airgap.location = self.gui_properties.core.airgap.location
        self.properties.core.airgap.height = self.gui_properties.core.airgap.height

        # Winding Properties from UI
        self.properties.winding.layers.type = self.gui_properties.winding.layer_type
        self.properties.winding.layers.spacing = self.gui_properties.winding.layer_spacing
        self.properties.winding.layers.definition_per_layer = self._create_layers_for_backend(
            self.gui_properties.winding.layers_definition
        )
        self.properties.winding.layers.number_of_layers = len(self.gui_properties.winding.layers_definition)

        self.properties.winding.conductor.cross_section = self.gui_properties.winding.conductor_type
        self.properties.winding.conductor.enabled_skin_depth_mesh = self.gui_properties.settings.draw_skin_layers
        self.properties.winding.conductor.material = self.gui_properties.winding.conductor_material

        # Bobbin Properties from UI
        self.properties.bobbin.enabled = self.gui_properties.settings.include_bobbin
        self.properties.bobbin.thickness = self.gui_properties.bobbin_board_and_margin.thickness
        self.properties.bobbin.material = self.gui_properties.bobbin_board_and_margin.material
        self.properties.winding.top_margin = self.gui_properties.bobbin_board_and_margin.top_margin
        self.properties.winding.side_margin = self.gui_properties.bobbin_board_and_margin.side_margin

        # Setup and Excitation definitions from UI
        self.properties.settings.adaptive_frequency = (
            self.gui_properties.electrical.adaptive_frequency * freq_scale["kHz"]
        )
        self.properties.settings.percentage_error = self.gui_properties.settings.percentage_error
        self.properties.settings.number_passes = self.gui_properties.settings.number_passes
        self.properties.circuit.transformer_sides = len(self.properties.circuit.side_loads)
        self.properties.circuit.side_loads = self.gui_properties.winding.side_loads
        self.properties.circuit.excitation.type = self.gui_properties.electrical.excitation_strategy
        self.properties.circuit.excitation.value = self.gui_properties.electrical.excitation_value
        self.properties.settings.offset = self.gui_properties.settings.offset
        self.properties.settings.full_model = self.gui_properties.settings.full_model
        self.properties.settings.project_path = self.gui_properties.settings.project_path
        self.properties.settings.frequency_sweep_definition = dict(
            self.gui_properties.settings.frequency_sweep_definition
        )
        self.properties.settings.frequency_sweep_definition.pop("start_frequency_unit")
        self.properties.settings.frequency_sweep_definition.pop("stop_frequency_unit")
        scale_factor_start_freq = freq_scale[
            self.gui_properties.settings.frequency_sweep_definition.start_frequency_unit
        ]
        self.properties.settings.frequency_sweep_definition["start_frequency"] *= scale_factor_start_freq
        scale_factor_stop_freq = freq_scale[self.gui_properties.settings.frequency_sweep_definition.stop_frequency_unit]
        self.properties.settings.frequency_sweep_definition["stop_frequency"] *= scale_factor_stop_freq
        self.properties.circuit.layer_side_definition = self.gui_properties.winding.layer_side_definition
        self.properties.circuit.connections_definition = self.gui_properties.winding.connections_definition
        self.properties.settings.segmentation_angle = self.gui_properties.settings.segmentation_angle

        # Materials
        if self.gui_properties.winding.insulation_material:
            self.properties.materials.update(
                {
                    self.gui_properties.winding.insulation_material: self.database_manager.materials_database[
                        "winding"
                    ][self.gui_properties.winding.insulation_material]
                }
            )
        if self.gui_properties.winding.conductor_material:
            self.properties.materials.update(
                {
                    self.gui_properties.winding.conductor_material: self.database_manager.materials_database["winding"][
                        self.gui_properties.winding.conductor_material
                    ]
                }
            )
        if self.gui_properties.core.material:
            self.properties.materials.update(
                {
                    self.gui_properties.core.material: self.database_manager.materials_database["core"][
                        self.gui_properties.core.material
                    ]
                }
            )
        if self.gui_properties.bobbin_board_and_margin.material:
            self.properties.materials.update(
                {
                    self.gui_properties.bobbin_board_and_margin.material: self.database_manager.materials_database[
                        "bobbin"
                    ][self.gui_properties.bobbin_board_and_margin.material]
                }
            )


data_manager = DataManager()
