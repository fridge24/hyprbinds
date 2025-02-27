from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QPushButton, QSizePolicy, QMessageBox, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QPalette
from keyboards import KeyboardFactory
from keybind_manager import KeybindManager
from keybind_editor import show_keybinds  # Import the popup logic

class KeybindManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manage Keybinds")
        self.keybind_manager = KeybindManager()
        self.setMinimumSize(900, 500)

        self.selected_keyboard_layout = "qwerty_full"  # Load dynamically if needed
        self.load_keyboard()
        self.initUI()

    def load_keyboard(self):
        """Loads the keyboard layout from the factory."""
        self.keyboard = KeyboardFactory.get_keyboard(self.selected_keyboard_layout)

    def initUI(self):
        """Initializes the GUI layout and components."""
        main_layout = QVBoxLayout()
        
        # Legend and Close Button
        legend_layout = QHBoxLayout()
        palette = self.palette()
        default_button_color = palette.color(QPalette.ColorRole.Button).name()
        highlight_color = palette.color(QPalette.ColorRole.Highlight).name()
        unsupported_color = palette.color(QPalette.ColorRole.Mid).name()  # Third color

        # Use addLayout instead of addWidget
        legend_layout.addLayout(self.create_color_legend("Occupied Keybinds", highlight_color))
        legend_layout.addLayout(self.create_color_legend("Unoccupied Keys", default_button_color))
        legend_layout.addLayout(self.create_color_legend("Unsupported Keys", unsupported_color))
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)  # Close the dialog on click
        legend_layout.addWidget(close_button)
        
        main_layout.addLayout(legend_layout)

        # Keyboard Layout
        self.keyboard_layout = QGridLayout()
        self.keyboard_layout.setSpacing(5)
        self.populate_keyboard()
        main_layout.addLayout(self.keyboard_layout)
        
        self.setLayout(main_layout)

    def create_color_legend(self, label_text, color):
        """Creates a color legend item with label."""
        legend_item = QHBoxLayout()
        color_box = QLabel()
        color_box.setFixedSize(20, 20)
        color_box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
        label = QLabel(label_text)
        legend_item.addWidget(color_box)
        legend_item.addWidget(label)
        return legend_item

    def populate_keyboard(self):
        """Creates the keyboard layout UI and colors the keys based on assigned binds."""
        palette = self.palette()
        default_button_color = palette.color(QPalette.ColorRole.Button).name()
        highlight_color = palette.color(QPalette.ColorRole.Highlight).name()
        unsupported_color = palette.color(QPalette.ColorRole.Mid).name()
        occupied = {}

        for (row, col), key in self.keyboard.get_keys().items():
            key_size = int(self.keyboard.get_key_size(key))

            while (row, col) in occupied:
                col += 1

            for offset in range(key_size):
                occupied[(row, col + offset)] = True

            key_button = QPushButton(key)
            key_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            key_button.setMinimumSize(40 * key_size, 40)

            if self.keybind_manager.get_keybinds_for_key(key):
                key_button.setStyleSheet(f"background-color: {highlight_color};")
            #elif key in self.keyboard.get_unsupported_keys():  # Assume method exists
            #   key_button.setStyleSheet(f"background-color: {unsupported_color};")
            else:
                key_button.setStyleSheet(f"background-color: {default_button_color};")

            key_button.clicked.connect(lambda checked, k=key: show_keybinds(self, k, self.keybind_manager))
            self.keyboard_layout.addWidget(key_button, row, col, 1, key_size)
