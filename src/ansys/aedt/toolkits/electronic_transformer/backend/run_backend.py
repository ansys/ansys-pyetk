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


import sys

# isort: off

from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend

from ansys.aedt.toolkits.common.backend.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.common.backend.rest_api import app
from ansys.aedt.toolkits.common.backend.rest_api import jsonify
from ansys.aedt.toolkits.common.backend.rest_api import logger

# isort: on

toolkit_api = ToolkitBackend()

if len(sys.argv) == 3:
    toolkit_api.properties.url = sys.argv[1]
    toolkit_api.properties.port = int(sys.argv[2])


@app.route("/create_core_geometry", methods=["POST"])
def create_core_geometry():
    """Create a core geometry in Maxwell.

    Returns
    -------
    str
        Message indicating if the core was created.
    """
    logger.info("[POST] /create_core_geometry (creates a core in Maxwell).")

    # Get properties from frontend
    properties_frontend = toolkit_api.get_properties()

    core_name = toolkit_api.create_core_geometry(properties_frontend)
    if core_name:
        return jsonify("Core created"), 200
    else:
        return jsonify("Core not created"), 500


@app.route("/create_winding_geometry", methods=["POST"])
def create_winding_geometry():
    """Create winding geometry in Maxwell.

    Returns
    -------
    str
        Message indicating if the winding was created.
    """
    logger.info("[POST] /create_winding_geometry (creates winding geometry in Maxwell).")

    # Get properties from frontend
    properties_frontend = toolkit_api.get_properties()

    winding_name = toolkit_api.create_winding_geometry(properties_frontend)
    if winding_name:
        return jsonify("Winding created"), 200
    else:
        return jsonify("Winding not created"), 500


@app.route("/create_bobbin_geometry", methods=["POST"])
def create_bobbin_geometry():
    """Create bobbin geometry in Maxwell.

    Returns
    -------
    str
        Message indicating if the bobbin was created.
    """
    logger.info("[POST] /create_bobbin_geometry (creates bobbin geometry in Maxwell).")

    # Get properties from frontend
    properties_frontend = toolkit_api.get_properties()

    bobbin_name = toolkit_api.create_bobbin_geometry(properties_frontend)
    if bobbin_name:
        return jsonify("Bobbin created"), 200
    else:
        return jsonify("Bobbin not created"), 500


@app.route("/create_model", methods=["POST"])
def create_model():
    """Create the entire transformer model.

    Returns
    -------
    str
        Message indicating if the model was created.
    """
    logger.info("[POST] /create_model (creates PyETK Model).")

    # Get properties from frontend
    properties_frontend = toolkit_api.get_properties()

    region = toolkit_api.create_model(properties_frontend)
    if region:
        return jsonify("PyETK model created"), 200
    else:
        return jsonify("PyETK model not created"), 500


@app.route("/validate_json", methods=["POST"])
def validate_json():
    """Validate the JSON file."""
    logger.info("[POST] /validate_json (Validates JSON file).")

    # Get properties from frontend
    properties_frontend = toolkit_api.get_properties()

    answer = toolkit_api.validate_json(properties_frontend)
    if answer:
        return jsonify("JSON file is valid"), 200
    else:
        return jsonify("JSON file is not valid"), 500


def run_backend(port: int = 0) -> None:
    """Run the server.

    Parameters
    ----------
    port : int, optional
        Port to run the server on. The default is ``0``.
    """
    app.debug = toolkit_api.properties.debug
    server = MultithreadingServer()
    if port == 0:
        port = toolkit_api.properties.port
    server.run(host=toolkit_api.properties.url, port=port, app=app)


if __name__ == "__main__":
    run_backend()
