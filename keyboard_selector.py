import json
import os
from keyboards import KeyboardFactory

CONFIG_FILE = os.path.expanduser("~/.config/hyprbinds/keyboard_config.json")

def save_selected_keyboard(layout_name):
    """Save the selected keyboard layout to a config file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump({"selected_layout": layout_name}, file)
        print(f"wrote current keyboard selection: {layout_name} to keyboard_config.json")

def load_selected_keyboard():
    """Loads the previously selected keyboard layout from the config file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                print(f"Loaded config: {config}")  # Debugging line
                return config.get("selected_layout", "qwerty_full")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")  # Debugging line
            pass
    return "qwerty_full"


def get_current_keyboard():
    """Return the keyboard instance based on saved user selection."""
    layout_name = load_selected_keyboard()
    return KeyboardFactory.get_keyboard(layout_name)