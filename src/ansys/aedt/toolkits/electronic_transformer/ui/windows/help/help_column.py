# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_column.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QMetaObject
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class Ui_LeftColumn(object):

    def setupUi(self, LeftColumn):
        if not LeftColumn.objectName():
            LeftColumn.setObjectName("LeftColumn")
        LeftColumn.resize(815, 600)
        self.verticalLayout = QVBoxLayout(LeftColumn)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.menus = QStackedWidget(LeftColumn)
        self.menus.setObjectName("menus")
        self.menu_help = QWidget()
        self.menu_help.setObjectName("menu_help")
        self.menu_home_layout = QVBoxLayout(self.menu_help)
        self.menu_home_layout.setSpacing(5)
        self.menu_home_layout.setObjectName("menu_home_layout")
        self.menu_home_layout.setContentsMargins(5, 5, 5, 5)
        self.help_vertical_layout = QVBoxLayout()
        self.help_vertical_layout.setObjectName("help_vertical_layout")

        self.menu_home_layout.addLayout(self.help_vertical_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.menu_home_layout.addItem(self.verticalSpacer)

        self.menus.addWidget(self.menu_help)

        self.verticalLayout.addWidget(self.menus)

        self.retranslateUi(LeftColumn)

        self.menus.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(LeftColumn)

    # setupUi

    def retranslateUi(self, LeftColumn):
        LeftColumn.setWindowTitle(QCoreApplication.translate("LeftColumn", "Form", None))

    # retranslateUi
