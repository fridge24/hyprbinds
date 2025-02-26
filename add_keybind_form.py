from PyQt6.QtWidgets import (
    QDialog, QComboBox, QLineEdit, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt
from keybind_manager import KeybindManager

MODIFIERS = ["SUPER", "CTRL", "ALT", "None"]
SECONDARY_MODIFIERS = ["None", "SHIFT", "ALT"]
KEYS = [chr(k) for k in range(65, 91)] + [str(n) for n in range(10)]  # A-Z, 0-9
COMMANDS = ["movewindow", "exit", "fullscreen", "exec", "togglefloating"]

class AddKeybindForm(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add Keybind")
        self.setFixedSize(800, 200)

        self.parent = parent
        self.keybind_manager = KeybindManager()

        # Create form elements
        self.mod_dropdown = QComboBox()
        self.mod_dropdown.addItems(MODIFIERS)

        self.sec_mod_dropdown = QComboBox()
        self.sec_mod_dropdown.addItems(SECONDARY_MODIFIERS)

        self.key_dropdown = QComboBox()
        self.key_dropdown.addItems(KEYS)

        self.command_dropdown = QComboBox()
        self.command_dropdown.addItems(COMMANDS + ["Custom"])

        self.argument_field = QLineEdit()

        # Error label (initially hidden)
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setVisible(False)  # Hide initially

        # Layout setup
        fields_layout = QHBoxLayout()

        # Labels for the fields
        labels = [
            ("Activator Key:", self.mod_dropdown),
            ("Optional Modifier:", self.sec_mod_dropdown),
            ("Letter/Number:", self.key_dropdown),
            ("Preset Command:", self.command_dropdown),
            ("Custom Command:", self.argument_field),
        ]

        for text, widget in labels:
            layout = QVBoxLayout()
            label = QLabel(text)
            layout.addWidget(label)
            layout.addWidget(widget)
            fields_layout.addLayout(layout)

        # Button Box
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.on_confirm)
        self.button_box.rejected.connect(self.reject)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.error_label)  # Error message at the top
        main_layout.addLayout(fields_layout)  # Form fields
        main_layout.addWidget(self.button_box, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # Command selection logic
        self.command_dropdown.currentTextChanged.connect(self.toggle_argument_visibility)

    def toggle_argument_visibility(self):
        """Show/hide the argument field based on the selected command."""
        self.argument_field.setVisible(self.command_dropdown.currentText() in ["exec", "Custom"])

    def on_confirm(self):
        """Handle form submission."""
        modifiers = self.mod_dropdown.currentText()
        sec_mod = self.sec_mod_dropdown.currentText()
        key = self.key_dropdown.currentText().upper()
        command = self.command_dropdown.currentText()
        argument = self.argument_field.text()

        try:
            if self.keybind_manager.is_keybind_taken(modifiers, sec_mod, key):
                self.error_label.setText("This keybind is already taken!")
                self.error_label.setVisible(True)
                return

            error_message = self.keybind_manager.add_keybind(modifiers, sec_mod, key, command, argument)

            if error_message:
                self.error_label.setText(error_message)
                self.error_label.setVisible(True)
            else:
                self.error_label.setVisible(False)  # Hide error if no issue
                self.accept()  # Close form
        except Exception as e:
            print("Exception occurred:", str(e))  # Debugging
            self.error_label.setText("An unexpected error occurred.")
            self.error_label.setVisible(True)
