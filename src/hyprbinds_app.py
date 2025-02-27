from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtCore import Qt
import json
import os
from keybind_manager import KeybindManager
from keybind_manager_dialog import KeybindManagerDialog
from keyboard_selector import KeyboardFactory
import keyboard_selector
from hyprbinds_setup import HyprbindsSetup  # Import the HyprbindsSetup QDialog

CONFIG_FILE = os.path.expanduser("~/.config/hyprbinds/keybinds_config.json")

ASCII_HEADER = """
       ▄█    █▄    ▄██   ▄      ▄███████▄    ▄████████ ▀█████████▄   ▄█  ███▄▄▄▄   ████████▄     ▄████████     
      ███    ███   ███   ██▄   ███    ███   ███    ███   ███    ███ ███  ███▀▀▀██▄ ███   ▀███   ███    ███     
      ███    ███   ███▄▄▄███   ███    ███   ███    ███   ███    ███ ███▌ ███   ███ ███    ███   ███    █▀  
▄███▄▄▄▄███▄▄ ▀▀▀▀▀▀███   ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄██▀  ███▌ ███   ███ ███    ███   ███        
      ▀▀███▀▀▀▀███▀  ▄██   ███ ▀█████████▀  ▀▀███▀▀▀▀▀   ▀▀███▀▀▀██▄  ███▌ ███   ███ ███    ███ ▀███████████     
        ███    ███   ███   ███   ███        ▀███████████   ███    ██▄ ███  ███   ███ ███    ███          ███     
        ███    ███   ███   ███   ███          ███    ███   ███    ███ ███  ███   ███ ███   ▄███    ▄█    ███     
       ███    █▀     ▀█████▀   ▄████▀        ███    ███ ▄█████████▀  █▀    ▀█   █▀  ████████▀   ▄████████▀                      
"""

class HyprBindsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyprBinds")
        self.setMinimumSize(900, 350)
        self.setMaximumSize(900, 350)
        self.keybind_manager = KeybindManager()
        self.initUI()

    def initUI(self):
        """Creates the main UI layout."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # ASCII Header
        header_label = QLabel(ASCII_HEADER)
        header_label.setFont(QFont("Courier", 10))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setWordWrap(True)
        palette = self.palette()
        bg_color = palette.color(QPalette.ColorRole.Window).name()
        header_label.setStyleSheet(f"background-color: {bg_color}; padding: 10px;")
        main_layout.addWidget(header_label)

        # Load current layout
        self.current_layout = keyboard_selector.load_selected_keyboard()
        print(f"current layout: {self.current_layout}")

        # Display current keyboard layout
        self.current_layout_label = QLabel(f"Current Keyboard Layout: {self.current_layout}")
        self.current_layout_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        main_layout.addWidget(self.current_layout_label)

        # Keyboard Layout Dropdown with Placeholder
        self.keyboard_combo = QComboBox()
        self.keyboard_combo.addItem("Select Keyboard Layout")  # Placeholder item
        self.keyboard_combo.addItems(["qwerty_full", "qwerty_reduced", "azerty", "dvorak", "colemak"])
        self.keyboard_combo.setCurrentText(self.current_layout if self.current_layout in self.keyboard_combo.itemText(1) else "Select Keyboard Layout")
        self.keyboard_combo.setEditable(False)  # Prevent typing
        self.keyboard_combo.model().item(0).setEnabled(False)  # Disable the placeholder
        self.keyboard_combo.currentTextChanged.connect(self.save_keyboard_layout)
        main_layout.addWidget(self.keyboard_combo)

        # Edit Keybinds Button
        edit_btn = QPushButton("Edit Keybinds")
        edit_btn.clicked.connect(self.show_keybind_manager_dialog)
        main_layout.addWidget(edit_btn)

        # Open Setup Dialog Button
        setup_btn = QPushButton("Open HyprBinds Setup")
        setup_btn.clicked.connect(self.open_setup_dialog)
        main_layout.addWidget(setup_btn)

        # Buttons Layout
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Keybinds")
        apply_btn.clicked.connect(self.apply_keybind_changes)
        button_layout.addWidget(apply_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

    def save_keyboard_layout(self, layout_name):
        keyboard_selector.save_selected_keyboard(layout_name)
        self.current_layout_label.setText(f"Current Keyboard Layout: {layout_name}")
        QMessageBox.information(self, "Keyboard Layout Saved", f"Selected layout: {layout_name}")
    
    def show_keybind_manager_dialog(self):
        dialog = KeybindManagerDialog(self)
        dialog.exec()
    
    def apply_keybind_changes(self):
        self.keybind_manager.save_keybinds_to_file()
        QMessageBox.information(self, "Success", "Keybind changes applied successfully.")
    
    def open_setup_dialog(self):
        setup_dialog = HyprbindsSetup(self)
        setup_dialog.exec()
