from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QGridLayout, 
    QComboBox, QLineEdit, QMessageBox
)

def show_keybinds(parent, key, keybind_manager):
    """Displays current binds for the selected key and allows adding/removing keybinds."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"Manage Keybinds for: {key}")
    layout = QVBoxLayout()

    # **Current Binds Section**
    layout.addWidget(QLabel("<b>Current Keybinds:</b>"))
    
    bind_list = QListWidget()
    bind_list.addItems(keybind_manager.get_keybinds_for_key(key))
    layout.addWidget(bind_list)

    format_label = QLabel("Format: <i>MOD+SEC_MOD, Key → Command, Argument</i>")
    layout.addWidget(format_label)

    # **Add Keybind Section**
    add_layout = QGridLayout()
    add_layout.addWidget(QLabel("<b>Add a New Keybind</b>"), 0, 0, 1, 4)

    mod_dropdown = QComboBox()
    mod_dropdown.addItems(["SUPER", "CTRL", "ALT", "None"])
    add_layout.addWidget(QLabel("Modifier:"), 1, 0)
    add_layout.addWidget(mod_dropdown, 1, 1)

    sec_mod_dropdown = QComboBox()
    sec_mod_dropdown.addItems(["None", "SHIFT", "ALT"])
    add_layout.addWidget(QLabel("Secondary Mod:"), 2, 0)
    add_layout.addWidget(sec_mod_dropdown, 2, 1)

    command_dropdown = QComboBox()
    command_dropdown.addItems(["movewindow", "exit", "fullscreen", "exec", "togglefloating", "Custom"])
    add_layout.addWidget(QLabel("Command:"), 3, 0)
    add_layout.addWidget(command_dropdown, 3, 1)

    argument_field = QLineEdit()
    argument_field.setPlaceholderText("Optional: Custom command")
    argument_field.setVisible(False)
    command_dropdown.currentTextChanged.connect(
        lambda: argument_field.setVisible(command_dropdown.currentText() in ["exec", "Custom"])
    )
    add_layout.addWidget(argument_field, 3, 2)

    add_button = QPushButton("Add Keybind")
    add_button.clicked.connect(lambda: add_new_bind(key, mod_dropdown, sec_mod_dropdown, command_dropdown, argument_field, bind_list, keybind_manager, parent))
    add_layout.addWidget(add_button, 4, 0, 1, 3)

    layout.addLayout(add_layout)

    # **Remove Keybind Section**
    remove_button = QPushButton("Remove Selected")
    remove_button.clicked.connect(lambda: remove_selected_bind(key, bind_list, keybind_manager, parent))
    layout.addWidget(QLabel("<b>Remove Selected Keybinds</b>"))
    layout.addWidget(remove_button)

    # **Close Button**
    close_button = QPushButton("Close")
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec()

def add_new_bind(key, mod_dropdown, sec_mod_dropdown, command_dropdown, argument_field, bind_list, keybind_manager, parent):
    """Handles adding a new keybind."""
    modifiers = mod_dropdown.currentText()
    sec_mod = sec_mod_dropdown.currentText()
    command = command_dropdown.currentText()
    argument = argument_field.text()

    if keybind_manager.is_keybind_taken(modifiers, sec_mod, key):
        QMessageBox.warning(parent, "Error", "This keybind is already taken!")
        return

    error_message = keybind_manager.add_keybind(modifiers, sec_mod, key, command, argument)
    if error_message:
        QMessageBox.warning(parent, "Error", error_message)
    else:
        bind_list.addItem(f"{modifiers}+{sec_mod if sec_mod != 'None' else ''}{key} → {command} {argument}".strip())

def remove_selected_bind(key, bind_list, keybind_manager, parent):
    """Removes the selected keybind."""
    selected_item = bind_list.currentItem()
    if not selected_item:
        QMessageBox.warning(parent, "Error", "No keybind selected for removal.")
        return

    try:
        bind_str = selected_item.text()  # Example: "SUPER+ALT+A → movewindow"
        bind_parts = bind_str.split(" → ")[0].split("+")

        if len(bind_parts) == 3:
            modifiers, sec_mod, key_name = bind_parts
        elif len(bind_parts) == 2:
            modifiers, key_name = bind_parts
            sec_mod = "None"
        else:
            raise ValueError("Invalid keybind format detected.")

        if not keybind_manager.is_keybind_taken(modifiers, sec_mod, key_name):
            QMessageBox.warning(parent, "Error", "Keybind not found. It may have already been removed.")
            return

        removal_result = keybind_manager.remove_keybind(modifiers, sec_mod, key_name)
        if removal_result == "Keybind not found.":
            QMessageBox.warning(parent, "Error", "Failed to remove keybind: Keybind does not exist.")
            return

        bind_list.takeItem(bind_list.row(selected_item))

    except Exception as e:
        QMessageBox.critical(parent, "Error", f"An unexpected error occurred: {str(e)}")
