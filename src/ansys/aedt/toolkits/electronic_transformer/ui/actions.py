# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

        Args:
            project_selected (str, optional): The project to select. Defaults to None.
            design_selected (str, optional): The design to select. Defaults to None.

        Returns
        -------
            bool: True if model creation was successful, False otherwise.
        """
        # Set active project and design
        be_properties = self.get_properties()
        if project_selected and design_selected:
            if project_selected == "No Project":
                project_selected = generate_unique_project_name(rootname=self.temp_folder)
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

        response = requests.post(self.url + "/create_model")

        if response.ok:
            msg = "Model Created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _create_core(self):
        """Create the core geometry.

        Returns
        -------
            bool: True if core geometry creation was successful, False otherwise.
        """
        response = requests.post(self.url + "/create_core_geometry")

        if response.ok:
            msg = "Core Geometry Created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _create_winding(self):
        """Create the winding geometry.

        Returns
        -------
            bool: True if winding geometry creation was successful, False otherwise.
        """
        response = requests.post(self.url + "/create_winding_geometry")

        if response.ok:
            msg = "Winding Geometry Created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _create_bobbin(self):
        """Create the bobbin geometry.

        Returns
        -------
            bool: True if bobbin geometry creation was successful, False otherwise.
        """
        response = requests.post(self.url + "/create_bobbin_geometry")

        if response.ok:
            msg = "Bobbin Geometry Created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _create_setup(self):
        """Create the transformer setup.

        Returns
        -------
            bool: True if setup creation was successful, False otherwise.
        """
        response = requests.post(self.url + "/create_setup")

        if response.ok:
            msg = "Successful Transformer Setup."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _create_circuit(self):
        """Create the circuit.

        Returns
        -------
            bool: True if circuit creation was successful, False otherwise.
        """
        response = requests.post(self.url + "/create_circuit")

        if response.ok:
            msg = "Circuit Created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _create_region(self):
        """Create the region.

        Returns
        -------
            bool: True if region creation was successful, False otherwise.
        """
        response = requests.post(self.url + "/create_region")

        if response.ok:
            msg = "Region Created."
            logger.info(msg)
            return True
        else:
            msg = f"Failed backend call: {self.url}"
            logger.error(msg)
            return False

    def _update_backend_properties(self, be_props):
        """
        Update backend properties with current frontend properties entries.

        This method fetches data from Frontend properties, creates a dictionary new core data.
        The updated information is then sent back to the backend using the set_properties method.
        """
        etk_model = self.data_manager.create_backend_data()
        be_props.update(etk_model)
        self.set_properties(be_props)
