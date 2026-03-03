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


import os
import sys

# isort: off
from ansys.aedt.toolkits.electronic_transformer import __version__

# Default user interface properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties as properties

# isort: on

# PySide6 Widgets
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow

from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger

# Common windows
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout

# Toolkit frontend API
from ansys.aedt.toolkits.electronic_transformer.ui.actions import Frontend
from ansys.aedt.toolkits.electronic_transformer.ui.windows.help.help_menu import HelpMenu

# New windows
from ansys.aedt.toolkits.electronic_transformer.ui.windows.main.main_menu import GeometryMenu

# Backend URL and port
if len(sys.argv) == 3:
    properties.backend_url = sys.argv[1]
    properties.backend_port = int(sys.argv[2])

url = properties.backend_url

port = properties.backend_port

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

properties.high_resolution = (
    os.getenv("AEDT_TOOLKIT_HIGH_RESOLUTION", "false").lower() in ("true", "1", "t") or properties.high_resolution
)
if properties.high_resolution:
    os.environ["QT_SCALE_FACTOR"] = "2"

properties.version = __version__


class ApplicationWindow(QMainWindow, Frontend):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.properties = properties

        # General Settings

        # Create main window layout
        self.ui = MainWindowLayout(self)
        self.ui.setup()

        # Home menu
        self.home_menu = HomeMenu(self)
        self.home_menu.setup()
        self.ui.left_menu.clicked.connect(self.home_menu_clicked)

        # Settings menu
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.setup()
        self.ui.title_bar.clicked.connect(self.settings_menu_clicked)

        # Check backend connection
        success = self.check_connection()
        self.backend_connected = False

        if not success:
            msg = "Error getting properties from backend. User interface running without backend"
            self.ui.update_logger(msg)
            logger.error(msg)
            self.settings_menu.signal_flag = False
            self.settings_menu.aedt_version.addItem("Backend OFF")
            self.settings_menu.aedt_session.addItem("Backend OFF")
        else:
            self.backend_connected = True
            # Get default properties
            be_properties = self.get_properties()
            # Get AEDT installed versions
            installed_versions = self.installed_versions()

            self.settings_menu.aedt_session.clear()
            self.settings_menu.aedt_session.addItem("New Session")
            if installed_versions:
                self.settings_menu.connect_aedt.setEnabled(True)
                for ver in installed_versions:
                    self.settings_menu.aedt_version.addItem(ver)
            else:
                self.settings_menu.aedt_version.addItem("AEDT not installed")

            if be_properties.get("aedt_version") in installed_versions:
                self.settings_menu.aedt_version.setCurrentText(be_properties.get("aedt_version"))

        # Custom toolkit setup starts here

        # Modeler menu
        self.geometry_menu = GeometryMenu(self)
        self.geometry_menu.setup()
        self.ui.left_menu.clicked.connect(self.geometry_menu_clicked)

        # Help menu
        self.help_menu = HelpMenu(self)
        self.help_menu.setup()
        self.ui.left_menu.clicked.connect(self.help_menu_clicked)

        # Progress column
        self.ui.left_menu.clicked.connect(self.progress_menu_clicked)

        # Close column
        self.ui.title_bar.clicked.connect(self.close_menu_clicked)
        self.ui.left_column.clicked.connect(self.close_menu_clicked)

        # Home page as first page
        self.ui.set_page(self.ui.load_pages.home_page)

    def progress_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        self.ui.left_menu.select_only_one(selected_menu.objectName())
        if menu_name == "progress_menu":
            is_progress_visible = self.ui.is_progress_visible()
            if is_progress_visible:
                selected_menu.set_active(False)
            self.ui.toggle_progress()

    def close_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        if menu_name != "top_settings" and self.ui.is_left_column_visible():
            selected_menu.set_active(False)
            self.ui.toggle_left_column()
            self.ui.left_menu.deselect_all()
        if menu_name == "top_settings" and self.ui.is_right_column_visible():
            self.ui.toggle_right_column()

    def home_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        self.ui.left_menu.select_only_one(selected_menu.objectName())
        if menu_name == "home_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.ui.load_pages.home_page)

            is_left_visible = self.ui.is_left_column_visible()

            self.ui.set_left_column_menu(
                menu=self.ui.left_column.menus.menu_home,
                title="Home",
                icon_path=self.ui.images_load.icon_path("icon_home.svg"),
            )

            if not is_left_visible:
                self.ui.toggle_left_column()

    def geometry_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "geometry_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.geometry_menu.geometry_menu_widget)

            is_left_visible = self.ui.is_left_column_visible()

            self.ui.set_left_column_menu(
                menu=self.geometry_menu.geometry_column_widget,
                title="Transformer Builder",
                icon_path=self.ui.images_load.icon_path("icon_plot_3d.svg"),
            )

            if not is_left_visible:
                self.ui.toggle_left_column()

    def settings_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        is_right_visible = self.ui.is_right_column_visible()
        is_left_visible = self.ui.is_left_column_visible()

        if menu_name == "top_settings" and not is_right_visible:
            self.ui.app.settings_menu.show_widgets()
            if is_left_visible:
                self.ui.toggle_left_column()
                self.ui.left_menu.deselect_all()
            self.ui.toggle_right_column()
            self.ui.set_right_column_menu(title="Settings")

    def help_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "help_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.help_menu.help_menu_widget)

            self.ui.set_left_column_menu(
                menu=self.help_menu.help_column_widget,
                title="Help",
                icon_path=self.ui.images_load.icon_path("help.svg"),
            )

            is_left_visible = self.ui.is_left_column_visible()
            if not is_left_visible:
                self.ui.toggle_left_column()

    def close_event(self, event):
        event.accept()


def run_frontend(backend_url: str = "", backend_port: int = 0, app: QApplication = None):  # pragma: no cover
    """Run the frontend application.

    Parameters
    ----------
    backend_url : str, optional
        The URL of the backend server. Default is ``""``.
    backend_port : int, optional
        The port of the backend server. Default is ``0``.
    app : QApplication, optional
        The Qt application instance. If not provided, a new instance will be created.
    """
    if backend_url:
        properties.backend_url = backend_url
    if backend_port:
        properties.backend_port = backend_port

    run_separately = False

    if not app:
        run_separately = True
        app = QApplication(sys.argv)

    window = ApplicationWindow()
    window.show()
    app.processEvents()
    if run_separately:
        sys.exit(app.exec())


if __name__ == "__main__":
    run_frontend()
