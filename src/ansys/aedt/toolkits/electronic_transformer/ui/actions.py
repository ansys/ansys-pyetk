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

import tempfile

import requests

from ansys.aedt.core.generic.file_utils import generate_unique_project_name
from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.electronic_transformer.ui.common.data_manager import data_manager

# Default user interface properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties


class Frontend(FrontendGeneric):
    """Manages the frontend actions for the electronic transformer toolkit."""

    def __init__(self):
        """Initialize the Frontend.

        Sets up a temporary folder and initializes properties.
        """
        FrontendGeneric.__init__(self)
        self.temp_folder = tempfile.mkdtemp()
        self.properties = fe_properties
        self.data_manager = data_manager

    def create_model(self, project_selected=None, design_selected=None):
        """Create the transformer model.

        Parameters
        ----------
        project_selected : str, optional
            The project to select. Defaults to None.
        design_selected : str, optional
            The design to select. Defaults to None.

        Returns
        -------
            bool: True if model creation was successful, False otherwise.
        """
        # Set active project and design
        be_properties = self.get_properties()
        if project_selected and design_selected:
            if project_selected == "No Project":
                project_selected = generate_unique_project_name(root_name=self.temp_folder)
                be_properties["active_project"] = project_selected

            for project in be_properties["project_list"]:
                if self.get_project_name(project) == project_selected:
                    be_properties["active_project"] = project
                    if project_selected in list(be_properties["design_list"].keys()):
                        designs = be_properties["design_list"][project_selected]
                        for design in designs:
                            if design_selected == design:
                                be_properties["active_design"] = design
                                break
                    break
        else:
            project_selected = generate_unique_project_name()
            project_selected = self.get_project_name(project_selected)
            be_properties["active_project"] = project_selected

        # update backend properties
        self._update_backend_properties(be_properties)

        # Validates the model before creating it
        validation = requests.get(self.url + "/validate_model")
        if not validation.ok:
            msg = f"Model Validation Failed: {self.url}"
            logger.error(msg)
            if hasattr(self, "ui"):
                self.ui.update_logger(msg)
            msg_list = validation.text.split("\\n")  # split string into a list of messages
            for msg in msg_list:
                logger.error(msg)
                msg.replace("\n", "")
                if hasattr(self, "ui"):
                    self.ui.update_logger(msg)
            return False

        # Creates the model
        if validation.ok:
            response = requests.post(self.url + "/create_model")
            if response.ok:
                msg = "Model Created."
                logger.info(msg)
                if hasattr(self, "ui"):
                    self.ui.update_logger(msg)
                return True
            else:
                msg = f"Failed backend call: {self.url}"
                logger.error(msg)
                if hasattr(self, "ui"):
                    self.ui.update_logger(msg)
                return False

    def _update_backend_properties(self, be_props):
        """
        Update backend properties with current frontend properties entries.

        This method fetches data from Frontend properties, creates a dictionary new core data.
        The updated information is then sent back to the backend using the set_properties method.
        """
        etk_model = self.data_manager.create_backend_data()
        be_props.update(etk_model)
        for prop in etk_model:
            self.set_properties({prop: be_props[prop]})
