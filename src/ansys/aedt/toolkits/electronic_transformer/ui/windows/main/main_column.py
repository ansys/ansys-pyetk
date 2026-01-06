# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_column.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_LeftColumn(object):
    def setupUi(self, LeftColumn):
        if not LeftColumn.objectName():
            LeftColumn.setObjectName(u"LeftColumn")
        LeftColumn.resize(918, 788)
        LeftColumn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.verticalLayout = QVBoxLayout(LeftColumn)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.menus = QStackedWidget(LeftColumn)
        self.menus.setObjectName(u"menus")
        self.menus.setMaximumSize(QSize(300, 16777215))
        self.menu_geometry = QWidget()
        self.menu_geometry.setObjectName(u"menu_geometry")
        self.menu_home_layout = QVBoxLayout(self.menu_geometry)
        self.menu_home_layout.setSpacing(5)
        self.menu_home_layout.setObjectName(u"menu_home_layout")
        self.menu_home_layout.setContentsMargins(5, 5, 5, 5)
        self.geometry_vertical_layout = QVBoxLayout()
        self.geometry_vertical_layout.setObjectName(u"geometry_vertical_layout")
        self.groupBox = QGroupBox(self.menu_geometry)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QSize(250, 16777215))
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalSpacer_4 = QSpacerItem(12, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 4, 0, 1, 1)

        self.percentage_error = QLineEdit(self.groupBox)
        self.percentage_error.setObjectName(u"percentage_error")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.percentage_error.sizePolicy().hasHeightForWidth())
        self.percentage_error.setSizePolicy(sizePolicy1)
        self.percentage_error.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.percentage_error, 7, 1, 1, 1)

        self.number_passes = QLineEdit(self.groupBox)
        self.number_passes.setObjectName(u"number_passes")
        sizePolicy1.setHeightForWidth(self.number_passes.sizePolicy().hasHeightForWidth())
        self.number_passes.setSizePolicy(sizePolicy1)
        self.number_passes.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.number_passes, 6, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 7, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 10, 0, 1, 1)

        self.segmentation_angle = QLineEdit(self.groupBox)
        self.segmentation_angle.setObjectName(u"segmentation_angle")
        sizePolicy1.setHeightForWidth(self.segmentation_angle.sizePolicy().hasHeightForWidth())
        self.segmentation_angle.setSizePolicy(sizePolicy1)
        self.segmentation_angle.setMaximumSize(QSize(50, 16777215))
        self.segmentation_angle.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.segmentation_angle, 11, 1, 1, 1)

        self.skip_check = QCheckBox(self.groupBox)
        self.skip_check.setObjectName(u"skip_check")

        self.gridLayout_2.addWidget(self.skip_check, 2, 0, 1, 2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 12, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 6, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 11, 0, 1, 1)

        self.draw_skin_layers = QCheckBox(self.groupBox)
        self.draw_skin_layers.setObjectName(u"draw_skin_layers")

        self.gridLayout_2.addWidget(self.draw_skin_layers, 0, 0, 1, 2)

        self.full_model = QCheckBox(self.groupBox)
        self.full_model.setObjectName(u"full_model")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.full_model.sizePolicy().hasHeightForWidth())
        self.full_model.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.full_model, 1, 0, 1, 2)

        self.offset = QLineEdit(self.groupBox)
        self.offset.setObjectName(u"offset")
        sizePolicy1.setHeightForWidth(self.offset.sizePolicy().hasHeightForWidth())
        self.offset.setSizePolicy(sizePolicy1)
        self.offset.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.offset, 12, 1, 1, 1)

        self.bobbin_checkbox = QCheckBox(self.groupBox)
        self.bobbin_checkbox.setObjectName(u"bobbin_checkbox")

        self.gridLayout_2.addWidget(self.bobbin_checkbox, 3, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.start_frequency_unit = QComboBox(self.groupBox)
        self.start_frequency_unit.setObjectName(u"start_frequency_unit")
        self.start_frequency_unit.setMinimumSize(QSize(60, 0))
        self.start_frequency_unit.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.start_frequency_unit, 1, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.stop_frequency_unit = QComboBox(self.groupBox)
        self.stop_frequency_unit.setObjectName(u"stop_frequency_unit")
        self.stop_frequency_unit.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.stop_frequency_unit, 2, 2, 1, 1)

        self.stop_frequency = QLineEdit(self.groupBox)
        self.stop_frequency.setObjectName(u"stop_frequency")
        sizePolicy1.setHeightForWidth(self.stop_frequency.sizePolicy().hasHeightForWidth())
        self.stop_frequency.setSizePolicy(sizePolicy1)
        self.stop_frequency.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.stop_frequency, 2, 1, 1, 1)

        self.start_frequency = QLineEdit(self.groupBox)
        self.start_frequency.setObjectName(u"start_frequency")
        sizePolicy1.setHeightForWidth(self.start_frequency.sizePolicy().hasHeightForWidth())
        self.start_frequency.setSizePolicy(sizePolicy1)
        self.start_frequency.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.start_frequency, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.samples = QLineEdit(self.groupBox)
        self.samples.setObjectName(u"samples")
        sizePolicy1.setHeightForWidth(self.samples.sizePolicy().hasHeightForWidth())
        self.samples.setSizePolicy(sizePolicy1)
        self.samples.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.samples, 3, 1, 1, 1)

        self.frequency_sweep = QCheckBox(self.groupBox)
        self.frequency_sweep.setObjectName(u"frequency_sweep")

        self.gridLayout.addWidget(self.frequency_sweep, 0, 0, 1, 3)

        self.scale_combo = QComboBox(self.groupBox)
        self.scale_combo.setObjectName(u"scale_combo")

        self.gridLayout.addWidget(self.scale_combo, 4, 1, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.geometry_vertical_layout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.geometry_vertical_layout.addItem(self.verticalSpacer)


        self.menu_home_layout.addLayout(self.geometry_vertical_layout)

        self.menus.addWidget(self.menu_geometry)

        self.verticalLayout.addWidget(self.menus)

        QWidget.setTabOrder(self.draw_skin_layers, self.full_model)
        QWidget.setTabOrder(self.full_model, self.skip_check)
        QWidget.setTabOrder(self.skip_check, self.number_passes)
        QWidget.setTabOrder(self.number_passes, self.percentage_error)
        QWidget.setTabOrder(self.percentage_error, self.segmentation_angle)
        QWidget.setTabOrder(self.segmentation_angle, self.offset)
        QWidget.setTabOrder(self.offset, self.frequency_sweep)
        QWidget.setTabOrder(self.frequency_sweep, self.start_frequency)
        QWidget.setTabOrder(self.start_frequency, self.start_frequency_unit)
        QWidget.setTabOrder(self.start_frequency_unit, self.stop_frequency)
        QWidget.setTabOrder(self.stop_frequency, self.stop_frequency_unit)
        QWidget.setTabOrder(self.stop_frequency_unit, self.samples)
        QWidget.setTabOrder(self.samples, self.scale_combo)

        self.retranslateUi(LeftColumn)

        self.menus.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LeftColumn)
    # setupUi

    def retranslateUi(self, LeftColumn):
        LeftColumn.setWindowTitle(QCoreApplication.translate("LeftColumn", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("LeftColumn", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate("LeftColumn", u"Percentage Error", None))
        self.skip_check.setText(QCoreApplication.translate("LeftColumn", u"Skip Check Windings", None))
        self.label_4.setText(QCoreApplication.translate("LeftColumn", u"Region Offset", None))
        self.label_3.setText(QCoreApplication.translate("LeftColumn", u"Number of Passes", None))
        self.label.setText(QCoreApplication.translate("LeftColumn", u"Segmentation Angle", None))
        self.draw_skin_layers.setText(QCoreApplication.translate("LeftColumn", u"Draw Skin Layers", None))
        self.full_model.setText(QCoreApplication.translate("LeftColumn", u"Make Full Model", None))
        self.bobbin_checkbox.setText(QCoreApplication.translate("LeftColumn", u"Draw Bobbin", None))
        self.label_6.setText(QCoreApplication.translate("LeftColumn", u"Stop", None))
        self.label_5.setText(QCoreApplication.translate("LeftColumn", u"Start", None))
        self.label_7.setText(QCoreApplication.translate("LeftColumn", u"Samples", None))
        self.label_8.setText(QCoreApplication.translate("LeftColumn", u"Scale", None))
        self.frequency_sweep.setText(QCoreApplication.translate("LeftColumn", u"Enable Frequency Sweep", None))
    # retranslateUi

