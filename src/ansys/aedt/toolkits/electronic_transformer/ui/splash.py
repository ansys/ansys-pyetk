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

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QSplashScreen

from ansys.aedt.toolkits.electronic_transformer import __version__
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties as properties


def show_splash_screen(app: QApplication) -> QSplashScreen:
    """Show the splash screen for the application.

    Creates a splash screen with a specified image and dimensions,
    displaying it for a certain duration before closing. The splash
    screen appears on top of the main application window and includes product name and version.

    Parameters
    ----------
    app : QApplication
        The Qt application instance.

    Returns
    -------
    QSplashScreen
        The splash screen instance.
    """
    from PySide6.QtGui import QFont
    from PySide6.QtGui import QPainter

    splash_dim = 800 if properties.high_resolution else 600
    splash_pix = QPixmap(Path(__file__).parent / "splash.png")
    scaled_pix = splash_pix.scaled(splash_dim, splash_dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    # Paint product name and version directly onto the pixmap
    painter = QPainter(scaled_pix)

    # --- Product name: top dead centre ---
    title_font = QFont()
    title_font.setPointSize(15)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.setPen(QColor("black"))
    painter.drawText(
        scaled_pix.rect().adjusted(0, 10, 0, 0), Qt.AlignTop | Qt.AlignHCenter, "Electronic Transformer Toolkit, PyETK"
    )

    # --- Version: bottom right ---
    version_font = QFont()
    version_font.setPointSize(15)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.setPen(QColor("black"))
    painter.drawText(scaled_pix.rect().adjusted(0, 0, -10, -10), Qt.AlignBottom | Qt.AlignRight, f"v{__version__}")

    painter.end()

    splash = QSplashScreen(scaled_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()

    app.processEvents()

    return splash
