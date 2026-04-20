# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_page.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Geometry(object):
    def setupUi(self, Geometry):
        if not Geometry.objectName():
            Geometry.setObjectName(u"Geometry")
        Geometry.resize(1250, 840)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Geometry.sizePolicy().hasHeightForWidth())
        Geometry.setSizePolicy(sizePolicy)
        Geometry.setMinimumSize(QSize(1210, 840))
        Geometry.setMaximumSize(QSize(1300, 840))
        self.verticalLayout_2 = QVBoxLayout(Geometry)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.top_layout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.groupBox_6 = QGroupBox(Geometry)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(555, 55))
        self.groupBox_6.setMaximumSize(QSize(575, 100))
        self.open_etk = QPushButton(self.groupBox_6)
        self.open_etk.setObjectName(u"open_etk")
        self.open_etk.setGeometry(QRect(10, 20, 75, 24))
        self.open_etk.setMaximumSize(QSize(75, 16777215))
        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(90, 20, 51, 16))
        self.previous_example_button = QPushButton(self.groupBox_6)
        self.previous_example_button.setObjectName(u"previous_example_button")
        self.previous_example_button.setGeometry(QRect(160, 20, 40, 24))
        self.previous_example_button.setMaximumSize(QSize(40, 16777215))
        self.next_example_button = QPushButton(self.groupBox_6)
        self.next_example_button.setObjectName(u"next_example_button")
        self.next_example_button.setGeometry(QRect(200, 20, 40, 24))
        self.next_example_button.setMaximumSize(QSize(40, 16777215))
        self.example_name = QLineEdit(self.groupBox_6)
        self.example_name.setObjectName(u"example_name")
        self.example_name.setGeometry(QRect(240, 20, 201, 22))
        self.reset_examples = QPushButton(self.groupBox_6)
        self.reset_examples.setObjectName(u"reset_examples")
        self.reset_examples.setGeometry(QRect(448, 20, 101, 24))

        self.verticalLayout_3.addWidget(self.groupBox_6)

        self.groupBox_4 = QGroupBox(Geometry)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.groupBox_4.setMinimumSize(QSize(555, 563))
        self.groupBox_4.setMaximumSize(QSize(555, 620))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.D_1_label = QLabel(self.groupBox_4)
        self.D_1_label.setObjectName(u"D_1_label")

        self.gridLayout.addWidget(self.D_1_label, 7, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(5, 220, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_3, 7, 4, 8, 1)

        self.D_6_ref = QLabel(self.groupBox_4)
        self.D_6_ref.setObjectName(u"D_6_ref")

        self.gridLayout.addWidget(self.D_6_ref, 12, 3, 1, 1)

        self.model_combo = QComboBox(self.groupBox_4)
        self.model_combo.setObjectName(u"model_combo")
        sizePolicy.setHeightForWidth(self.model_combo.sizePolicy().hasHeightForWidth())
        self.model_combo.setSizePolicy(sizePolicy)
        self.model_combo.setMinimumSize(QSize(100, 0))
        self.model_combo.setMaximumSize(QSize(100, 30))

        self.gridLayout.addWidget(self.model_combo, 2, 2, 1, 2)

        self.D_6 = QLineEdit(self.groupBox_4)
        self.D_6.setObjectName(u"D_6")
        self.D_6.setMinimumSize(QSize(65, 0))
        self.D_6.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_6, 12, 2, 1, 1)

        self.custom_core_checkbox = QCheckBox(self.groupBox_4)
        self.custom_core_checkbox.setObjectName(u"custom_core_checkbox")

        self.gridLayout.addWidget(self.custom_core_checkbox, 6, 2, 1, 1)

        self.D_7_ref = QLabel(self.groupBox_4)
        self.D_7_ref.setObjectName(u"D_7_ref")

        self.gridLayout.addWidget(self.D_7_ref, 13, 3, 1, 1)

        self.label_26 = QLabel(self.groupBox_4)
        self.label_26.setObjectName(u"label_26")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy2)
        self.label_26.setFrameShape(QFrame.Shape.NoFrame)
        self.label_26.setFrameShadow(QFrame.Shadow.Raised)
        self.label_26.setLineWidth(5)
        self.label_26.setMidLineWidth(2)

        self.gridLayout.addWidget(self.label_26, 1, 0, 1, 1)

        self.D_3 = QLineEdit(self.groupBox_4)
        self.D_3.setObjectName(u"D_3")
        self.D_3.setMinimumSize(QSize(65, 0))
        self.D_3.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_3, 9, 2, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_5, 16, 4, 1, 1)

        self.type_combo = QComboBox(self.groupBox_4)
        self.type_combo.setObjectName(u"type_combo")
        sizePolicy.setHeightForWidth(self.type_combo.sizePolicy().hasHeightForWidth())
        self.type_combo.setSizePolicy(sizePolicy)
        self.type_combo.setMinimumSize(QSize(100, 0))
        self.type_combo.setMaximumSize(QSize(100, 30))

        self.gridLayout.addWidget(self.type_combo, 1, 2, 1, 2)

        self.supplier_combo = QComboBox(self.groupBox_4)
        self.supplier_combo.setObjectName(u"supplier_combo")
        sizePolicy.setHeightForWidth(self.supplier_combo.sizePolicy().hasHeightForWidth())
        self.supplier_combo.setSizePolicy(sizePolicy)
        self.supplier_combo.setMinimumSize(QSize(100, 0))
        self.supplier_combo.setMaximumSize(QSize(100, 30))

        self.gridLayout.addWidget(self.supplier_combo, 0, 2, 1, 2)

        self.D_1 = QLineEdit(self.groupBox_4)
        self.D_1.setObjectName(u"D_1")
        sizePolicy.setHeightForWidth(self.D_1.sizePolicy().hasHeightForWidth())
        self.D_1.setSizePolicy(sizePolicy)
        self.D_1.setMinimumSize(QSize(65, 0))
        self.D_1.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_1, 7, 2, 1, 1)

        self.D_8 = QLineEdit(self.groupBox_4)
        self.D_8.setObjectName(u"D_8")
        self.D_8.setMinimumSize(QSize(65, 0))
        self.D_8.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_8, 14, 2, 1, 1)

        self.D_2_ref = QLabel(self.groupBox_4)
        self.D_2_ref.setObjectName(u"D_2_ref")

        self.gridLayout.addWidget(self.D_2_ref, 8, 3, 1, 1)

        self.D_3_label = QLabel(self.groupBox_4)
        self.D_3_label.setObjectName(u"D_3_label")

        self.gridLayout.addWidget(self.D_3_label, 9, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_4, 17, 4, 1, 1)

        self.D_8_ref = QLabel(self.groupBox_4)
        self.D_8_ref.setObjectName(u"D_8_ref")

        self.gridLayout.addWidget(self.D_8_ref, 14, 3, 1, 1)

        self.verticalSpacer_16 = QSpacerItem(5, 85, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_16, 18, 4, 1, 1)

        self.material_combo = QComboBox(self.groupBox_4)
        self.material_combo.setObjectName(u"material_combo")
        sizePolicy.setHeightForWidth(self.material_combo.sizePolicy().hasHeightForWidth())
        self.material_combo.setSizePolicy(sizePolicy)
        self.material_combo.setMinimumSize(QSize(100, 0))
        self.material_combo.setMaximumSize(QSize(100, 30))

        self.gridLayout.addWidget(self.material_combo, 3, 2, 1, 2)

        self.airgap_combo = QComboBox(self.groupBox_4)
        self.airgap_combo.addItem("")
        self.airgap_combo.addItem("")
        self.airgap_combo.addItem("")
        self.airgap_combo.addItem("")
        self.airgap_combo.setObjectName(u"airgap_combo")
        self.airgap_combo.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.airgap_combo, 16, 2, 1, 1)

        self.D_5_label = QLabel(self.groupBox_4)
        self.D_5_label.setObjectName(u"D_5_label")

        self.gridLayout.addWidget(self.D_5_label, 11, 0, 1, 1)

        self.D_5_ref = QLabel(self.groupBox_4)
        self.D_5_ref.setObjectName(u"D_5_ref")

        self.gridLayout.addWidget(self.D_5_ref, 11, 3, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(5, 112, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_9, 0, 4, 4, 1)

        self.airgap_value = QLineEdit(self.groupBox_4)
        self.airgap_value.setObjectName(u"airgap_value")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.airgap_value.sizePolicy().hasHeightForWidth())
        self.airgap_value.setSizePolicy(sizePolicy3)
        self.airgap_value.setMinimumSize(QSize(65, 0))
        self.airgap_value.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.airgap_value, 17, 2, 1, 1)

        self.D_6_label = QLabel(self.groupBox_4)
        self.D_6_label.setObjectName(u"D_6_label")

        self.gridLayout.addWidget(self.D_6_label, 12, 0, 1, 1)

        self.D_2_label = QLabel(self.groupBox_4)
        self.D_2_label.setObjectName(u"D_2_label")

        self.gridLayout.addWidget(self.D_2_label, 8, 0, 1, 1)

        self.D_7_label = QLabel(self.groupBox_4)
        self.D_7_label.setObjectName(u"D_7_label")

        self.gridLayout.addWidget(self.D_7_label, 13, 0, 1, 1)

        self.D_7 = QLineEdit(self.groupBox_4)
        self.D_7.setObjectName(u"D_7")
        self.D_7.setMinimumSize(QSize(65, 0))
        self.D_7.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_7, 13, 2, 1, 1)

        self.D_2 = QLineEdit(self.groupBox_4)
        self.D_2.setObjectName(u"D_2")
        self.D_2.setMinimumSize(QSize(65, 0))
        self.D_2.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_2, 8, 2, 1, 1)

        self.D_8_label = QLabel(self.groupBox_4)
        self.D_8_label.setObjectName(u"D_8_label")

        self.gridLayout.addWidget(self.D_8_label, 14, 0, 1, 1)

        self.D_3_ref = QLabel(self.groupBox_4)
        self.D_3_ref.setObjectName(u"D_3_ref")

        self.gridLayout.addWidget(self.D_3_ref, 9, 3, 1, 1)

        self.D_4_ref = QLabel(self.groupBox_4)
        self.D_4_ref.setObjectName(u"D_4_ref")

        self.gridLayout.addWidget(self.D_4_ref, 10, 3, 1, 1)

        self.D_4 = QLineEdit(self.groupBox_4)
        self.D_4.setObjectName(u"D_4")
        self.D_4.setMinimumSize(QSize(65, 0))
        self.D_4.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_4, 10, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 16, 0, 1, 1)

        self.label_32 = QLabel(self.groupBox_4)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout.addWidget(self.label_32, 0, 0, 1, 1)

        self.core_airgap_size = QLabel(self.groupBox_4)
        self.core_airgap_size.setObjectName(u"core_airgap_size")

        self.gridLayout.addWidget(self.core_airgap_size, 17, 0, 1, 1)

        self.label_27 = QLabel(self.groupBox_4)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout.addWidget(self.label_27, 2, 0, 1, 1)

        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.D_1_ref = QLabel(self.groupBox_4)
        self.D_1_ref.setObjectName(u"D_1_ref")

        self.gridLayout.addWidget(self.D_1_ref, 7, 3, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(5, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_6, 15, 4, 1, 1)

        self.verticalSpacer = QSpacerItem(5, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.D_4_label = QLabel(self.groupBox_4)
        self.D_4_label.setObjectName(u"D_4_label")

        self.gridLayout.addWidget(self.D_4_label, 10, 0, 1, 1)

        self.D_5 = QLineEdit(self.groupBox_4)
        self.D_5.setObjectName(u"D_5")
        self.D_5.setMinimumSize(QSize(65, 0))
        self.D_5.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.D_5, 11, 2, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_7, 6, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(5, -1, -1, -1)
        self.verticalSpacer_17 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_9.addItem(self.verticalSpacer_17, 3, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_12, 1, 0, 1, 1)

        self.core_image = QGraphicsView(self.groupBox_4)
        self.core_image.setObjectName(u"core_image")
        sizePolicy.setHeightForWidth(self.core_image.sizePolicy().hasHeightForWidth())
        self.core_image.setSizePolicy(sizePolicy)
        self.core_image.setMinimumSize(QSize(310, 370))
        self.core_image.setMaximumSize(QSize(310, 370))
        self.core_image.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

        self.gridLayout_9.addWidget(self.core_image, 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_2.addLayout(self.gridLayout_9)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 5, 5, -1)
        self.bobbin_groupbox = QGroupBox(Geometry)
        self.bobbin_groupbox.setObjectName(u"bobbin_groupbox")
        self.bobbin_groupbox.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.bobbin_groupbox.sizePolicy().hasHeightForWidth())
        self.bobbin_groupbox.setSizePolicy(sizePolicy4)
        self.bobbin_groupbox.setMinimumSize(QSize(230, 130))
        self.bobbin_groupbox.setMaximumSize(QSize(230, 130))
        self.gridLayout_4 = QGridLayout(self.bobbin_groupbox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bobbin_label = QLabel(self.bobbin_groupbox)
        self.bobbin_label.setObjectName(u"bobbin_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.bobbin_label.sizePolicy().hasHeightForWidth())
        self.bobbin_label.setSizePolicy(sizePolicy5)
        self.bobbin_label.setMinimumSize(QSize(130, 0))
        self.bobbin_label.setMaximumSize(QSize(130, 16777215))

        self.gridLayout_3.addWidget(self.bobbin_label, 1, 0, 1, 1)

        self.top_margin = QLineEdit(self.bobbin_groupbox)
        self.top_margin.setObjectName(u"top_margin")
        sizePolicy.setHeightForWidth(self.top_margin.sizePolicy().hasHeightForWidth())
        self.top_margin.setSizePolicy(sizePolicy)
        self.top_margin.setMinimumSize(QSize(55, 0))
        self.top_margin.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_3.addWidget(self.top_margin, 2, 2, 1, 1)

        self.bobbin_board_thickness = QLineEdit(self.bobbin_groupbox)
        self.bobbin_board_thickness.setObjectName(u"bobbin_board_thickness")
        sizePolicy.setHeightForWidth(self.bobbin_board_thickness.sizePolicy().hasHeightForWidth())
        self.bobbin_board_thickness.setSizePolicy(sizePolicy)
        self.bobbin_board_thickness.setMinimumSize(QSize(55, 0))
        self.bobbin_board_thickness.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_3.addWidget(self.bobbin_board_thickness, 1, 2, 1, 1)

        self.side_margin = QLineEdit(self.bobbin_groupbox)
        self.side_margin.setObjectName(u"side_margin")
        sizePolicy.setHeightForWidth(self.side_margin.sizePolicy().hasHeightForWidth())
        self.side_margin.setSizePolicy(sizePolicy)
        self.side_margin.setMinimumSize(QSize(55, 0))
        self.side_margin.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_3.addWidget(self.side_margin, 3, 2, 1, 1)

        self.label_11 = QLabel(self.bobbin_groupbox)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 3, 0, 1, 1)

        self.label_5 = QLabel(self.bobbin_groupbox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.bobbin_groupbox)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.groupBox = QGroupBox(Geometry)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy4.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy4)
        self.groupBox.setMinimumSize(QSize(200, 130))
        self.groupBox.setMaximumSize(QSize(200, 131))
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.excitation_label = QLabel(self.groupBox)
        self.excitation_label.setObjectName(u"excitation_label")

        self.gridLayout_2.addWidget(self.excitation_label, 2, 0, 1, 1)

        self.excitation_combo = QComboBox(self.groupBox)
        self.excitation_combo.setObjectName(u"excitation_combo")
        self.excitation_combo.setMinimumSize(QSize(55, 0))
        self.excitation_combo.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_2.addWidget(self.excitation_combo, 1, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 1, 0, 1, 1)

        self.excitation_value = QLineEdit(self.groupBox)
        self.excitation_value.setObjectName(u"excitation_value")
        self.excitation_value.setMinimumSize(QSize(55, 0))
        self.excitation_value.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_2.addWidget(self.excitation_value, 2, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.adaptive_frequency = QLineEdit(self.groupBox)
        self.adaptive_frequency.setObjectName(u"adaptive_frequency")
        sizePolicy.setHeightForWidth(self.adaptive_frequency.sizePolicy().hasHeightForWidth())
        self.adaptive_frequency.setSizePolicy(sizePolicy)
        self.adaptive_frequency.setMinimumSize(QSize(55, 0))
        self.adaptive_frequency.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_2.addWidget(self.adaptive_frequency, 0, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_18)


        self.top_layout.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBox_2 = QGroupBox(Geometry)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.groupBox_2.setMinimumSize(QSize(575, 625))
        self.groupBox_2.setMaximumSize(QSize(575, 640))
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.parallel = QPushButton(self.groupBox_2)
        self.parallel.setObjectName(u"parallel")
        self.parallel.setMinimumSize(QSize(0, 25))
        self.parallel.setMaximumSize(QSize(90, 25))

        self.gridLayout_5.addWidget(self.parallel, 13, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_5.addWidget(self.label_7, 1, 1, 1, 1)

        self.delete_row = QPushButton(self.groupBox_2)
        self.delete_row.setObjectName(u"delete_row")

        self.gridLayout_5.addWidget(self.delete_row, 7, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_5.addWidget(self.label_3, 10, 1, 1, 1)

        self.verticalSpacer_15 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_15, 14, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_14, 17, 3, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_13, 3, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_5.addWidget(self.label_9, 1, 4, 1, 1)

        self.add_winding = QPushButton(self.groupBox_2)
        self.add_winding.setObjectName(u"add_winding")
        self.add_winding.setMinimumSize(QSize(0, 25))
        self.add_winding.setMaximumSize(QSize(90, 20))

        self.gridLayout_5.addWidget(self.add_winding, 4, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_5.addWidget(self.label_10, 11, 0, 1, 1)

        self.cond_material = QComboBox(self.groupBox_2)
        self.cond_material.addItem("")
        self.cond_material.addItem("")
        self.cond_material.setObjectName(u"cond_material")
        sizePolicy.setHeightForWidth(self.cond_material.sizePolicy().hasHeightForWidth())
        self.cond_material.setSizePolicy(sizePolicy)
        self.cond_material.setMinimumSize(QSize(90, 0))
        self.cond_material.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_5.addWidget(self.cond_material, 0, 5, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_5.addWidget(self.label_8, 0, 4, 1, 1)

        self.layer_spacing = QLineEdit(self.groupBox_2)
        self.layer_spacing.setObjectName(u"layer_spacing")
        self.layer_spacing.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_5.addWidget(self.layer_spacing, 1, 5, 1, 1)

        self.cond_type = QComboBox(self.groupBox_2)
        self.cond_type.addItem("")
        self.cond_type.addItem("")
        self.cond_type.setObjectName(u"cond_type")
        sizePolicy.setHeightForWidth(self.cond_type.sizePolicy().hasHeightForWidth())
        self.cond_type.setSizePolicy(sizePolicy)
        self.cond_type.setMinimumSize(QSize(100, 0))
        self.cond_type.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_5.addWidget(self.cond_type, 1, 2, 1, 1)

        self.connections_tree_widget = QTreeWidget(self.groupBox_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.connections_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.connections_tree_widget.setObjectName(u"connections_tree_widget")
        sizePolicy.setHeightForWidth(self.connections_tree_widget.sizePolicy().hasHeightForWidth())
        self.connections_tree_widget.setSizePolicy(sizePolicy)
        self.connections_tree_widget.setMaximumSize(QSize(450, 300))

        self.gridLayout_5.addWidget(self.connections_tree_widget, 11, 1, 6, 6)

        self.verticalSpacer_11 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_11, 16, 0, 1, 1)

        self.winding_tree_widget = QTreeWidget(self.groupBox_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.winding_tree_widget.setHeaderItem(__qtreewidgetitem1)
        self.winding_tree_widget.setObjectName(u"winding_tree_widget")
        sizePolicy.setHeightForWidth(self.winding_tree_widget.sizePolicy().hasHeightForWidth())
        self.winding_tree_widget.setSizePolicy(sizePolicy)
        self.winding_tree_widget.setMinimumSize(QSize(450, 300))
        self.winding_tree_widget.setMaximumSize(QSize(450, 300))

        self.gridLayout_5.addWidget(self.winding_tree_widget, 3, 1, 7, 6)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 6, 1, 1)

        self.series = QPushButton(self.groupBox_2)
        self.series.setObjectName(u"series")
        self.series.setMinimumSize(QSize(0, 25))
        self.series.setMaximumSize(QSize(90, 25))

        self.gridLayout_5.addWidget(self.series, 12, 0, 1, 1)

        self.add_layer = QPushButton(self.groupBox_2)
        self.add_layer.setObjectName(u"add_layer")
        self.add_layer.setMinimumSize(QSize(0, 25))
        self.add_layer.setMaximumSize(QSize(90, 16777215))

        self.gridLayout_5.addWidget(self.add_layer, 5, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_5.addWidget(self.label_6, 0, 1, 1, 1)

        self.build_combo = QComboBox(self.groupBox_2)
        self.build_combo.addItem("")
        self.build_combo.addItem("")
        self.build_combo.setObjectName(u"build_combo")
        self.build_combo.setMinimumSize(QSize(100, 0))
        self.build_combo.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_5.addWidget(self.build_combo, 0, 2, 1, 1)

        self.ungroup = QPushButton(self.groupBox_2)
        self.ungroup.setObjectName(u"ungroup")
        self.ungroup.setMinimumSize(QSize(91, 25))
        self.ungroup.setMaximumSize(QSize(90, 16777215))

        self.gridLayout_5.addWidget(self.ungroup, 15, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)

        self.winding_label = QLabel(self.groupBox_2)
        self.winding_label.setObjectName(u"winding_label")

        self.gridLayout_5.addWidget(self.winding_label, 10, 2, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_8, 6, 0, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_5, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_5 = QGroupBox(Geometry)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy6)
        self.groupBox_5.setMinimumSize(QSize(0, 80))
        self.groupBox_5.setMaximumSize(QSize(16777215, 100))
        self.groupBox_5.setSizeIncrement(QSize(0, 50))
        self.New_button = QPushButton(self.groupBox_5)
        self.New_button.setObjectName(u"New_button")
        self.New_button.setEnabled(True)
        self.New_button.setGeometry(QRect(440, 20, 130, 40))
        sizePolicy.setHeightForWidth(self.New_button.sizePolicy().hasHeightForWidth())
        self.New_button.setSizePolicy(sizePolicy)
        self.New_button.setMinimumSize(QSize(130, 40))
        self.New_button.setMaximumSize(QSize(115, 25))
        self.New_button.setIconSize(QSize(20, 20))
        self.save_etk = QPushButton(self.groupBox_5)
        self.save_etk.setObjectName(u"save_etk")
        self.save_etk.setGeometry(QRect(10, 20, 80, 40))
        self.save_etk.setMinimumSize(QSize(0, 40))
        self.save_etk.setMaximumSize(QSize(80, 25))

        self.verticalLayout.addWidget(self.groupBox_5)

        self.verticalSpacer_10 = QSpacerItem(20, 5000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_10)


        self.top_layout.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(5, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.top_layout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.top_layout)

        QWidget.setTabOrder(self.supplier_combo, self.type_combo)
        QWidget.setTabOrder(self.type_combo, self.model_combo)
        QWidget.setTabOrder(self.model_combo, self.material_combo)
        QWidget.setTabOrder(self.material_combo, self.D_1)
        QWidget.setTabOrder(self.D_1, self.D_2)
        QWidget.setTabOrder(self.D_2, self.D_3)
        QWidget.setTabOrder(self.D_3, self.D_4)
        QWidget.setTabOrder(self.D_4, self.D_5)
        QWidget.setTabOrder(self.D_5, self.D_6)
        QWidget.setTabOrder(self.D_6, self.D_7)
        QWidget.setTabOrder(self.D_7, self.D_8)
        QWidget.setTabOrder(self.D_8, self.airgap_combo)
        QWidget.setTabOrder(self.airgap_combo, self.airgap_value)
        QWidget.setTabOrder(self.airgap_value, self.core_image)
        QWidget.setTabOrder(self.core_image, self.bobbin_board_thickness)
        QWidget.setTabOrder(self.bobbin_board_thickness, self.top_margin)
        QWidget.setTabOrder(self.top_margin, self.side_margin)
        QWidget.setTabOrder(self.side_margin, self.adaptive_frequency)
        QWidget.setTabOrder(self.adaptive_frequency, self.excitation_combo)
        QWidget.setTabOrder(self.excitation_combo, self.excitation_value)
        QWidget.setTabOrder(self.excitation_value, self.build_combo)
        QWidget.setTabOrder(self.build_combo, self.cond_material)
        QWidget.setTabOrder(self.cond_material, self.cond_type)
        QWidget.setTabOrder(self.cond_type, self.layer_spacing)
        QWidget.setTabOrder(self.layer_spacing, self.add_winding)
        QWidget.setTabOrder(self.add_winding, self.add_layer)
        QWidget.setTabOrder(self.add_layer, self.delete_row)
        QWidget.setTabOrder(self.delete_row, self.winding_tree_widget)
        QWidget.setTabOrder(self.winding_tree_widget, self.series)
        QWidget.setTabOrder(self.series, self.parallel)
        QWidget.setTabOrder(self.parallel, self.ungroup)
        QWidget.setTabOrder(self.ungroup, self.connections_tree_widget)

        self.retranslateUi(Geometry)

        QMetaObject.connectSlotsByName(Geometry)
    # setupUi

    def retranslateUi(self, Geometry):
        Geometry.setWindowTitle(QCoreApplication.translate("Geometry", u"Form", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Geometry", u"Open PyETK", None))
        self.open_etk.setText(QCoreApplication.translate("Geometry", u"Open", None))
        self.label_13.setText(QCoreApplication.translate("Geometry", u"Browse", None))
        self.previous_example_button.setText(QCoreApplication.translate("Geometry", u"<", None))
        self.next_example_button.setText(QCoreApplication.translate("Geometry", u">", None))
        self.reset_examples.setText(QCoreApplication.translate("Geometry", u"Reset Example Dir", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Geometry", u"Core", None))
        self.D_1_label.setText(QCoreApplication.translate("Geometry", u"D_1, (mm)", None))
        self.D_6_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.custom_core_checkbox.setText(QCoreApplication.translate("Geometry", u"Custom Core", None))
        self.D_7_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.label_26.setText(QCoreApplication.translate("Geometry", u"Type", None))
        self.D_2_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.D_3_label.setText(QCoreApplication.translate("Geometry", u"D_3, (mm)", None))
        self.D_8_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.airgap_combo.setItemText(0, QCoreApplication.translate("Geometry", u"None", None))
        self.airgap_combo.setItemText(1, QCoreApplication.translate("Geometry", u"Center", None))
        self.airgap_combo.setItemText(2, QCoreApplication.translate("Geometry", u"Side", None))
        self.airgap_combo.setItemText(3, QCoreApplication.translate("Geometry", u"Both", None))

        self.D_5_label.setText(QCoreApplication.translate("Geometry", u"D_5, (mm)", None))
        self.D_5_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.D_6_label.setText(QCoreApplication.translate("Geometry", u"D_6, (mm)", None))
        self.D_2_label.setText(QCoreApplication.translate("Geometry", u"D_2, (mm)", None))
        self.D_7_label.setText(QCoreApplication.translate("Geometry", u"D_7, (mm)", None))
        self.D_8_label.setText(QCoreApplication.translate("Geometry", u"D_8, (mm)", None))
        self.D_3_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.D_4_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("Geometry", u"Core_Airgap", None))
        self.label_32.setText(QCoreApplication.translate("Geometry", u"Supplier", None))
        self.core_airgap_size.setText(QCoreApplication.translate("Geometry", u"Size, (mm)", None))
        self.label_27.setText(QCoreApplication.translate("Geometry", u"Model", None))
        self.label.setText(QCoreApplication.translate("Geometry", u"Material", None))
        self.D_1_ref.setText(QCoreApplication.translate("Geometry", u"TextLabel", None))
        self.D_4_label.setText(QCoreApplication.translate("Geometry", u"D_4, (mm)", None))
        self.bobbin_groupbox.setTitle(QCoreApplication.translate("Geometry", u"Bobbin and Margin", None))
        self.bobbin_label.setText(QCoreApplication.translate("Geometry", u"Bobbin Thickness, (mm)", None))
        self.label_11.setText(QCoreApplication.translate("Geometry", u"Side Margin, (mm)", None))
        self.label_5.setText(QCoreApplication.translate("Geometry", u"Top Margin, (mm)", None))
        self.groupBox.setTitle(QCoreApplication.translate("Geometry", u"Electrical (Side1)", None))
        self.excitation_label.setText(QCoreApplication.translate("Geometry", u"Voltage, (V)", None))
        self.label_12.setText(QCoreApplication.translate("Geometry", u"Excitation Type", None))
        self.label_4.setText(QCoreApplication.translate("Geometry", u"Frequency, (kHz)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Geometry", u"Winding", None))
        self.parallel.setText(QCoreApplication.translate("Geometry", u"Parallel", None))
        self.label_7.setText(QCoreApplication.translate("Geometry", u"Conductor Shape", None))
        self.delete_row.setText(QCoreApplication.translate("Geometry", u"Delete", None))
        self.label_3.setText(QCoreApplication.translate("Geometry", u"Winding", None))
        self.label_9.setText(QCoreApplication.translate("Geometry", u"Layer Spacing, (mm)", None))
        self.add_winding.setText(QCoreApplication.translate("Geometry", u"Add Winding", None))
        self.label_10.setText(QCoreApplication.translate("Geometry", u"Connect In:", None))
        self.cond_material.setItemText(0, QCoreApplication.translate("Geometry", u"Copper", None))
        self.cond_material.setItemText(1, QCoreApplication.translate("Geometry", u"Aluminium", None))

        self.label_8.setText(QCoreApplication.translate("Geometry", u"Conductor Material", None))
        self.cond_type.setItemText(0, QCoreApplication.translate("Geometry", u"Rectangular", None))
        self.cond_type.setItemText(1, QCoreApplication.translate("Geometry", u"Circular", None))

        self.series.setText(QCoreApplication.translate("Geometry", u"Series", None))
        self.add_layer.setText(QCoreApplication.translate("Geometry", u"Add Layer", None))
        self.label_6.setText(QCoreApplication.translate("Geometry", u"Winding Build", None))
        self.build_combo.setItemText(0, QCoreApplication.translate("Geometry", u"Wound", None))
        self.build_combo.setItemText(1, QCoreApplication.translate("Geometry", u"Planar", None))

        self.ungroup.setText(QCoreApplication.translate("Geometry", u"Disconnect", None))
        self.winding_label.setText(QCoreApplication.translate("Geometry", u"winding_label", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Geometry", u"Save and Create Transformer", None))
        self.New_button.setText(QCoreApplication.translate("Geometry", u"Create Transformer", None))
        self.save_etk.setText(QCoreApplication.translate("Geometry", u"Save As", None))
    # retranslateUi

