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
## Form generated from reading UI file 'help_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QMetaObject
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout


class Ui_help(object):

    def setupUi(self, help):
        if not help.objectName():
            help.setObjectName("help")
        help.resize(1205, 805)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(help.sizePolicy().hasHeightForWidth())
        help.setSizePolicy(sizePolicy)
        help.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(help)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.help_layout = QVBoxLayout()
        self.help_layout.setObjectName("help_layout")
        self.help_layout.setContentsMargins(-1, 0, -1, -1)
        self.help_label = QLabel(help)
        self.help_label.setObjectName("help_label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.help_label.setFont(font)
        self.help_label.setAlignment(Qt.AlignCenter)

        self.help_layout.addWidget(self.help_label)

        self.help_grid = QGridLayout()
        self.help_grid.setObjectName("help_grid")
        self.help_grid.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.help_grid.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.help_layout.addLayout(self.help_grid)

        self.verticalLayout_2.addLayout(self.help_layout)

        self.retranslateUi(help)

        QMetaObject.connectSlotsByName(help)

    # setupUi

    def retranslateUi(self, help):
        help.setWindowTitle(QCoreApplication.translate("help", "Form", None))
        self.help_label.setText(QCoreApplication.translate("help", "AEDT Design", None))

    # retranslateUi
