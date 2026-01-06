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
    else:  # pragma: no cover
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
    else:  # pragma: no cover
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
    else:  # pragma: no cover
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
    else:  # pragma: no cover
        return jsonify("PyETK model not created"), 500


@app.route("/validate_json", methods=["POST"])
def validate_json():
    logger.info("[POST] /validate_json (Validates the Json file).")

    # Get properties from frontend
    properties_frontend = toolkit_api.get_properties()

    answer = toolkit_api.validate_json(properties_frontend)
    if answer:
        return jsonify("Json file valid"), 200
    else:  # pragma: no cover
        return jsonify("Json file not valid"), 500


def run_backend(port=0):
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
