
import json
from pathlib import Path
import sys

from PySide6.QtCore import QThread
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTreeWidget
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.electronic_transformer.ui.common.database_manager import database_manager
# Default user interface properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import fe_properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import gui_properties
from ansys.aedt.toolkits.electronic_transformer.ui.models import AirGapConfig
from ansys.aedt.toolkits.electronic_transformer.ui.common.data_manager import data_manager
from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import freq_units
from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import freq_scale
from ansys.aedt.toolkits.electronic_transformer.ui.common.units_and_scales import scale_units

from ansys.aedt.toolkits.electronic_transformer.ui.windows.main.main_column import Ui_LeftColumn
from ansys.aedt.toolkits.electronic_transformer.ui.windows.main.main_page import Ui_Geometry

# Path to examples
etk_root = Path(__file__).resolve().parents[8]
if hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    example_files = Path(sys._MEIPASS) / 'examples'
else:
    example_files = etk_root / "tests" / "backend" / "json_files"

class CreateGeometryThread(QThread):
    """Manages the geometry creation thread."""

    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design):
        """Initialize the geometry creation thread.
        Args:
            app: The main application instance.
            selected_project (str): The selected project.
            selected_design (str): The selected design.
        """

        super().__init__()
        self.geometry_menu = app
        self.main_window = app.main_window
        self.selected_project = selected_project
        self.selected_design = selected_design

    def run(self):
        """Run the geometry creation thread."""
        success = self.main_window.create_model(self.selected_project, self.selected_design)
        self.finished_signal.emit(success)


