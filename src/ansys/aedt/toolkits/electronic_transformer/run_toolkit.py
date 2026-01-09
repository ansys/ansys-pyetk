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


import atexit
import importlib
import multiprocessing
import os
import sys
import time

from ansys.aedt.toolkits.common.utils import check_backend_communication
from ansys.aedt.toolkits.common.utils import clean_python_processes
from ansys.aedt.toolkits.common.utils import find_free_port
from ansys.aedt.toolkits.common.utils import is_server_running
from ansys.aedt.toolkits.common.utils import process_desktop_properties
from ansys.aedt.toolkits.common.utils import wait_for_server
from ansys.aedt.toolkits.electronic_transformer.backend.models import properties as backend_properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties as frontend_properties
from ansys.aedt.toolkits.electronic_transformer.ui.splash import show_splash_screen

backend = None
ui = None


def get_backend():
    global backend
    if backend is None:
        backend = importlib.import_module("ansys.aedt.toolkits.electronic_transformer.backend.run_backend")
    return backend


def get_ui():
    global ui
    if ui is None:
        ui = importlib.import_module("ansys.aedt.toolkits.electronic_transformer.ui.run_frontend")
    return ui


def start_backend(pp):
    """Start the backend process."""
    backend_imported = get_backend()

    print(f"Starting backend on port {pp}...")
    backend_imported.run_backend(pp)


def start_frontend(backend_url, backend_port):
    """Start the frontend process."""
    ui_imported = get_ui()
    print("Starting frontend...")
    ui_imported.run_frontend(backend_url, backend_port)


if __name__ == "__main__":
    multiprocessing.freeze_support()

    is_linux = os.name == "posix"
    new_port = find_free_port(backend_properties.url, backend_properties.port)
    if not new_port:
        raise Exception(f"No free ports available in {backend_properties.url}")

    backend_properties.port = new_port
    frontend_properties.backend_port = new_port
    url = frontend_properties.backend_url
    port = frontend_properties.backend_port
    url_call = f"http://{url}:{port}"
    python_path = sys.executable

    def terminate_processes():
        print("Terminating backend and frontend processes...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join()
        frontend_process.join()
        print("Processes terminated.")

    # Clean python processes when script ends
    atexit.register(clean_python_processes, url, port)

    # Check if backend is already running
    if is_server_running(server=url, port=port):
        raise Exception(f"A process is already running at: {url_call}")

    if not is_linux:
        # Launch splash
        splash_process = multiprocessing.Process(target=show_splash_screen)
        splash_process.start()

    # Launch backend process
    backend_process = multiprocessing.Process(target=start_backend, args=(new_port,))
    backend_process.start()

    # Wait for backend to start
    count = 0
    while not check_backend_communication(url_call) and count < 10:
        time.sleep(1)
        count += 1

    if not check_backend_communication(url_call):
        raise Exception("Backend communication is not working.")

    # Connect to AEDT session if necessary
    process_desktop_properties(is_linux, url_call)

    if not is_linux:
        splash_process.join()

    # Launch frontend process
    frontend_process = multiprocessing.Process(target=start_frontend, args=(url, port))
    frontend_process.start()

    # Wait for backend confirmation
    if not wait_for_server(server=url, port=port):
        raise Exception(f"Backend did not start properly at {url_call}")

    # Keep frontend running
    frontend_process.join()

    terminate_processes()
