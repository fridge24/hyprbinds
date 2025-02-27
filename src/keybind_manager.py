import os
import json
import shutil

CONFIG_FILE = os.path.expanduser("~/.config/hyprbinds/keyboard_config.json")
JSON_KEYBINDS_FILE = os.path.expanduser("~/.config/hyprbinds/keybinds.json")

def get_keybinds_path():
    """Extracts the keybinds file path from a JSON config file."""
    config_path = os.path.expanduser("~/.config/hyprbinds/keybinds_config.json")
    
    try:
        with open(config_path, "r") as file:
            data = json.load(file)
            if "keybinds_path" in data:
                return os.path.expanduser(data["keybinds_path"])
            else:
                raise KeyError("Missing 'keybinds_path' in JSON config.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading keybinds path: {e}")
        return None

# Set KEYBINDS_FILE dynamically
KEYBINDS_FILE = get_keybinds_path()

# Validate the extracted path
if not KEYBINDS_FILE or not os.path.exists(KEYBINDS_FILE):
    print(f"Error: Keybinds file '{KEYBINDS_FILE}' does not exist.")

class KeybindManager:
    def __init__(self):
        """Initialize the keybind manager and parse existing keybinds."""
        self.keybinds = self.parse_keybinds()
        self.save_json_keybinds()  # Overwrite JSON file with fresh keybinds

    def parse_keybinds(self):
        """Reads the config file and extracts keybinds into a nested dictionary."""
        keybinds = {}
        try:
            with open(KEYBINDS_FILE, "r") as file:
                for line in file:
                    if line.startswith("bind ="):
                        parts = line.strip().split(", ")
                        modifiers = parts[0].split(" ")[2:]
                        key = parts[1].upper()
                        command = parts[2] if len(parts) > 2 else ""
                        argument = parts[3] if len(parts) > 3 else ""

                        sec_mod = "None"
                        for mod in ["SHIFT", "ALT"]:
                            if mod in modifiers:
                                sec_mod = mod
                                modifiers.remove(mod)
                        primary_mod = modifiers[0] if modifiers else "None"

                        if primary_mod not in keybinds:
                            keybinds[primary_mod] = {}
                        if sec_mod not in keybinds[primary_mod]:
                            keybinds[primary_mod][sec_mod] = {}

                        keybinds[primary_mod][sec_mod][key] = {"command": command, "argument": argument}
        except FileNotFoundError:
            pass
        return keybinds
        
    def save_json_keybinds(self):
        """Overwrites the JSON file with the latest parsed keybinds from Hyprland."""
        with open(JSON_KEYBINDS_FILE, "w") as file:
            json.dump(self.keybinds, file, indent=4)

    def load_json_keybinds(self):
        """Loads keybinds from the JSON file if it exists."""
        if os.path.exists(JSON_KEYBINDS_FILE):
            with open(JSON_KEYBINDS_FILE, "r") as file:
                self.keybinds.update(json.load(file))

    def parse_json(self):
        try:
            with open(JSON_KEYBINDS_FILE, "r") as file:
                keybinds = json.load(file)
            config_lines = []
            for mod, sec_mods in keybinds.items():
                for sec_mod, keys in sec_mods.items():
                    for key, bind in keys.items():
                        line = f'bind = {mod}'
                        if sec_mod != "None":
                            line += f'+{sec_mod}'
                        line += f', {key}, {bind["command"]}'
                        if bind["argument"]:
                            line += f', {bind["argument"]}'
                        config_lines.append(line)
            return config_lines
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return []

    def apply_keybind_changes(self):
        keybinds_config = self.parse_json()
        try:
            with open(KEYBINDS_FILE, "w") as file:
                file.write("\n".join(keybinds_config) + "\n")
            print(f"Keybinds updated successfully in {KEYBINDS_FILE}")
        except Exception as e:
            print(f"Error updating keybinds: {e}")

    def get_keybinds(self):
        """Returns a flattened list of keybinds."""
        keybind_list = []
        for mod, sec_mods in self.keybinds.items():
            for sec_mod, keys in sec_mods.items():
                for key, bind in keys.items():
                    keybind_list.append({
                        "modifiers": mod,
                        "secondary_modifier": sec_mod,
                        "key": key,
                        "command": bind["command"],
                        "argument": bind["argument"]
                    })
        return keybind_list

    def is_keybind_taken(self, modifiers, sec_mod, key):
        """Checks if a keybind exists in the dictionary."""
        key = key.upper()
        return modifiers in self.keybinds and sec_mod in self.keybinds[modifiers] and key in self.keybinds[modifiers][sec_mod]

    def add_keybind(self, modifiers, sec_mod, key, command, argument):
        """Adds a keybind to the JSON file without modifying the config file."""
        key = key.upper()
        if self.is_keybind_taken(modifiers, sec_mod, key):
            return "This keybind is already taken!"

        if modifiers not in self.keybinds:
            self.keybinds[modifiers] = {}
        if sec_mod not in self.keybinds[modifiers]:
            self.keybinds[modifiers][sec_mod] = {}

        self.keybinds[modifiers][sec_mod][key] = {"command": command, "argument": argument}
        self.save_json_keybinds()
        return None

    def remove_keybind(self, modifiers, sec_mod, key):
        """Removes a keybind from the JSON file."""
        key = key.upper()
        if self.is_keybind_taken(modifiers, sec_mod, key):
            del self.keybinds[modifiers][sec_mod][key]
            if not self.keybinds[modifiers][sec_mod]:
                del self.keybinds[modifiers][sec_mod]
            if not self.keybinds[modifiers]:
                del self.keybinds[modifiers]
            self.save_json_keybinds()
            return None
        return "Keybind not found."

    def save_keybinds_to_file(self):
        try:
            # Create a backup of the current keybinds file
            shutil.copy(KEYBINDS_FILE, KEYBINDS_FILE + ".backup")
            print(f"Backup created at {KEYBINDS_FILE}.backup")

            # Read the existing file content
            with open(KEYBINDS_FILE, "r") as file:
                lines = file.readlines()

            # Remove all lines starting with "bind ="
            lines = [line.rstrip() for line in lines if not line.strip().startswith("bind =")]

            # Get the updated keybinds from the JSON representation
            bind_lines = [line.strip() for line in self.parse_json()]  # Ensure no extra spaces/newlines

            # Combine the filtered lines with the updated keybinds
            updated_lines = lines + bind_lines

            # Write the fully updated content back to the file
            with open(KEYBINDS_FILE, "w") as file:
                file.write("\n".join(updated_lines) + "\n")  # Ensures only one newline between entries

            print(f"Keybinds successfully applied to {KEYBINDS_FILE}")
        except Exception as e:
            print(f"Error saving keybinds: {e}")

    def get_keybinds_for_key(self, key):
        """
        Fetch keybinds associated with a specific key from the JSON file.
        
        Args:
            key (str): The key to check for bindings.
        
        Returns:
            list: A list of formatted strings representing the keybinds bound to the given key.
        """
        key = key.upper()  # Ensure case consistency
        matching_binds = []

        try:
            with open(JSON_KEYBINDS_FILE, "r") as file:
                keybinds = json.load(file)

            for mod, sec_mods in keybinds.items():
                for sec_mod, keys in sec_mods.items():
                    if key in keys:
                        bind = keys[key]
                        sec_mod_display = f"+{sec_mod}" if sec_mod != "None" else ""
                        matching_binds.append(f"bind = {mod}{sec_mod_display}, {key}, {bind['command']}, {bind['argument']}")

        except FileNotFoundError:
            print(f"Warning: {JSON_KEYBINDS_FILE} not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {JSON_KEYBINDS_FILE}.")

        return matching_binds  # Returns a list of keybinds or an empty list if none are found