class GeometryMenu(object):
    """Manages the UI geometry menu."""

    def __init__(self, main_window):
        """Initialize the geometry menu.

        Args:
            main_window (QMainWindow): Main window that contains the menu.
        """
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui
        self._importing_connections = False

        # Adjust size of Main Window
        min_width = 1520
        min_height = 1000
        self.main_window.setMinimumSize(min_width, min_height)

        # Add page
        geometry_menu_index = self.ui.add_page(Ui_Geometry)
        self.ui.load_pages.pages.setCurrentIndex(geometry_menu_index)
        self.geometry_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.geometry_column_widget = new_column_widget
        self.geometry_column_vertical_layout = new_ui.geometry_vertical_layout

        self.geometry_thread = None

        self.top_layout = self.geometry_menu_widget.findChild(QHBoxLayout, "top_layout")
        self.button_layout = self.geometry_menu_widget.findChild(QHBoxLayout, "button_layout")

        # Initialize front end properties
        self.properties = fe_properties
        self.gui_properties = gui_properties
        self.data_manager = data_manager
        self.database_manager = database_manager

        # ───────────────────────────────
        # Core Group
        # ───────────────────────────────
        # Assign instance variables to QComboBoxes
        self.custom_core = self.geometry_menu_widget.findChild(QCheckBox,"custom_core_checkbox")
        self.supplier_combo = self.geometry_menu_widget.findChild(QComboBox, "supplier_combo")
        self.type_combo = self.geometry_menu_widget.findChild(QComboBox, "type_combo")
        self.model_combo = self.geometry_menu_widget.findChild(QComboBox, "model_combo")
        self.material_combo = self.geometry_menu_widget.findChild(QComboBox, "material_combo")

        # Assign to QGraphicsView for showing core geometry in window
        self.core_image = self.geometry_menu_widget.findChild(QGraphicsView, "core_image")

        self.airgap_combo = self.geometry_menu_widget.findChild(QComboBox, "airgap_combo")
        self.airgap_value = self.geometry_menu_widget.findChild(QLineEdit, "airgap_value")
        self.airgap_value.setText("0.0")
        self.airgap_combo_label = self.geometry_menu_widget.findChild(QLabel, "core_airgap_size")

        # Assign to QLineEdit and QLabel for core dimensions
        for key, value in self.properties.core.dimensions.items():
            setattr(self, key + "_label", self.geometry_menu_widget.findChild(QLabel, key + "_label"))
            setattr(self, key, self.geometry_menu_widget.findChild(QLineEdit, key))
            setattr(self, key + "_ref", self.geometry_menu_widget.findChild(QLabel, key + "_ref"))
            getattr(self, key).setReadOnly(True)
            line_edit = getattr(self,key)
            line_edit.editingFinished.connect(lambda k=key, le=line_edit:self._update_core_dimensions({"dimensions":{k:le.text()}}))

        # Initialize last airgap value
        self._last_valid_airgap_value = "0.0"

        # Import core dimensions and material properties
        self.cores_database = self.database_manager.cores_database
        self.materials_database = self.database_manager.materials_database
        self.core_materials = []

        # Connect UI event signals (callbacks) to their corresponding slots (methods)
        self.supplier_combo.currentIndexChanged.connect(self._update_core_types)
        self.type_combo.currentIndexChanged.connect(self._update_core_models)
        self.model_combo.currentIndexChanged.connect(self._update_core_dimensions)
        self.airgap_combo.currentTextChanged.connect(self._update_airgap_type)
        self.custom_core.toggled.connect(self._update_core_dimensions)

        # ───────────────────────────────
        # Bobbin and Margin
        # ───────────────────────────────
        # Assign instance variable
        self.bobbin_groupbox = self.geometry_menu_widget.findChild(QGroupBox, "bobbin_groupbox")
        self.bobbin_board_thickness = self.geometry_menu_widget.findChild(QLineEdit, "bobbin_board_thickness")
        self.top_margin = self.geometry_menu_widget.findChild(QLineEdit, "top_margin")
        self.side_margin = self.geometry_menu_widget.findChild(QLineEdit, "side_margin")
        self.bobbin_label = self.geometry_menu_widget.findChild(QLabel, "bobbin_label")
        self.bobbin_checkbox = self.geometry_column_widget.findChild(QCheckBox, "bobbin_checkbox")

        # Populate UI with default values
        self.bobbin_checkbox.setChecked(self.gui_properties.settings.include_bobbin)
        self.bobbin_board_thickness.setText(str(self.gui_properties.bobbin_board_and_margin.thickness))
        self.top_margin.setText(str(self.gui_properties.bobbin_board_and_margin.top_margin))
        self.side_margin.setText(str(self.gui_properties.bobbin_board_and_margin.side_margin))

        # ───────────────────────────────
        # Electrical
        # ───────────────────────────────
        # Assign instance variables to QWidgets
        self.adaptive_frequency = self.geometry_menu_widget.findChild(QLineEdit, "adaptive_frequency")
        self.excitation_combo = self.geometry_menu_widget.findChild(QComboBox, "excitation_combo")
        self.excitation_value = self.geometry_menu_widget.findChild(QLineEdit, "excitation_value")
        self.excitation_label = self.geometry_menu_widget.findChild(QLabel, "excitation_label")

        # Populate UI with default values
        self.adaptive_frequency.setText(str(self.gui_properties.electrical.adaptive_frequency))
        self.excitation_combo.addItem("Voltage")
        self.excitation_combo.addItem("Current")
        self.excitation_combo.setCurrentText(self.gui_properties.electrical.excitation_strategy)
        self.excitation_combo.setItemData(0, str(self.gui_properties.electrical.voltage), Qt.UserRole)
        self.excitation_combo.setItemData(1, str(self.gui_properties.electrical.current), Qt.UserRole)

        # Connect UI event signals (callbacks) to their corresponding slots (methods)
        self.excitation_combo.currentIndexChanged.connect(self._excitation_change)

        # Set Initial State
        self._excitation_change()

        # ───────────────────────────────
        # Winding Group
        # ───────────────────────────────
        # Assign instance variables to QWidgets
        self.winding_tree_widget = self.geometry_menu_widget.findChild(QTreeWidget, "winding_tree_widget")
        self.add_winding = self.geometry_menu_widget.findChild(QPushButton, "add_winding")
        self.add_layer = self.geometry_menu_widget.findChild(QPushButton, "add_layer")
        self.cond_type = self.geometry_menu_widget.findChild(QComboBox, "cond_type")
        self.cond_material = self.geometry_menu_widget.findChild(QComboBox, "cond_material")
        self.build_combo = self.geometry_menu_widget.findChild(QComboBox, "build_combo")

        self.connections_tree_widget = self.geometry_menu_widget.findChild(QTreeWidget, "connections_tree_widget")
        self.layer_spacing = self.geometry_menu_widget.findChild(QLineEdit, "layer_spacing")
        self.series = self.geometry_menu_widget.findChild(QPushButton, "series")
        self.parallel = self.geometry_menu_widget.findChild(QPushButton, "parallel")
        self.ungroup = self.geometry_menu_widget.findChild(QPushButton, "ungroup")

        self.winding_label = self.geometry_menu_widget.findChild(QLabel, "winding_label")

        # # Default Winding and Layer values
        self._conductor_width = 0.2
        self._conductor_height = 2.2
        self._conductor_diameter = 1.0
        self._insulation_thickness = 0.05
        self._turn_number = 10
        self._default_side_load = 1e-6
        self._segments_number = 8

        # Populate UI with default values
        self.layer_spacing.setText(str(self.gui_properties.winding.layer_spacing))

        # Connect UI event signals (callbacks) to their corresponding slots (methods)
        self.add_winding.clicked.connect(self._add_winding)
        self.add_layer.clicked.connect(self._add_layer)
        self.cond_type.currentIndexChanged.connect(self._conductor_type_changed)
        self.winding_tree_widget.itemChanged.connect(self._winding_item_changed)
        self.build_combo.currentIndexChanged.connect(self._update_build)
        self.winding_tree_widget.itemSelectionChanged.connect(self._stash_connections)

        self.series.clicked.connect(lambda: self.connect_connections(connection_type="Series"))
        self.parallel.clicked.connect(lambda: self.connect_connections(connection_type="Parallel"))
        self.ungroup.clicked.connect(self._disconnect)

        # Set Initial State
        self._populate_winding_tree()

        # Add first winding so window isn't empty
        self._add_winding()

        # ───────────────────────────────
        # File Handling
        # ───────────────────────────────
        self._project_path = ""

        # ───────────────────────────────
        # Maxwell Settings
        # ───────────────────────────────
        # Assign instance variables to QWidgets
        self.draw_skin_layers = self.geometry_column_widget.findChild(QCheckBox, "draw_skin_layers")
        self.full_model = self.geometry_column_widget.findChild(QCheckBox, "full_model")
        self.skip_check = self.geometry_column_widget.findChild(QCheckBox, "skip_check")

        self.number_passes = self.geometry_column_widget.findChild(QLineEdit, "number_passes")
        self.percentage_error = self.geometry_column_widget.findChild(QLineEdit, "percentage_error")
        self.segmentation_angle = self.geometry_column_widget.findChild(QLineEdit, "segmentation_angle")
        self.offset = self.geometry_column_widget.findChild(QLineEdit, "offset")

        self.frequency_sweep = self.geometry_column_widget.findChild(QCheckBox, "frequency_sweep")
        self.start_frequency = self.geometry_column_widget.findChild(QLineEdit, "start_frequency")
        self.start_frequency_unit = self.geometry_column_widget.findChild(QComboBox, "start_frequency_unit")

        self.stop_frequency = self.geometry_column_widget.findChild(QLineEdit, "stop_frequency")
        self.stop_frequency_unit = self.geometry_column_widget.findChild(QComboBox, "stop_frequency_unit")
        self.samples = self.geometry_column_widget.findChild(QLineEdit, "samples")
        self.scale = self.geometry_column_widget.findChild(QComboBox, "scale_combo")

        # Checks
        self._skip_check = True

        # Populate UI with Default values
        self.draw_skin_layers.setChecked(self.gui_properties.settings.draw_skin_layers)
        self.full_model.setChecked(self.gui_properties.settings.full_model)
        self.skip_check.setChecked(self._skip_check)

        self.number_passes.setText(str(self.gui_properties.settings.number_passes))
        self.percentage_error.setText(str(self.gui_properties.settings.percentage_error))
        self.segmentation_angle.setText(str(self.gui_properties.settings.segmentation_angle))
        self.offset.setText(str(self.gui_properties.settings.offset))

        self.frequency_sweep.setChecked(self.gui_properties.settings.frequency_sweep_definition.frequency_sweep)
        self.start_frequency.setText(str(self.gui_properties.settings.frequency_sweep_definition.start_frequency))
        self.start_frequency_unit.addItems(freq_units)
        self.start_frequency_unit.setCurrentText(self.gui_properties.settings.frequency_sweep_definition.start_frequency_unit)
        self.stop_frequency.setText(str(self.gui_properties.settings.frequency_sweep_definition.stop_frequency))
        self.stop_frequency_unit.addItems(freq_units)
        self.stop_frequency_unit.setCurrentText(self.gui_properties.settings.frequency_sweep_definition.stop_frequency_unit)
        self.samples.setText(str(self.gui_properties.settings.frequency_sweep_definition.samples))
        self.scale.addItems(scale_units)
        self.scale.setCurrentText(self.gui_properties.settings.frequency_sweep_definition.scale)

        # Connect UI event signals (callbacks) to their corresponding slots (methods)
        self.frequency_sweep.toggled.connect(self._update_frequency_sweep)
        self.start_frequency.textEdited.connect(lambda:self._update_frequency_sweep())
        self.stop_frequency.textEdited.connect(lambda:self._update_frequency_sweep())
        self.start_frequency_unit.currentIndexChanged.connect(lambda:self._update_frequency_sweep())
        self.stop_frequency_unit.currentIndexChanged.connect(lambda:self._update_frequency_sweep())

        # Stylesheet to show startfreq > stopfreq
        self.main_window.setStyleSheet(
            'QLineEdit[invalid="true"] { border: 2px solid red; border-radius: 4px; }'
        )

        # ───────────────────────────────
        # UI Formatting
        # ───────────────────────────────
        # Restrict what can be entered into the LineEdit fields of the UI
        # Numbers only
        # Iterate over all attributes of self to find those that contain QLineEdit
        line_edits = []

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QLineEdit):
                line_edits.append(attr)

        # Construct validator restrictions for QLineEdit fields in UI
        validator = QDoubleValidator()
        validator.setBottom(0.0)
        validator.setTop(1000.0)
        validator.setDecimals(4)

        # Apply validator restrictions to fields
        for line_edit in line_edits:
            line_edit.setValidator(validator)

        self.connections_tree_widget.setHeaderLabels(["Connections"])

        self.winding_tree_widget.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.EditKeyPressed)
        self.winding_tree_widget.setDragDropMode(QTreeWidget.InternalMove)
        self.winding_tree_widget.setDefaultDropAction(Qt.MoveAction)
        self.winding_tree_widget.setSelectionMode(QTreeWidget.SingleSelection)
        self.winding_tree_widget.setDragEnabled(True)
        self.winding_tree_widget.setAcceptDrops(True)
        self.winding_tree_widget.setDropIndicatorShown(True)
        self.winding_tree_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Allows ctrl-Click
        self.connections_tree_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Allows ctrl-Click

        # UI Controls: Button Setup
        self.example_button = self.geometry_menu_widget.findChild(QPushButton, "open_etk")
        self.example_button.clicked.connect(self.example_button_clicked)
        self.next_example_button = self.geometry_menu_widget.findChild(QPushButton, "next_example_button")
        self.previous_example_button = self.geometry_menu_widget.findChild(QPushButton, "previous_example_button")
        self.example_name = self.geometry_menu_widget.findChild(QLineEdit, "example_name")
        self.save_etk = self.geometry_menu_widget.findChild(QPushButton, "save_etk")

        # Load all example files from directory and add placeholder [None] for "Start New design"
        self.example_files = sorted(example_files.glob("*.json")) + [None]
        self.current_example_index = 0

        # Connect signals
        self.next_example_button.clicked.connect(lambda: self.load_example(direction="Forwards"))
        self.previous_example_button.clicked.connect(lambda: self.load_example(direction="Backwards"))
        self.save_etk.clicked.connect(self.save_button_clicked)

        # Populate UI widgets before signals are assigned to avoid misfires
        self._update_supplier()
        self._update_core_materials()
        self._update_airgap_type(airgap=None)

        self.new_filename="NewDesign"
        self.example_name.setText(self.new_filename)


    def _set_invalid(self, widget, invalid, tip= ""):
        """Manage the style of a widget based on invalid entries.

        Args:
            widget (QWidget): The widget to style.
            invalid (bool): Whether the widget's content is invalid.
            tip (str, optional): The tooltip to display. Defaults to "".
        """
        widget.setProperty("invalid", invalid)
        widget.setToolTip(tip if invalid else "")
        # Apply style refresh in case border no longer needed
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)
        widget.update()

    def load_example(self, direction):
        """Load an example file by stepping forwards or backwards.

        Args:
            direction (str): The direction to step, either "Forwards" or "Backwards".
        """
        step = 1 if direction == "Forwards" else -1

        # Catch case where user presses Cancel in File Dialog window
        if self.example_files:
            self.custom_core.setChecked(False)
            # Navigation through examples is looped, looping index is worked out here
            self.current_example_index = (self.current_example_index + step) % len(self.example_files)
            self._load_etk_json(self.example_files[self.current_example_index])

    def _load_etk_json(self, path):
        """Load a JSON file, display its filename in the UI, and update the UI.
        Args:
            path (pathlib.Path): The path to the JSON file.
        """
        # Reset UI defaults
        if path is None:
            self.example_name.setText(self.new_filename)
        else:
            msg, is_valid = self.data_manager._import_data_from_json(path)
            self.ui.update_logger(msg)

            if is_valid:
                self._write_ui_data()
                self.example_name.setText(path.name)

    def setup(self):
        """Set up the geometry menu."""

        self.new_button = self.geometry_menu_widget.findChild(QPushButton, "New_button")
        self.new_button.clicked.connect(self.geometry_button_clicked)

    def geometry_button_clicked(self):
        """Handle the geometry button click event."""
        if not self.main_window.settings_menu.aedt_thread or (
            hasattr(self.main_window.settings_menu.aedt_thread, "aedt_launched")
            and not self.main_window.settings_menu.aedt_thread.aedt_launched
        ):
            msg = "AEDT not launched."
            self.ui.update_logger(msg)
            return False

        if self.geometry_thread and self.geometry_thread.isRunning() or self.main_window.backend_busy():
            msg = "Toolkit running"
            self.ui.update_logger(msg)
            self.main_window.logger.debug(msg)
            return False

        self._read_ui_data()
        self.data_manager._update_frontend_properties()

        be_properties = self.main_window.get_properties()
        if be_properties.get("active_project"):
            self.ui.update_progress(0)
            selected_project = self.main_window.home_menu.project_combobox.currentText()
            selected_design = self.main_window.home_menu.design_combobox.currentText()

            # Start a separate thread for the backend call
            self.geometry_thread = CreateGeometryThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
            )
            self.geometry_thread.finished_signal.connect(self.geometry_created_finished)

            msg = "Creating transformer model..."
            self.ui.update_logger(msg)
            self.geometry_thread.start()

        else:
            self.ui.update_logger("Toolkit not connected to AEDT.")

    def geometry_created_finished(self, success):
        """Handle the geometry created finished event.
        Args:
            success (bool): Whether the geometry creation was successful.
        """
        self.ui.update_progress(100)
        selected_project = self.main_window.home_menu.project_combobox.currentText()
        selected_design = self.main_window.home_menu.design_combobox.currentText()

        properties = self.main_window.get_properties()
        active_project = self.main_window.get_project_name(properties["active_project"])
        active_design = properties["active_design"]
        if active_project != selected_project or active_design != selected_design:
            self.main_window.home_menu.update_project()
            self.main_window.home_menu.update_design()

        if success:
            msg = "...Transformer model created."
            self.ui.update_logger(msg)
        else:
            msg = f"Failed backend call: {self.main_window.url}"
            self.ui.update_logger(msg)

    def _update_core_info(self):
        self.gui_properties.core.supplier = self.supplier_combo.currentText()
        self.gui_properties.core.type = self.type_combo.currentText()
        self.gui_properties.core.model = self.model_combo.currentText()

    def _update_supplier(self):
        """Extract supplier names from ``cores_database`` and populate the supplier combo box."""
        self.supplier_combo.blockSignals(True)
        self.supplier_combo.clear()

        suppliers = sorted(self.cores_database, key=str.lower)
        for supplier_name in suppliers:
            self.supplier_combo.addItem(supplier_name)

        self.supplier_combo.blockSignals(False)
        self._update_core_types()

    def _update_core_types(self):
        """Extract core types from ``cores_database`` and populate the core type combo box."""

        self._update_core_info()

        self.type_combo.blockSignals(True)
        self.type_combo.clear()

        for core_type in self.cores_database[self.gui_properties.core.supplier].keys():
            self.type_combo.addItem(core_type)

        self.type_combo.blockSignals(False)
        self._update_core_models()

    def _update_core_models(self):
        """Extract core models from ``cores_database`` and populate the core model combo box."""
        self._update_core_info()

        self.model_combo.blockSignals(True)
        self.model_combo.clear()

        for model in self.cores_database[self.gui_properties.core.supplier][self.gui_properties.core.type].keys():
            self.model_combo.addItem(model)

        self.model_combo.blockSignals(False)

        self.show_core_img()
        self._update_core_dimensions()

    def _update_core_materials(self):
        """Read core materials from input data and populate the material combo box."""
        self.material_combo.clear()

        for key in sorted(self.materials_database["core"].keys(), key=lambda x: x.lower()):
            self.core_materials.append(key)

        for index, value in enumerate(self.core_materials):
            self.material_combo.addItem("")
            self.material_combo.setItemText(index, self.core_materials[index])

    def _update_core_dimensions(self, core_data=None):
        """Show only the core dimension fields needed for the selected core model.

            This method updates fields with their corresponding values, which can be from the model
            or a JSON file that contains custom values. It hides any unused dimension fields and
            shows the nominal value as a reference next to any custom one.
            Args:
                core_data (dict, optional): A dictionary containing core data. Defaults to ``None``.
        """
        self._update_core_info()

        selected_dimensions = self.cores_database[self.gui_properties.core.supplier][self.gui_properties.core.type][self.gui_properties.core.model]
        unused_values = ["", " "]
        json_dims = {}
        core_dimensions = {}

        # Returns Bool state of custom core checkbox
        custom_core = self.custom_core.isChecked()

        for dim_label, dim_value in self.gui_properties.core.dimensions.items():
            getattr(self, dim_label).setReadOnly(not custom_core)

        # Combine custom core dims with Nominal model ones.
        if isinstance(core_data, dict):
            json_dims = core_data.get("dimensions", {})
            for json_dim, json_value in json_dims.items():
                if json_dim in selected_dimensions:
                    try:
                        if float(json_value) != float(selected_dimensions[json_dim]):
                            custom_core = True
                            self.custom_core.setChecked(True)
                        core_dimensions[json_dim] = float(json_value)
                    except (TypeError, ValueError):
                        continue

        # Deactivate combo boxes when custom core selected
        for combo in (self.supplier_combo, self.type_combo, self.model_combo):
            combo.setEnabled(not custom_core)

        # Update each dimension field
        for nominal_dim, nominal_val in selected_dimensions.items():
            line_edit = getattr(self, nominal_dim)
            label = getattr(self, nominal_dim + "_label")
            ref_label = getattr(self, nominal_dim + "_ref")
            line_edit.blockSignals(True)

            # Hide unused dimensions
            if nominal_val in unused_values:
                line_edit.hide()
                label.hide()
                ref_label.hide()
                continue
            else:
                line_edit.show()
                label.show()
                ref_label.show()

            # Nominal values from database
            try:
                nominal_val = float(nominal_val)
            except (TypeError, ValueError):
                nominal_val = 0.0

            # When Custom Core is enabled allow editing and show reference value if different
            current_val = core_dimensions.get(nominal_dim,float(json_dims.get(nominal_dim, nominal_val)))

            if custom_core:
                line_edit.setReadOnly(False)
                line_edit.setText(str(current_val))
                if current_val != nominal_val:
                    ref_label.setText("(" + str(nominal_val) + ")")
                    ref_label.show()
                else:
                    ref_label.clear()
                    ref_label.hide()
            else:
                line_edit.setReadOnly(True)
                line_edit.setText(str(nominal_val))
                ref_label.clear()
                ref_label.hide()

            line_edit.blockSignals(False)

            # Update core dimensions dictionary with values
            core_dimensions[nominal_dim] = float(line_edit.text())
        self.gui_properties.core.dimensions = core_dimensions

    def show_core_img(self):
        """Display the expected core type image."""
        # Create a new QGraphicsScene
        scene = QGraphicsScene()

        # Load the image into a QPixmap
        image_dir = Path(__file__).parents[1] / "images"
        image_filename = self.type_combo.currentText() + "Core.png"
        image_path = QPixmap(str(image_dir / image_filename))

        # Create a QGraphicsPixmapItem from the QPixmap
        item = QGraphicsPixmapItem(image_path)

        # Add the QGraphicsPixmapItem to the scene
        scene.addItem(item)

        # Set the scene to the QGraphicsView
        self.core_image.setScene(scene)

    def _update_airgap_type(self, airgap):
        """Manage the airgap combo box and input based on the selected airgap type.
        This method works for both UI changes and programmatically from a JSON import.
        Args:
            airgap (str or dict): The airgap type.
        """
        # Initial population, None here is airgap attribute not supplied, "None" is the string for combo box.

        if airgap is None:
            enabled = False
            airgap_type = "None"
            airgap_value = "0.0"

        # UI selection emits combo box signal
        elif isinstance(airgap, str):
            airgap_type = airgap

            if airgap_type in ("Center", "Side", "Both"):
                enabled = True

                # Use last valid value if switching back from "None"
                current_text = self.airgap_value.text()
                airgap_value = self._last_valid_airgap_value if current_text == "0.0" else current_text
                self._last_valid_airgap_value = str(airgap_value)

            # Stash existing value before overwriting with 0.0 for 'None' airgap
            else:
                enabled = False
                current_text = self.airgap_value.text()

                if current_text != "0.0":
                    self._last_valid_airgap_value = str(current_text)

                airgap_value = "0.0"

        # JSON import, airgap is in same format as dict from JSON file.
        # JSON schema will have already checked below upon import
        else:
            enabled = airgap.enabled
            airgap_type = airgap.location
            airgap_value = airgap.height

            if enabled and airgap_value != "0.0":
                self._last_valid_airgap_value = str(airgap_value)

        # Update UI
        self.airgap_combo.setCurrentText(airgap_type)
        self.airgap_combo_label.setEnabled(enabled)
        self.airgap_value.setEnabled(enabled)
        self.airgap_value.setText(str(airgap_value))

    def _update_build(self):
        """Manage the UI display based on the selected build, either ``Wound`` or ``Planar``.
        Planar components can only be constructed with rectangular wire. Wound components can be
        constructed from either rectangular or circular wire."""

        header_item = self.winding_tree_widget.headerItem()

        if self.build_combo.currentIndex() == 1:
            self.bobbin_label.setText("Board Thickness, (mm)")
            self.cond_type.setCurrentText("Rectangular")
            self.cond_type.setDisabled(True)
            self.bobbin_groupbox.setTitle("Board and Margin")
            self.bobbin_checkbox.setText("Include Board")
            header_item.setText(3, "Turn Spacing\n(mm)")

        else:
            self.bobbin_label.setText("Bobbin Thickness, (mm)")
            self.cond_type.setDisabled(False)
            self.bobbin_groupbox.setTitle("Bobbin and Margin")
            self.bobbin_checkbox.setText("Include Bobbin")
            header_item.setText(3, "Insulation\n(mm)")

        self.gui_properties.winding.layer_type = self.build_combo.currentText()

    def _excitation_change(self):
        """Switch between voltage and current using values stored in ``UserRole``."""
        line_edit = self.excitation_value

        # Store existing value from linedit in UserRole
        prev_index = getattr(self, "_prev_excitation_index", None)
        if prev_index is not None:
            self.excitation_combo.setItemData(prev_index, line_edit.text().strip(), Qt.UserRole)

        new_index = self.excitation_combo.currentIndex()

        # Update the UI text label to match changed excitation type
        if new_index == 0:
            self.excitation_label.setText("Voltage, (V)")
        else:
            self.excitation_label.setText("Current, (A)")

        # Restore the stored value
        stored_value = self.excitation_combo.itemData(new_index, Qt.UserRole)
        line_edit.setText(str(stored_value))

        # Update previous index
        self._prev_excitation_index = new_index

    def _populate_winding_tree(self):
        """Populate the winding tree with initial headings and sizes."""

        headers = [
            "",
            "Turns",
            "",
            "Cond_Insulation",
            "Side Load",
        ]

        self.winding_tree_widget.setHeaderLabels(headers)

        # Set header size to display two rows in title
        hdr = self.winding_tree_widget.header()
        hdr.setDefaultAlignment(Qt.AlignCenter)
        hdr.setFixedHeight(50)

        # Hard wired column widths...
        self.winding_tree_widget.setColumnWidth(0, 95)  # Layer label
        self.winding_tree_widget.setColumnWidth(1, 40)  # Turns
        self.winding_tree_widget.setColumnWidth(2, 110)  # Cond Size
        self.winding_tree_widget.setColumnWidth(3, 95)  # Turn Spacing / Wire Insulation
        self.winding_tree_widget.setColumnWidth(4, 40)  # Side Load

        # Conductor column is added in this method
        self._conductor_type_changed()

    def _add_winding(self):
        """Add a new winding with a single layer to the winding tree."""
        next_side_index = self.winding_tree_widget.topLevelItemCount() + 1

        new_winding = QTreeWidgetItem(
            [
                "Side" + str(next_side_index),
                "",
                "",
                "",
                str(self._default_side_load),
            ]
        )
        new_winding.setFlags(new_winding.flags() | Qt.ItemIsEditable)
        new_winding.setData(
            0,
            Qt.UserRole,
            {
                "type": "Winding",
                "side": next_side_index,
                "side_load": self._default_side_load,
            },
        )

        self.winding_tree_widget.addTopLevelItem(new_winding)
        self.winding_tree_widget.setCurrentItem(new_winding)

        self._add_layer()

    def _conductor_type_changed(self):
        """Handle the conductor type change event.
        When the user changes the conductor type, this method populates the conductor column
        from ``UserRole`` and updates the conductor column header.
        """
        # First change winding tree header to match selected conductor type
        cond_text = self.cond_type.currentText()
        header_item = self.winding_tree_widget.headerItem()

        if cond_text == "Circular":
            header_item.setText(2, "Conductor_Size\n(Diameter)")
        else:
            header_item.setText(2, "Conductor_Size\n(Width x Height)")

        # Then retrieve values for that conductor from UserRole
        tree = self.winding_tree_widget
        tree.blockSignals(True)

        for winding_index in range(tree.topLevelItemCount()):
            winding = tree.topLevelItem(winding_index)

            for layer_index in range(winding.childCount()):
                row = winding.child(layer_index)
                data = row.data(0, Qt.UserRole)

                cond = data.get("conductor")
                if cond_text == "Circular":
                    dia = cond.get("diameter")
                    if dia is None:
                        dia = self._conductor_diameter
                    row.setText(2, str(dia))

                else:
                    width = cond.get("width")
                    height = cond.get("height")
                    if width or height is None:
                        width = self._conductor_width
                        height = self._conductor_height
                    row.setText(2, (str(width) + " x " + str(height)))

        tree.blockSignals(False)
        self.gui_properties.winding.conductor_type = cond_text

    def _winding_item_changed(self, item, column):
        """Update ``UserRole`` with modified winding tree entries.
        Args:
            item (QTreeWidgetItem): The item that was changed.
            column (int): The column of the changed item.
        """
        data = item.data(0, Qt.UserRole)
        row_type = data.get("type")

        if row_type == "Layer":
            if column == 1:
                data["turns"] = int(item.text(1))

            elif column == 2:
                mode = self.cond_type.currentText()
                cond = data.setdefault("conductor", {})

                raw_input = (item.text(2) or "").strip()
                parts = raw_input.replace("x", " ").split()

                if mode == "Circular":
                    dia = float(parts[0])
                    cond["diameter"] = dia
                else:
                    width = float(parts[0])
                    height = float(parts[1])
                    cond["width"] = width
                    cond["height"] = height

            elif column == 3:
                data["insulation"] = float(item.text(3))

            elif column == 4:
                return

        elif row_type == "Winding":
            if column == 4:
                data["side_load"] = float(item.text(4))
            else:
                return

        item.setData(0, Qt.UserRole, data)

        if row_type == "Layer":
            self.gui_properties.winding.layers_definition = self._update_layers_definition()

        elif row_type == "Winding":
            self.gui_properties.winding.side_loads = self._update_loads_definition()

    def _add_layer(self):
        """Add a new layer to the selected winding and update the corresponding connection tree.
        - If no connections exist, the layer is added to a new row.
        - If one layer row already exists, both are connected in series as ``Series(L1, L2)``.
        - If there is exactly one flat series or parallel connection, the new layer is appended,
          for example, ``Series(L1, L2, L3)``.
        - If the connection is more complicated than the preceding cases, the new row is added as a
          new top-level layer row.
        - If one top-level row exists, the ``update_connections_def()`` method is run.
        """

        # Get the selected winding or parent winding of selected layer
        current_row = self.winding_tree_widget.currentItem()
        current_winding = current_row
        while current_winding and current_winding.parent():
            current_winding = current_winding.parent()

        # Work out next free layer ID
        root = self.winding_tree_widget.invisibleRootItem()
        total_layers = sum(root.child(winding).childCount() for winding in range(root.childCount()))
        new_layer_id = str(total_layers + 1)

        # Construct layer data
        layer_data = {
            "type": "Layer",
            "id": new_layer_id,
            "turns": self._turn_number,
            "insulation": self._insulation_thickness,
            "conductor": {
                "width": self._conductor_width,
                "height": self._conductor_height,
                "diameter": self._conductor_diameter,
            },
        }

        # Choose correct conductor values based on conductor type
        cond_type = self.cond_type.currentText()
        conductor = layer_data["conductor"]

        if cond_type == "Circular":
            conductor_display = str(conductor["diameter"])
        else:
            conductor_display = str(conductor["width"]) + " x " + str(conductor["height"])

        self.winding_tree_widget.blockSignals(True)

        # Construct object with the new layers detail in it
        new_layer = QTreeWidgetItem(
            [
                "Layer " + str(new_layer_id),
                str(layer_data["turns"]),
                conductor_display,
                str(layer_data["insulation"]),
                "",
            ]
        )

        new_layer.setFlags(new_layer.flags() | Qt.ItemIsEditable)
        new_layer.setData(0, Qt.UserRole, layer_data)

        current_winding.addChild(new_layer)

        self.winding_tree_widget.expandItem(current_winding)
        self.winding_tree_widget.setCurrentItem(new_layer)
        self.winding_tree_widget.blockSignals(False)

        # Handles adding a layer on top of a previously imported json connection
        side_payload = current_winding.data(0, Qt.UserRole)

        # Move saved connection into WIP so new layer gets included
        if "conn_saved" in side_payload:
            side = str(side_payload.get("side"))
            side_def = self.gui_properties.winding.connections_definition[side]

            conn_payloads = [self._definition_to_payload(conn_key, conn_def)
                for conn_key, conn_def in side_def.items()]

            side_payload["conn_wip"] = json.loads(json.dumps(conn_payloads))

            # Convert to WIP connection
            side_payload.pop("conn_saved")
            current_winding.setData(0, Qt.UserRole, side_payload)

        # Delete old valid details from connections definition
        self.gui_properties.winding.connections_definition.pop(str(side_payload.get("side")), None)

        # New layer also needs to be added to connections tree
        new_conn_layer = {"type": "Layer", "id": new_layer_id}
        connection_count = self.connections_tree_widget.topLevelItemCount()

        # No connections, layer is added on its own, a valid entry
        if connection_count == 0:
            self.connections_tree_widget.addTopLevelItem(self._connection_to_item(new_conn_layer))

        # One connection, assess how nested it is
        elif connection_count == 1:
            first_item = self.connections_tree_widget.topLevelItem(0)
            first_payload = first_item.data(0, Qt.UserRole)

            # Create Series connection between Layer1 and Layer2
            if first_payload.get("type") == "Layer":
                group_payload = {"type": "Series", "children": [first_payload, new_conn_layer]}
                group_item = self._connection_to_item(group_payload)
                self.connections_tree_widget.takeTopLevelItem(0)
                self.connections_tree_widget.addTopLevelItem(group_item)

            # Adds Layer inside existing single level deep connection
            elif first_payload.get("type") in ("Series", "Parallel"):
                children = first_payload["children"]
                all_layers = all(isinstance(child, dict) and child.get("type") == "Layer" for child in children)
                if all_layers:
                    children.append(new_conn_layer)
                    first_payload["children"] = children
                    first_item.setData(0, Qt.UserRole, first_payload)
                    first_item.setText(0, self._connection_to_label(first_payload))
                    first_item.addChild(self._connection_to_item(new_conn_layer))

                # More than one level deep, layer gets added to a new row
                else:
                    self.connections_tree_widget.addTopLevelItem(self._connection_to_item(new_conn_layer))
        else:
            self.connections_tree_widget.addTopLevelItem(self._connection_to_item(new_conn_layer))

        # Updates connections_def for the backend once a valid connection has been constructed
        if self.connections_tree_widget.topLevelItemCount() == 1:
            root_item = self.connections_tree_widget.topLevelItem(0)
            payload = root_item.data(0, Qt.UserRole)

            self._commit_connection_to_UserData(payload)

            #Push the payload (now with key added) back into the UI
            root_item.setData(0, Qt.UserRole, payload)
            root_item.setText(0, self._connection_to_label(payload))
            self.update_connections_def()
            self._display_connection_scheme()

    def _update_loads_definition(self):
        """Retrieve loads from ``UserRole`` and construct the side loads definition.
        Returns:
            list: A list of side loads for the backend.
        """
        loads = []

        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            winding = self.winding_tree_widget.topLevelItem(side_index)
            winding_data = winding.data(0, Qt.UserRole)
            loads.append(float(winding_data.get("side_load", 0.0)))

        return loads


    def selected_rows(self):
        """Get a list of selected rows from the connections tree.
        Returns:
            list: A list of selected rows.
        """
        selected_rows = []

        for row_index in range(self.connections_tree_widget.topLevelItemCount()):
            row = self.connections_tree_widget.topLevelItem(row_index)
            if row.isSelected():
                selected_rows.append(row)

        return selected_rows

    def _next_connection_key_index(self):
        """Find the next index for connection number"""

        existing_connections = [self.gui_properties.winding.connections_definition]
        current_max_index = 0

        while existing_connections:
            candidate_item = existing_connections.pop()

            # Search candidates and update max used index
            if isinstance(candidate_item, dict):
                for key, value in candidate_item.items():
                    if isinstance(key, str) and len(key) >= 2:
                        prefix = key[0]
                        suffix = key[1:]
                        if prefix in ("S", "P") and suffix.isdigit():
                            current_max_index = max(current_max_index, int(suffix))

                    # If item is nested add to end to check later
                    existing_connections.append(value)

        return current_max_index + 1

    def _commit_connection_to_UserData(self, payload):
        """Update UserData with valid connection"""

        # Get the next free index
        next_free_index = self._next_connection_key_index()

        # Iterate over the payload tree to convert UI connections to UserRole format
        connection_tree = [payload]

        while connection_tree:
            connection = connection_tree.pop()

            if not isinstance(connection, dict):
                continue

            if connection.get("type") in ("Series", "Parallel"):
                key = connection.get("key")

                # Reuse existing key
                if key:
                    number = key[1:]

                # No existing key so use next free one for S/P connection
                else:
                    number = str(next_free_index)
                    next_free_index += 1
                if connection["type"] == "Series":
                    connection["key"] = "S" + number
                else:
                    connection["key"] = "P" + number

            # Add nested connections to end
            children = connection.get("children")
            if isinstance(children, list):
                for child in children:
                    connection_tree.append(child)

        side_item = self.winding_tree_widget.currentItem()
        while side_item and side_item.parent():
            side_item = side_item.parent()

        side_payload = side_item.data(0, Qt.UserRole)
        side_payload["conn_saved"] = json.loads(json.dumps(payload))
        side_payload.pop("conn_wip", None)
        side_item.setData(0, Qt.UserRole, side_payload)

    def connect_connections(self, connection_type="Series"):
        """Apply a series or parallel connection.
        - Applying to multiple rows results in grouping them into a new series or parallel connection.
        - If applied to a single existing series or parallel connection, the type is toggled.
        - This method cannot be applied to a single layer.
        Args:
            connection_type (str, optional): The type of connection. Defaults to ``"Series"``.
        """
        selected = self.selected_rows()

        # Apply Series/Parallel connection to single row returns if a Layer is selected
        if len(selected) == 1:
            row = selected[0]
            row_data = row.data(0, Qt.UserRole)

            if row_data.get("type") in ("Series", "Parallel"):
                old_key = row_data.get("key")
                row_data["type"] = connection_type

                # Just toggle connection type S>P>S
                if old_key:
                    num = old_key[1:]
                    prefix = "S" if connection_type == "Series" else "P"
                    row_data["key"] = prefix + num

                row.setData(0, Qt.UserRole, row_data)
                row.setText(0, self._connection_to_label(row_data))

                if self.connections_tree_widget.topLevelItemCount() == 1:
                    root_item = self.connections_tree_widget.topLevelItem(0)
                    payload = root_item.data(0, Qt.UserRole)
                    self._commit_connection_to_UserData(payload)
                    root_item.setData(0, Qt.UserRole, payload)
                    root_item.setText(0, self._connection_to_label(payload))
                    self.update_connections_def()
            return

        child_data = [connection.data(0, Qt.UserRole) for connection in selected]

        # Reuse key if just one group is being toggled
        old_key = None

        if len(selected) == 1:
            row_data = selected[0].data(0, Qt.UserRole)
            row_type = row_data.get("type")

            if row_type in ("Series", "Parallel"):
                old_key = row_data.get("key")
        group_data = {"type": connection_type, "children": child_data}

        if old_key:
            num = old_key[1:]
            prefix = "S" if connection_type == "Series" else "P"
            group_data["key"] = prefix + num

        group_item = self._connection_to_item(group_data)

        first_index = self.connections_tree_widget.indexOfTopLevelItem(selected[0])
        self.connections_tree_widget.insertTopLevelItem(first_index, group_item)

        # Remove old rows in reverse order!
        for item in sorted(selected, key=self.connections_tree_widget.indexOfTopLevelItem, reverse=True):
            self.connections_tree_widget.takeTopLevelItem(self.connections_tree_widget.indexOfTopLevelItem(item))

        # And update connections def if we have a single row
        if self.connections_tree_widget.topLevelItemCount() == 1:
            root_item = self.connections_tree_widget.topLevelItem(0)
            payload = root_item.data(0, Qt.UserRole)
            self._commit_connection_to_UserData(payload)
            self.update_connections_def()

    def _disconnect(self):

        """Remove selected series or parallel connections by promoting their children."""
        selected = self.selected_rows()

        for row in selected:
            row_data = row.data(0, Qt.UserRole)

            # Only groups can be disconnected
            if row_data.get("type") not in ("Series", "Parallel"):
                continue

            # Need to insert Layers/nested groups at original group index
            parent_index = self.connections_tree_widget.indexOfTopLevelItem(row)

            # Remove parent row first
            self.connections_tree_widget.takeTopLevelItem(parent_index)

            # Promote children to top level
            insert_index = parent_index
            for child_payload in row_data.get("children", []):
                child_payload = dict(child_payload)
                child_payload.pop("key", None)

                child_item = self._connection_to_item(child_payload)
                self.connections_tree_widget.insertTopLevelItem(insert_index, child_item)
                insert_index += 1

        # Disconnect only creates WIP state and not a valid index so we stash instead updating connections
        self._stash_connections()

    def _definition_to_payload(self, key, value):
        """Recursively convert definition dictionaries into payloads for ``_connection_to_item``.
        Args:
            key (str): The key of the definition.
            value (str or dict): The value of the definition.
        Returns:
            dict: The payload dictionary.
        """
        if value == "Layer":
            return {"type": "Layer", "id": key}

        if isinstance(value, dict):
            conn_type = "Series" if key.startswith("S") else "Parallel"
            children = [self._definition_to_payload(k, v) for k, v in value.items()]
            return {"type": conn_type, "key": key, "children": children}

    def _connection_to_label(self, payload):
        """Get the UI display text for a given layer, series, or parallel dictionary.
        Args:
            payload (dict): The payload dictionary.
        Returns:
            str: The UI display text.
        """
        row_type = payload.get("type")

        # Creates Layer text for connections tree UI
        if row_type == "Layer":
            return "Layer " + str(payload.get("id", ""))

        # Creates Series/Parallel text for connections tree UI
        else:
            children = payload.get("children", [])
            child_labels = [self._connection_to_label(child) for child in children if isinstance(child, dict)]
            return row_type + "(" + ", ".join(child_labels) + ")"

    def _connection_to_item(self, payload):
        """Get a ``QTreeWidgetItem`` for a given layer, series, or parallel dictionary.
        Args:
            payload (dict): The payload dictionary.
        Returns:
            QTreeWidgetItem: The tree widget item.
        """
        item = QTreeWidgetItem([self._connection_to_label(payload)])
        item.setData(0, Qt.UserRole, dict(payload))

        # Recursively add children for groups
        for child in payload.get("children", []):
            child_item = self._connection_to_item(child)
            item.addChild(child_item)

        return item

    def update_connections_def(self, merge=True):
        """Populate the ``_connections_definition`` dictionary from UI entries via ``UserRole`` payloads.
        Only sides where ``conn_saved`` are exported. Sides with ``conn_wip`` are skipped.
        Args:
            merge (bool, optional): Whether to merge with existing definitions. Defaults to ``True``.
        """


        # Recursive function to help construct connection dict
        def export(payload):
            """Recursively convert payload into correct dict format for connections_definition."""
            connection_type = payload.get("type")

            if connection_type == "Layer":
                return {str(payload["id"]): "Layer"}

            if connection_type in ("Series", "Parallel"):
                connection_key = payload.get("key")



                # Recursive step to create valid dict entry
                children_dict = {}
                for child_payload in payload.get("children", []):
                    if not isinstance(child_payload, dict):
                        continue
                    if child_payload.get("type") not in ("Layer", "Series", "Parallel"):
                        continue

                    child_export = export(child_payload)
                    if not child_export:
                        continue

                    for child_key, child_value in child_export.items():
                        children_dict[child_key] = child_value

                return {connection_key: children_dict}
            return {}

        # Iterate over all sides
        new_conn_def = dict(self.gui_properties.winding.connections_definition) if merge else {}

        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            winding_item = self.winding_tree_widget.topLevelItem(side_index)
            side_key = winding_item.text(0).replace("Side", "").strip()
            side_payload = winding_item.data(0, Qt.UserRole) or {}

            # Remove previous connections that now relate to WIP sides
            if side_payload.get("conn_wip"):
                new_conn_def.pop(side_key, None)
                continue

            # Applies only to sides with valid saved connections
            saved_conn = side_payload.get("conn_saved")
            if not saved_conn:
                continue

            exported = export(saved_conn)
            if not exported:
                continue

            new_conn_def[side_key] = exported



        self.gui_properties.winding.connections_definition = new_conn_def

    def _display_connection_scheme(self):
        """Display the selected side's connection scheme in the connection tree.
        This method restores WIP rows if they are present in ``UserRole`` (``conn_wip``) and
        restores a single saved connection if it is present in ``UserRole`` (``conn_saved``).
        Otherwise, it rebuilds from the global ``_connections_definition``.
        """
        side_key = self.winding_label.text().replace("Side", "").strip()
        self.connections_tree_widget.clear()

        # Find the current top-level side item
        side_item = None
        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            winding = self.winding_tree_widget.topLevelItem(side_index)
            if winding.text(0).replace("Side", "").strip() == side_key:
                side_item = winding
                break
        if side_item is None:
            return

        side_payload = side_item.data(0, Qt.UserRole) or {}
        items = []

        # Restore WIP rows if they exist in stash
        if "conn_wip" in side_payload:
            items = [self._connection_to_item(p) for p in side_payload["conn_wip"]]

        # Restore single saved connection if in stash
        elif "conn_saved" in side_payload:
            items = [self._connection_to_item(side_payload["conn_saved"])]

        # Rebuild from definition
        else:
            group = self.gui_properties.winding.connections_definition.get(side_key, {})
            for key, value in group.items():
                payload = self._definition_to_payload(key, value)
                if payload:
                    items.append(self._connection_to_item(payload))

        # Add valid items
        for item in filter(None, items):
            self.connections_tree_widget.addTopLevelItem(item)

    def _update_layer_side_definition(self):
        """Extract the layer-to-side mapping from the winding tree's ``UserRole``.
        Returns:
            dict: The layer-to-side mapping.
        """
        if not self.gui_properties.winding.layer_side_definition:
            layer_side_definition = {}
        else:
            return  self.gui_properties.winding.layer_side_definition

        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            winding_item = self.winding_tree_widget.topLevelItem(side_index)
            winding_data = winding_item.data(0, Qt.UserRole)

            # Get side number from winding data
            side_num = str(winding_data.get("id", side_index + 1))

            layers = []
            for layer_index in range(winding_item.childCount()):
                layer_item = winding_item.child(layer_index)
                layer_data = layer_item.data(0, Qt.UserRole)

                if layer_data.get("type") == "Layer":
                    layers.append(str(layer_data.get("id")))

            layer_side_definition[side_num] = layers

        return layer_side_definition

    def _update_layers_definition(self):
        """Extract ``UserRole`` from the winding tree and write it in the format needed for ``layers_definition``.
        Returns:
            dict: The layers definition.
        """

        # Initialize layers definition as empty
        layers_def = {}

        # Iterate all windings and their child layers
        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            winding = self.winding_tree_widget.topLevelItem(side_index)

            for layer in range(winding.childCount()):
                child = winding.child(layer)
                data = child.data(0, Qt.UserRole)
                if data.get("type") != "Layer":
                    continue

                layer_id = str(data.get("id"))
                layer_key = "layer_" + layer_id

                turns = data.get("turns")
                insulation = data.get("insulation")
                cond = data.get("conductor")

                if self.cond_type.currentText() == "Circular":
                    layers_def[layer_key] = {
                        "conductor_diameter": cond.get("diameter"),
                        "segments_number": self._segments_number,
                        "insulation_thickness": insulation,
                        "turns_number": turns,
                    }

                else:
                    if self.build_combo.currentText() == "Wound":
                        layers_def[layer_key] = {
                            "conductor_width": cond.get("width"),
                            "conductor_height": cond.get("height"),
                            "insulation_thickness": insulation,
                            "turns_number": turns,
                        }
                    else:
                        layers_def[layer_key] = {
                            "conductor_width": cond.get("width"),
                            "conductor_height": cond.get("height"),
                            "turn_spacing": insulation,
                            "turns_number": turns,
                            "segments_number": self._segments_number,
                        }
        # self.gui_properties.winding.turn_spacing = insulation
        return layers_def

    def _stash_connections(self):
        """Save WIP rows or a single valid connection into the previous side's ``UserRole``.
        This method loads the new side's rows from ``UserRole`` (``conn_wip`` or ``conn_saved``).
        """
        if self._importing_connections:
            return

        # Stash previous sides text
        prev_side_text = self.winding_label.text()
        if prev_side_text:
            prev_key = prev_side_text.replace("Side", "")

            # Get previous top-level side item
            prev_item = None
            for side_index in range(self.winding_tree_widget.topLevelItemCount()):
                winding = self.winding_tree_widget.topLevelItem(side_index)
                if winding.text(0).replace("Side", "").strip() == prev_key:
                    prev_item = winding
                    break

            # Stash current connections_tree_widget into UserRole
            if prev_item is not None:
                connection_count = self.connections_tree_widget.topLevelItemCount()

                # Stops JSON being overwritten when connection tree is initially empty
                if connection_count != 0:
                    side_payload = prev_item.data(0, Qt.UserRole)

                    # Single valid connection so write to conn_saved and delete WIP
                    if connection_count == 1:
                        row_item = self.connections_tree_widget.topLevelItem(0)
                        side_payload["conn_saved"] = json.loads(json.dumps(row_item.data(0, Qt.UserRole)))
                        side_payload.pop("conn_wip", None)

                    else:
                        # Multiple rows so restore to previous WIP state
                        rows = []
                        for index in range(connection_count):
                            row_item = self.connections_tree_widget.topLevelItem(index)
                            rows.append(json.loads(json.dumps(row_item.data(0, Qt.UserRole))))
                        side_payload["conn_wip"] = rows
                        side_payload.pop("conn_saved", None)

                    prev_item.setData(0, Qt.UserRole, side_payload)

        # Switch to new side
        item = self.winding_tree_widget.currentItem()
        if item is None:
            return

        while item.parent():
            item = item.parent()
        top_level_name = item.text(0)

        if self.winding_label.text() != top_level_name:
            self.winding_label.setText(top_level_name)

        self._display_connection_scheme()

        # Only export when exactly one valid connection exists
        if self.connections_tree_widget.topLevelItemCount() == 1:
            self.update_connections_def()

    def example_button_clicked(self):
        """Handle the example button click event."""
        file_name_tuple = QFileDialog.getOpenFileName(
            caption="Open ETK file",
            dir=str(example_files),
            filter="ETK files (*.json)",
        )

        # Catch Cancel button being pressed (To stop manually added layers in UI being overwritten)
        if not file_name_tuple[0]:
            return

        file_name = Path(file_name_tuple[0])
        msg, is_valid = self.data_manager._import_data_from_json(file_name)
        self.ui.update_logger(msg)
        if is_valid:
            self._write_ui_data()
            self.example_name.setText(file_name.name)


    def _clear_connection_state(self):
        "Clears Connections tree UI, conn_saved and conn_wip form UI UserData"
        self.connections_tree_widget.clear()

        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            side_item = self.winding_tree_widget.topLevelItem(side_index)
            payload = side_item.data(0, Qt.UserRole)
            # Remove existing connection states if they exist
            payload.pop("conn_saved", None)
            payload.pop("conn_wip", None)
            side_item.setData(0, Qt.UserRole, payload)

    def _write_ui_data(self):
        """Programmatically update the UI from an imported JSON file.
        This method uses the methods and checks already in place for manual UI changes. It also
        resets the UI to its defaults for a new design."""

        # Save imported connections_definition for reuse and then clear connections in UI and UserRole
        imported_connections_def = dict(self.gui_properties.winding.connections_definition)
        self._clear_connection_state()
        self.gui_properties.winding.connections_definition = imported_connections_def

        self.ui.update_logger("UI data written from external source")

        # Populate UI for Bobbin/Board and Margin Group
        self.bobbin_board_thickness.setText(str(self.gui_properties.bobbin_board_and_margin.thickness))
        self.bobbin_checkbox.setChecked(self.gui_properties.settings.include_bobbin)
        self.top_margin.setText(str(self.gui_properties.bobbin_board_and_margin.top_margin))
        self.side_margin.setText(str(self.gui_properties.bobbin_board_and_margin.side_margin))

        # Populate UI for Electrical Group
        self.adaptive_frequency.setText(str(float(self.gui_properties.electrical.adaptive_frequency) / freq_scale["kHz"]))
        self.excitation_combo.setCurrentText(self.gui_properties.electrical.excitation_strategy)

        if self.excitation_combo.currentText() == "Voltage":
            self.excitation_combo.setItemData(0, "Voltage", Qt.UserRole)
            self.excitation_value.setText(str(self.gui_properties.electrical.voltage))
        else:
            self.excitation_combo.setItemData(1, "Current", Qt.UserRole)
            self.excitation_value.setText(str(self.gui_properties.electrical.current))

        # Populate UI for Winding Group
        self.build_combo.setCurrentText(self.gui_properties.winding.layer_type)
        self.cond_type.setCurrentText(self.gui_properties.winding.conductor_type)
        self.cond_material.setCurrentText(self.gui_properties.winding.conductor_material)
        self.layer_spacing.setText(str(self.gui_properties.winding.layer_spacing))

        # Winding Table
        self._populate_layers_from_definition(self.gui_properties.winding.layers_definition,
                                              self.gui_properties.winding.layer_side_definition,
                                              self.gui_properties.winding.side_loads)

        # Connections Table populated and displayed
        self._populate_connections_from_definition(self.gui_properties.winding.connections_definition)
        self._display_connection_scheme()

        # Add first winding to tree for a new design
        if not self.gui_properties.winding.layers_definition:
            self._add_winding()

        # Select first layer in first side to refresh connections
        self.winding_tree_widget.setCurrentItem(self.winding_tree_widget.topLevelItem(0).child(0))

        # Settings
        self.draw_skin_layers.setChecked(self.gui_properties.settings.draw_skin_layers)
        self.full_model.setChecked(self.gui_properties.settings.full_model)

        # 'Skip Check Windings' is in UI only, JSON does not store this.
        self.number_passes.setText(str(self.gui_properties.settings.number_passes))
        self.percentage_error.setText(str(self.gui_properties.settings.percentage_error))
        self.segmentation_angle.setText(str(self.gui_properties.settings.segmentation_angle))
        self.offset.setText(str(self.gui_properties.settings.offset))
        self._update_frequency_sweep(dict(self.gui_properties.settings.frequency_sweep_definition))


        # Populate UI for Core Group
        self.material_combo.setCurrentText(self.gui_properties.core.material)
        self._update_airgap_type(airgap=self.gui_properties.core.airgap)

        core_def = {"supplier" : self.gui_properties.core.supplier,
                    "type" : self.gui_properties.core.type,
                    "model" : self.gui_properties.core.model,
                    "dimensions": self.gui_properties.core.dimensions}
        self.supplier_combo.setCurrentText(core_def["supplier"])
        self.type_combo.setCurrentText(core_def["type"])
        self.model_combo.setCurrentText(core_def["model"])

        # # # Handle case where core has custom dimensions
        self.gui_properties.core.supplier = core_def["supplier"]
        self.gui_properties.core.type = core_def["type"]
        self.gui_properties.core.model = core_def["model"]
        self._update_core_dimensions(core_data=core_def) # check custom core

    def _update_frequency_sweep(self, freq_sweep=None):
        """Manage frequency sweep population and formatting upon UI and JSON import.

        Args:
            freq_sweep (dict, optional): The frequency sweep definition. Defaults to ``None``.
        """
        frequency_widgets = (
            self.start_frequency, self.stop_frequency, self.samples,
            self.start_frequency_unit, self.stop_frequency_unit, self.scale)

        # Populate UI with imported JSON (Two possible frequency sweep formats)
        if isinstance(freq_sweep, dict):
            enabled = freq_sweep.get("frequency_sweep", False)
            self.frequency_sweep.setChecked(enabled)

            for widget in frequency_widgets:
                widget.setEnabled(enabled)

            self.start_frequency.setText(str(freq_sweep.get("start_frequency", self.gui_properties.settings.frequency_sweep_definition.start_frequency)))
            self.start_frequency_unit.setCurrentText(freq_sweep.get("start_frequency_unit", self.gui_properties.settings.frequency_sweep_definition.start_frequency_unit))
            self.stop_frequency.setText(str(freq_sweep.get("stop_frequency", self.gui_properties.settings.frequency_sweep_definition.stop_frequency)))
            self.stop_frequency_unit.setCurrentText(freq_sweep.get("stop_frequency_unit", self.gui_properties.settings.frequency_sweep_definition.stop_frequency_unit))
            self.samples.setText(str(freq_sweep.get("samples", self.gui_properties.settings.frequency_sweep_definition.samples)))
            self.scale.setCurrentText(freq_sweep.get("scale", self.gui_properties.settings.frequency_sweep_definition.scale))

        # Use tick box bool value from UI to set visibility
        enabled = self.frequency_sweep.isChecked()
        for widget in frequency_widgets:
            widget.setEnabled(enabled)

        # Construct and return frequency sweep definition when we have no sweep
        if not enabled:
            self.gui_properties.settings.frequency_sweep_definition = {"frequency_sweep":False}
            return self.gui_properties.settings.frequency_sweep_definition

        # Red format of frequency fields to display incorrect entries
        def convert_to_hz(edit, unit):
            try:
                return float(edit.text()) * freq_scale[unit.currentText()]
            except ValueError:
                return None

        start_freq = convert_to_hz(self.start_frequency, self.start_frequency_unit)
        stop_freq = convert_to_hz(self.stop_frequency, self.stop_frequency_unit)
        invalid = (
                start_freq is not None
                and stop_freq is not None
                and start_freq >= stop_freq
        )

        for widget in (self.start_frequency, self.stop_frequency):
            self._set_invalid(widget, invalid, "Start frequency must be less than Stop frequency." if invalid else "")

            # Construct and return frequency sweep
        self.gui_properties.settings.frequency_sweep_definition = {
            "frequency_sweep": True,
            "start_frequency": float(self.start_frequency.text()),
            "start_frequency_unit": self.start_frequency_unit.currentText(),
            "stop_frequency": float(self.stop_frequency.text()),
            "stop_frequency_unit": self.stop_frequency_unit.currentText(),
            "samples": int(self.samples.text()),
            "scale": self.scale.currentText(),
        }
        return self.gui_properties.settings.frequency_sweep_definition

    def _populate_layers_from_definition(self, layers_def, layer_side_def, side_loads=None):
        """Populate the winding tree from JSON definitions.
        Args:
            layers_def (dict): A dictionary with ``layer_X`` entries.
            layer_side_def (dict): A dictionary mapping a side to a list of layer IDs.
            side_loads (list, optional): A list of load values, one per side. Defaults to ``None``.
        """
        self.winding_tree_widget.clear()
        self.winding_tree_widget.blockSignals(True)

        # Build a side load mapping that follows the JSON key order
        side_keys = list(layer_side_def.keys())
        side_load_map = {}
        if side_loads and len(side_loads) >= len(side_keys):
            for i, side in enumerate(side_keys):
                side_load_map[side] = side_loads[i]

        # Build windings in order, this may be different to JSON
        for side in sorted(layer_side_def.keys(), key=lambda x: int(x)):
            layer_ids = layer_side_def[side]
            load = side_load_map.get(side, self._default_side_load)

            winding_item = QTreeWidgetItem(["Side" + str(side), "", "", "", str(load)])
            winding_item.setFlags(winding_item.flags() | Qt.ItemIsEditable)
            winding_item.setData(
                0,
                Qt.UserRole,
                {
                    "type": "Winding",
                    "side": int(side),
                    "side_load": float(load),
                },
            )

            # Add layers to each winding
            for layer_id in layer_ids:
                layer_key = "layer_" + str(layer_id)
                layer_def = layers_def.get(layer_key, {})

                turns = layer_def.get("turns_number", self._turn_number)

                if "conductor_diameter" in layer_def:
                    conductor_display = str(layer_def["conductor_diameter"])
                    conductor = {"diameter": layer_def["conductor_diameter"]}
                    insulation = layer_def.get("insulation_thickness", self._insulation_thickness)
                else:
                    w = layer_def.get("conductor_width", self._conductor_width)
                    h = layer_def.get("conductor_height", self._conductor_height)
                    conductor_display = str(w) + " x " + str(h)
                    conductor = {"width": w, "height": h}
                    insulation = layer_def.get("turn_spacing", self._insulation_thickness)

                layer_item = QTreeWidgetItem(
                    [
                        "Layer " + str(layer_id),
                        str(turns),
                        conductor_display,
                        str(insulation),
                        "",
                    ]
                )
                layer_item.setFlags(layer_item.flags() | Qt.ItemIsEditable)
                layer_item.setData(
                    0,
                    Qt.UserRole,
                    {
                        "type": "Layer",
                        "id": layer_id,
                        "turns": turns,
                        "insulation": insulation,
                        "conductor": conductor,
                    },
                )

                winding_item.addChild(layer_item)

            self.winding_tree_widget.addTopLevelItem(winding_item)

        self.winding_tree_widget.expandAll()
        self.winding_tree_widget.blockSignals(False)

    def _populate_connections_from_definition(self, connections_def):
        """Store the JSON connections definition and show only the first side.
        Args:
            connections_def (dict): The connections definition.
        """

        self._importing_connections = True

        self.gui_properties.winding.connections_definition = {
            str(side_key): side_connection for side_key, side_connection in connections_def.items()
        }
        self.connections_tree_widget.clear()

        if not self.gui_properties.winding.connections_definition:
            self._importing_connections = False
            return

        # Populate UI with connections
        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            side_item = self.winding_tree_widget.topLevelItem(side_index)
            side_key = side_item.text(0).replace("Side", "").strip()

            conn_def = self.gui_properties.winding.connections_definition.get(side_key)

            # Handle sides with just one layer and no connections
            if not conn_def:
                continue

            # connections_definition always has exactly one Layer,Series or Parallel per Side
            key, value = next(iter(conn_def.items()))
            payload = self._definition_to_payload(key, value)

            side_payload = side_item.data(0, Qt.UserRole)
            side_payload["conn_saved"] = payload
            side_payload.pop("conn_wip", None)
            side_item.setData(0, Qt.UserRole, side_payload)

        # Pick the first side so it can be selected and connections tree updated
        first_side = next(iter(self.gui_properties.winding.connections_definition))
        for side_index in range(self.winding_tree_widget.topLevelItemCount()):
            side_item = self.winding_tree_widget.topLevelItem(side_index)
            if side_item.text(0).replace("Side", "") == first_side:
                self.winding_tree_widget.setCurrentItem(side_item)
                break

        self._importing_connections = False

    def _read_ui_data(self):
        """Read from the UI selection and write to internal variables."""
        self.ui.update_logger("Data from UI read and stored in GUI data model")

        self.gui_properties.core.supplier = self.supplier_combo.currentText()
        self.gui_properties.core.type = self.type_combo.currentText()
        self.gui_properties.core.model = self.model_combo.currentText()
        self.gui_properties.core.dimensions = {
            "D_1": self.D_1.text(),
            "D_2": self.D_2.text(),
            "D_3": self.D_3.text(),
            "D_4": self.D_4.text(),
            "D_5": self.D_5.text(),
            "D_6": self.D_6.text(),
            "D_7": self.D_7.text(),
            "D_8": self.D_8.text()
        }
        self.gui_properties.core.material = self.material_combo.currentText()
        self.gui_properties.core.airgap.location = self.airgap_combo.currentText()
        self.gui_properties.core.airgap.height = float(self.airgap_value.text())

        self.gui_properties.winding.layer_type = self.build_combo.currentText()
        self.gui_properties.winding.layers_definition = self._update_layers_definition()
        self._number_of_layers = len(self.gui_properties.winding.layers_definition)
        self.gui_properties.winding.layer_spacing = self.layer_spacing.text()
        self.gui_properties.settings.draw_skin_layers = self.draw_skin_layers.isChecked()
        self.gui_properties.winding.conductor_type= self.cond_type.currentText()
        self.gui_properties.winding.conductor_material = self.cond_material.currentText()

        self.gui_properties.settings.include_bobbin = self.bobbin_checkbox.isChecked()
        self.gui_properties.bobbin_board_and_margin.thickness = float(self.bobbin_board_thickness.text())
        self.gui_properties.bobbin_board_and_margin.top_margin = float(self.top_margin.text())
        self.gui_properties.bobbin_board_and_margin.side_margin = float(self.side_margin.text())

        self.gui_properties.electrical.adaptive_frequency = float(self.adaptive_frequency.text())
        self.gui_properties.electrical.excitation_strategy = self.excitation_combo.currentText()
        self.gui_properties.electrical.excitation_value = float(self.excitation_value.text())
        self.gui_properties.settings.percentage_error = float(self.percentage_error.text())
        self.gui_properties.settings.number_passes = int(self.number_passes.text())
        self._transformer_sides = self.winding_tree_widget.topLevelItemCount()
        self.gui_properties.winding.side_loads = self._update_loads_definition()
        self.gui_properties.settings.offset = float(self.offset.text())
        self.gui_properties.settings.full_model = self.full_model.isChecked()
        self.gui_properties.settings.project_path = "C:/Files/"

        self.gui_properties.settings.frequency_sweep_definition = self._update_frequency_sweep()
        self.gui_properties.winding.layer_side_definition = self._update_layer_side_definition()
        self.gui_properties.settings.segmentation_angle = self.segmentation_angle.text()

    def save_button_clicked(self):
        """Save the UI state to a JSON file."""
        file_name_tuple = QFileDialog.getSaveFileName(
            caption="Save ETK file", dir=str(example_files), filter="ETK files (*.json)"
        )
        file_name = Path(file_name_tuple[0])

        # handle the event where the user cancels the option to save
        if file_name != Path("."):
            self._save_model(file=file_name)
        else:
            self.ui.update_logger("Save As operation cancelled by user")

    def _save_model(self, file):
        """Save the etk model to a JSON file.
        Args:
            file (pathlib.Path): The path to the JSON file.
        """

        file = Path(file)
        self._read_ui_data()
        self.data_manager._update_frontend_properties()
        etk_model = self.data_manager.create_backend_data()
        with file.open(mode="w") as f:
            json.dump(etk_model, f, indent=2)
