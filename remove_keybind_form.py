from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QLineEdit, QHBoxLayout
)
from keybind_manager import KeybindManager

class RemoveKeybindForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Keybind")
        self.setGeometry(200, 200, 400, 250)
        self.keybind_manager = KeybindManager()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Enter key to filter or select a keybind to remove:")
        layout.addWidget(self.label)

        # Input field for filtering
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter a key (e.g., A, B, 1, 2)")
        self.key_input.textChanged.connect(self.filter_keybinds)
        layout.addWidget(self.key_input)

        # Dropdown for keybind selection
        self.keybind_dropdown = QComboBox()
        self.populate_keybinds()
        layout.addWidget(self.keybind_dropdown)

        # Button layout
        button_layout = QHBoxLayout()

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        # Remove button
        self.remove_button = QPushButton("Remove Keybind")
        self.remove_button.clicked.connect(self.remove_keybind)
        button_layout.addWidget(self.remove_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def populate_keybinds(self, key_filter=None):
        """Populates the dropdown with existing keybinds, optionally filtering by key."""
        self.keybind_dropdown.clear()
        keybinds = self.keybind_manager.get_keybinds()
        
        for bind in keybinds:
            key = bind["key"].upper()
            if key_filter and key_filter.upper() not in key:
                continue
            
            mod = bind["modifiers"]
            sec_mod = bind["secondary_modifier"]
            command = bind["command"]
            argument = bind["argument"]
            display_text = (
                f"{mod} + {sec_mod} + {key} -> {command} {argument}" if sec_mod != "None" 
                else f"{mod} + {key} -> {command} {argument}"
            )
            self.keybind_dropdown.addItem(display_text, bind)

    def filter_keybinds(self):
        """Filters keybinds based on user input."""
        key_filter = self.key_input.text().strip()
        self.populate_keybinds(key_filter)

    def remove_keybind(self):
        """Removes the selected keybind from the JSON file and updates the dropdown."""
        index = self.keybind_dropdown.currentIndex()
        if index == -1:
            QMessageBox.warning(self, "Warning", "No keybind selected.")
            return

        keybind_to_remove = self.keybind_dropdown.currentData()
        
        if keybind_to_remove:
            self.keybind_manager.remove_keybind(
                keybind_to_remove["modifiers"], 
                keybind_to_remove["secondary_modifier"], 
                keybind_to_remove["key"]
            )
            
            QMessageBox.information(self, "Success", "Keybind removed successfully.")
            self.filter_keybinds()
        else:
            QMessageBox.warning(self, "Warning", "Invalid keybind selected.")
