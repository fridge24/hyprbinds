from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtCore import Qt
from keybind_manager import KeybindManager
from add_keybind_form import AddKeybindForm
from remove_keybind_form import RemoveKeybindForm
from keyboard_display import KeyboardDisplay
import sys

# Modifier options
MODIFIERS = ["SUPER", "CTRL", "ALT", "None"]
SECONDARY_MODIFIERS = ["None", "SHIFT", "ALT"]
KEYS = [chr(k) for k in range(65, 91)] + [str(n) for n in range(10)]  # A-Z, 0-9
COMMANDS = ["movewindow", "exit", "fullscreen", "exec", "togglefloating"]

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
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumWidth(900)
        self.setMinimumHeight(350)

        self.keybind_manager = KeybindManager()
        self.initUI()

    def initUI(self):
        """Creates the main UI layout."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # ASCII Header
        header_label = QLabel(ASCII_HEADER)
        header_label.setFont(QFont("Courier", 10))  # Monospace font
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setWordWrap(True)

        # Get current background color from the platform theme
        palette = self.palette()
        bg_color = palette.color(QPalette.ColorRole.Window).name()

        # Set the background color of the header to match the platform's theme
        header_label.setStyleSheet(f"background-color: {bg_color}; padding: 10px;")

        main_layout.addWidget(header_label)

        # Add Keybind Button
        add_btn = QPushButton("Add Keybind")
        add_btn.clicked.connect(self.show_add_keybind_form)
        main_layout.addWidget(add_btn)

        # Remove Keybind Button
        remove_btn = QPushButton("Remove Keybind")
        remove_btn.clicked.connect(self.show_remove_keybind_form)
        main_layout.addWidget(remove_btn)
        
        # View Existing Keybinds Button
        view_btn = QPushButton("View Existing Keybinds")
        view_btn.clicked.connect(self.show_keyboard_display)
        main_layout.addWidget(view_btn)

        # Button Layout
        button_layout = QHBoxLayout()

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        # Apply Button
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_keybind_changes)
        button_layout.addWidget(apply_btn)

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

    def show_add_keybind_form(self):
        """Opens the form in a new dialog to add a new keybind."""
        self.add_keybind_form = AddKeybindForm(self)
        self.add_keybind_form.exec()  # Show the dialog

    def show_keyboard_display(self):
        """Opens the keyboard display window."""
        self.keyboard_display = KeyboardDisplay(self)
        self.keyboard_display.show()

    def show_remove_keybind_form(self):
        """Opens the form in a new dialog to remove a keybind."""
        self.remove_keybind_form = RemoveKeybindForm(self)
        self.remove_keybind_form.exec()  # Show the dialog

    def apply_keybind_changes(self):
        """Applies the keybind changes."""
        self.keybind_manager.save_keybinds_to_file()
        QMessageBox.information(self, "Success", "Keybind changes applied successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HyprBindsApp()
    window.show()
    sys.exit(app.exec())
