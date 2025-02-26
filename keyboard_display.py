from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QDialog, QSizePolicy
from PyQt6.QtCore import Qt
from keybind_manager import KeybindManager  # Import KeybindManager directly

class KeyboardDisplay(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Keybind Viewer")
        self.setGeometry(200, 200, 800, 300)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)  # Floating window
        self.keybind_manager = KeybindManager()  # Instantiate KeybindManager here
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Click a key to see bound commands:")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        keyboard_layout = QGridLayout()
        keyboard_layout.setSpacing(5)

        key_positions = {
            "Esc": (0, 0), "F1": (0, 1), "F2": (0, 2), "F3": (0, 3), "F4": (0, 4), "F5": (0, 5),
            "F6": (0, 6), "F7": (0, 7), "F8": (0, 8), "F9": (0, 9), "F10": (0, 10), "F11": (0, 11), "F12": (0, 12),
            "`": (1, 0), "1": (1, 1), "2": (1, 2), "3": (1, 3), "4": (1, 4), "5": (1, 5), "6": (1, 6),
            "7": (1, 7), "8": (1, 8), "9": (1, 9), "0": (1, 10), "-": (1, 11), "=": (1, 12), "Backspace": (1, 13, 2),
            "Tab": (2, 0, 1.5), "Q": (2, 1), "W": (2, 2), "E": (2, 3), "R": (2, 4), "T": (2, 5), "Y": (2, 6),
            "U": (2, 7), "I": (2, 8), "O": (2, 9), "P": (2, 10), "[": (2, 11), "]": (2, 12), "\\": (2, 13),
            "CapsLock": (3, 0, 2), "A": (3, 2), "S": (3, 3), "D": (3, 4), "F": (3, 5), "G": (3, 6), "H": (3, 7),
            "J": (3, 8), "K": (3, 9), "L": (3, 10), ";": (3, 11), "'": (3, 12), "Enter": (3, 13, 2),
            "Shift": (4, 0, 2.5), "Z": (4, 2), "X": (4, 3), "C": (4, 4), "V": (4, 5), "B": (4, 6), "N": (4, 7),
            "M": (4, 8), ",": (4, 9), ".": (4, 10), "/": (4, 11), "Shift2": (4, 12, 2.5),
            "Ctrl": (5, 0, 1.5), "Super": (5, 1, 1.5), "Alt": (5, 2, 1.5), "Space": (5, 3, 7),  
            "Alt2": (5, 10, 1.5), "Super2": (5, 11, 1.5), "Menu": (5, 12, 1.5), "Ctrl2": (5, 13, 1.5)
        }

        for key, pos in key_positions.items():
            row, col = pos[0], pos[1]
            width_factor = pos[2] if len(pos) > 2 else 1  # Default width factor is 1

            key_display = key[:-1] if key in {"Shift2", "Ctrl2", "Alt2", "Super2"} else key
            key_button = QPushButton(key_display)
            key_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            key_button.setMinimumSize(int(40 * width_factor), 40)

            if self.keybind_manager.get_keybinds_for_key(key_display):
                key_button.setStyleSheet("background-color: orange;")
            else:
                key_button.setStyleSheet("background-color: darkgray;")

            key_button.clicked.connect(lambda checked, k=key_display: self.show_keybinds(k))
            keyboard_layout.addWidget(key_button, row, col, 1, int(width_factor))

        for i in range(14):  # Adjust column spacing
            keyboard_layout.setColumnStretch(i, 1)

        layout.addLayout(keyboard_layout)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def show_keybinds(self, key):
        binds = self.keybind_manager.get_keybinds_for_key(key)
        bind_text = "\n".join(binds) if binds else "No keybinds found."

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Keybinds for {key}")
        dialog.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        dialog.setLayout(QVBoxLayout())

        label = QLabel(bind_text)
        dialog.layout().addWidget(label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        dialog.layout().addWidget(close_button)

        dialog.exec()
