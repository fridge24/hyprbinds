import os
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QRadioButton, QHBoxLayout,
    QFileDialog, QCheckBox, QMessageBox
)

class HyprbindsSetup(QDialog):
    CONFIG_DIR = os.path.expanduser("~/.config/hyprbinds")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "keybinds_config.json")
    HYPRLAND_CONFIG = os.path.expanduser("~/.config/hypr/hyprland.conf")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.keybinds_path = ""
        self.init_ui()
        self.setMinimumSize(450, 200)
        self.setMaximumSize(450, 200)
    def init_ui(self):
        self.setWindowTitle("First-Time Setup: Keybinds Configuration")
        layout = QVBoxLayout()

        # Welcome text
        layout.addWidget(QLabel("Welcome! Please set up your keybinds configuration file."))

        # Radio buttons for selection
        self.radio_existing = QRadioButton("Use an existing keybinds.conf file")
        self.radio_new = QRadioButton("Create a new keybinds.conf file")
        layout.addWidget(self.radio_existing)
        layout.addWidget(self.radio_new)

        # File selection button
        self.btn_select_file = QPushButton("Select File")
        self.btn_select_file.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select_file)

        # Checkbox for extracting from hyprland.conf
        self.chk_extract = QCheckBox("Extract keybinds from hyprland.conf")
        layout.addWidget(self.chk_extract)

        # Confirm and Cancel buttons
        button_layout = QHBoxLayout()
        self.btn_confirm = QPushButton("Confirm Setup")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_confirm.clicked.connect(self.confirm_selection)
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_confirm)
        button_layout.addWidget(self.btn_cancel)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def select_file(self):
        if self.radio_existing.isChecked():
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Keybinds File", "", "Config Files (*.conf)")
        elif self.radio_new.isChecked():
            dir_path = QFileDialog.getExistingDirectory(self, "Select Directory for New File")
            file_path = os.path.join(dir_path, "keybinds.conf") if dir_path else ""
        else:
            QMessageBox.warning(self, "Selection Required", "Please choose an option first.")
            return
        
        if file_path:
            self.keybinds_path = file_path
            QMessageBox.information(self, "Selection Saved", f"Selected: {file_path}")

    def confirm_selection(self):
        if not self.keybinds_path:
            QMessageBox.critical(self, "Error", "No file selected. Please choose a valid option.")
            return
        
        # Create new file if chosen
        if self.radio_new.isChecked() and not os.path.exists(self.keybinds_path):
            with open(self.keybinds_path, "w") as f:
                f.write("# Custom Hyprland keybinds file\n")
                if self.chk_extract.isChecked() and os.path.exists(self.HYPRLAND_CONFIG):
                    self.extract_keybinds(self.HYPRLAND_CONFIG, self.keybinds_path)

        # Ensure the config directory exists
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        
        # Save to config file in ~/.config/hyprbinds/
        with open(self.CONFIG_FILE, "w") as config:
            json.dump({"keybinds_path": self.keybinds_path}, config)
        
        QMessageBox.information(self, "Success", "Configuration saved successfully.")
        self.accept()

    def extract_keybinds(self, source_file, destination_file):
        try:
            with open(source_file, "r") as source:
                keybinds = [line for line in source if line.strip().startswith(("bind", "unbind", "bindm"))]
            if keybinds:
                with open(destination_file, "a") as dest:
                    dest.writelines(keybinds)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract keybinds: {e}")
