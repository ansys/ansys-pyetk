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
import multiprocessing
import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from ansys.aedt.toolkits.common.utils import check_backend_communication
from ansys.aedt.toolkits.common.utils import clean_python_processes
from ansys.aedt.toolkits.common.utils import find_free_port
from ansys.aedt.toolkits.common.utils import is_server_running
from ansys.aedt.toolkits.common.utils import process_desktop_properties
from ansys.aedt.toolkits.electronic_transformer.backend.models import properties as backend_properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties as frontend_properties
from ansys.aedt.toolkits.electronic_transformer.ui.splash import show_splash_screen


def start_backend(pp: int) -> None:
    """Start the backend process.

    Parameters
    ----------
    pp : int
        Port to run the backend on.
    """
    from ansys.aedt.toolkits.electronic_transformer.backend.run_backend import run_backend

    print(f"Starting backend on port {pp}...")
    run_backend(pp)


def show_splash_and_start_frontend(qt_app: QApplication, url_backend: str) -> None:
    """Show the splash screen and start the frontend process.

    Parameters
    ----------
    qt_app : QApplication
        The Qt application instance.
    url_backend : str
        The URL of the backend server.
    """
    splash = show_splash_screen(qt_app)

    def check_backend():
        """Loop until the backend is running, then close the splash screen and start the frontend."""
        if check_backend_communication(url_backend):
            # Import here to avoid circular imports and speed up initial loading
            from ansys.aedt.toolkits.electronic_transformer.ui.run_frontend import run_frontend

            splash.close()
            run_frontend(url, port, qt_app)
        else:  # pragma: no cover
            # Check again in 0.5s
            QTimer.singleShot(500, check_backend)

    check_backend()


if __name__ == "__main__":

    def terminate_backend_process():
        print("Terminating backend process...")
        backend_process.terminate()
        backend_process.join()
        print("Backend process is terminated.")

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

    # Clean Python processes when script ends
    atexit.register(clean_python_processes, url, port)

    # Check if backend is already running
    if is_server_running(server=url, port=port):
        raise Exception(f"A process is already running at: {url_call}")

    # Launch backend process
    backend_process = multiprocessing.Process(target=start_backend, args=(new_port,))
    backend_process.start()

    # Connect to AEDT session if necessary
    process_desktop_properties(is_linux, url_call)

    app = QApplication(sys.argv)
    show_splash_and_start_frontend(app, url_call)
    app.aboutToQuit.connect(terminate_backend_process)
    sys.exit(app.exec())
