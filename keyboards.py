class Keyboard:
    def __init__(self, name, keys, key_sizes):
        """
        Base Keyboard class representing a generic keyboard layout.
        :param name: Name of the keyboard layout.
        :param keys: A dictionary mapping row/column positions to key labels.
        :param key_sizes: A dictionary mapping key labels to their respective widths.
        """
        self.name = name
        self.keys = keys
        self.key_sizes = key_sizes
    
    def get_keys(self):
        """Returns the key mapping of the keyboard."""
        return self.keys
    
    def has_key(self, key):
        """Checks if a key exists in this keyboard layout."""
        return key in self.keys.values()
    
    def get_layout_name(self):
        """Returns the name of the keyboard layout."""
        return self.name
    
    def get_key_size(self, key):
        """Returns the width of the specified key, defaulting to 1 if not specified."""
        return self.key_sizes.get(key, 1)

class QWERTY_Full(Keyboard):
    def __init__(self):
        keys = {
            # Function key row
            (0, 0): "ESC", (0, 1): "F1", (0, 2): "F2", (0, 3): "F3", (0, 4): "F4",
            (0, 6): "F5", (0, 7): "F6", (0, 8): "F7", (0, 9): "F8",
            (0, 11): "F9", (0, 12): "F10", (0, 13): "F11", (0, 14): "F12",
            (0, 15): "PRTSC", (0, 16): "SCRLK", (0, 17): "PAUSE",

            # Number row
            (1, 0): "` ~", (1, 1): "1", (1, 2): "2", (1, 3): "3", (1, 4): "4",
            (1, 5): "5", (1, 6): "6", (1, 7): "7", (1, 8): "8",
            (1, 9): "9", (1, 10): "0", (1, 11): "- _", (1, 12): "= +",
            (1, 13): "BACKSPACE", (1, 15): "INS", (1, 16): "HOME", (1, 17): "PGUP",

            # QWERTY row
            (2, 0): "TAB", (2, 1): "Q", (2, 2): "W", (2, 3): "E", (2, 4): "R",
            (2, 5): "T", (2, 6): "Y", (2, 7): "U", (2, 8): "I",
            (2, 9): "O", (2, 10): "P", (2, 11): "[{", (2, 12): "]}",
            (2, 13): "\\ |", (2, 15): "DEL", (2, 16): "END", (2, 17): "PGDN",

            # Home row (with empty spaces for WASD)
            (3, 0): "CAPS", (3, 1): "A", (3, 2): "S", (3, 3): "D", (3, 4): "F",
            (3, 5): "G", (3, 6): "H", (3, 7): "J", (3, 8): "K",
            (3, 9): "L", (3, 10): "; :", (3, 11): "' \"", (3, 12): "ENTER" ,

            # Bottom row (Shift and Arrows)
            (4, 0): "LSHIFT", (4, 1): "Z", (4, 2): "X", (4, 3): "C", (4, 4): "V",
            (4, 5): "B", (4, 6): "N", (4, 7): "M", (4, 8): ", <",
            (4, 9): ". >", (4, 10): "/ ?", (4, 11): "RSHIFT",
            (4, 16): "↑",  # Up arrow

            # Bottom row (Modifiers and Arrows)
            (5, 0): "LCTRL", (5, 1): "WIN", (5, 2): "LALT", (5, 3): "SPACE", (5, 4): "RALT",
            (5, 5): "FN", (5, 12): "MENU", (5, 13): "RCTRL", (5, 14): "←", (5, 15): "↓", (5,16): "→",  # Numpad Enter

            # Numpad
            (1, 19): "NLOCK", (1, 20): "/", (1, 21): "*",
            (2, 19): "7", (2, 20): "8", (2, 21): "9",
            (3, 19): "4", (3, 20): "5", (3, 21): "6",
            (4, 19): "1", (4, 20): "2", (4, 21): "3",
            (5, 19): "0", (5, 20): ".", (5, 21): "↵" 
        }

        key_sizes = {
            "SPACE": 7, "LSHIFT": 2, "RSHIFT": 3, "CAPS": 1.75, "ENTER": 3, "TAB": 1.5,
            "LCTRL": 1.5, "RCTRL": 2, "ALT": 1.5, "WIN": 1.5, "BACKSPACE": 2.0, "\\ |": 2.0
        }

        super().__init__("QWERTY Full", keys, key_sizes)




class QWERTY_Reduced(Keyboard):
    def __init__(self):
        keys = {
            # Function keys and ESC
            (0, 0): "ESC", (0, 1): "F1", (0, 2): "F2", (0, 3): "F3", (0, 4): "F4",
            (0, 5): "F5", (0, 6): "F6", (0, 7): "F7", (0, 8): "F8",
            (0, 9): "F9", (0, 10): "F10",

            # Number row
            (1, 0): "`", (1, 1): "1", (1, 2): "2", (1, 3): "3", (1, 4): "4",
            (1, 5): "5", (1, 6): "6", (1, 7): "7", (1, 8): "8",
            (1, 9): "9", (1, 10): "0",

            # QWERTY row
            (2, 0): "Q", (2, 1): "W", (2, 2): "E", (2, 3): "R", (2, 4): "T",
            (2, 5): "Y", (2, 6): "U", (2, 7): "I", (2, 8): "O",
            (2, 9): "P",

            # Home row
            (3, 0): "A", (3, 1): "S", (3, 2): "D", (3, 3): "F", (3, 4): "G",
            (3, 5): "H", (3, 6): "J", (3, 7): "K", (3, 8): "L",

            # Bottom row
            (4, 0): "Z", (4, 1): "X", (4, 2): "C", (4, 3): "V", (4, 4): "B",
            (4, 5): "N", (4, 6): "M"
        }
        key_sizes = {
            "SPACE": 7, "LSHIFT": 2, "RSHIFT": 3, "CAPS": 1.75, "ENTER": 3, "TAB": 1.5,
            "LCTRL": 1.5, "RCTRL": 2, "ALT": 1.5, "WIN": 1.5, "BACKSPACE": 2.0, "\\": 2.0
        }
        
        super().__init__("QWERTY Reduced", keys, {})

class Dvorak(Keyboard):
    def __init__(self):
        keys = {
            # Function keys
            (0, 0): "ESC", (0, 1): "F1", (0, 2): "F2", (0, 3): "F3", (0, 4): "F4",
            (0, 5): "F5", (0, 6): "F6", (0, 7): "F7", (0, 8): "F8",
            (0, 9): "F9", (0, 10): "F10", (0, 11): "F11", (0, 12): "F12",

            # Number row
            (1, 0): "`", (1, 1): "1", (1, 2): "2", (1, 3): "3", (1, 4): "4",
            (1, 5): "5", (1, 6): "6", (1, 7): "7", (1, 8): "8",
            (1, 9): "9", (1, 10): "0", (1, 11): "[", (1, 12): "]",

            # Dvorak top row
            (2, 0): "TAB", (2, 1): "'", (2, 2): ",", (2, 3): ".", (2, 4): "P",
            (2, 5): "Y", (2, 6): "F", (2, 7): "G", (2, 8): "C",
            (2, 9): "R", (2, 10): "L", (2, 11): "/", (2, 12): "=",

            # Home row
            (3, 0): "CAPS", (3, 1): "A", (3, 2): "O", (3, 3): "E", (3, 4): "U",
            (3, 5): "I", (3, 6): "D", (3, 7): "H", (3, 8): "T",
            (3, 9): "N", (3, 10): "S", (3, 11): "-",

            # Bottom row
            (4, 0): "RSHIFT", (4, 1): ";", (4, 2): "Q", (4, 3): "J", (4, 4): "K",
            (4, 5): "X", (4, 6): "B", (4, 7): "M", (4, 8): "W",
            (4, 9): "V", (4, 10): "Z", (4, 11): "LSHIFT"
        }
        key_sizes = {
            "SPACE": 7, "LSHIFT": 2, "RSHIFT": 3, "CAPS": 1.75, "ENTER": 3, "TAB": 1.5,
            "LCTRL": 1.5, "RCTRL": 2, "ALT": 1.5, "WIN": 1.5, "BACKSPACE": 2.0, "\\": 2.0
        }
        super().__init__("Dvorak", keys, {})

class AZERTY(Keyboard):
    def __init__(self):
        keys = {
            (1, 0): "²", (1, 1): "&", (1, 2): "é", (1, 3): "\"", (1, 4): "'",
            (1, 5): "(", (1, 6): "-", (1, 7): "è", (1, 8): "_",
            (1, 9): "ç", (1, 10): "à", (1, 11): ")", (1, 12): "=",

            (2, 0): "TAB", (2, 1): "A", (2, 2): "Z", (2, 3): "E", (2, 4): "R",
            (2, 5): "T", (2, 6): "Y", (2, 7): "U", (2, 8): "I",
            (2, 9): "O", (2, 10): "P", (2, 11): "^", (2, 12): "$",

            (3, 0): "CAPS", (3, 1): "Q", (3, 2): "S", (3, 3): "D", (3, 4): "F",
            (3, 5): "G", (3, 6): "H", (3, 7): "J", (3, 8): "K",
            (3, 9): "L", (3, 10): "M", (3, 11): "ù", (3, 12): "*",
        }
        key_sizes = {
            "SPACE": 7, "LSHIFT": 2, "RSHIFT": 3, "CAPS": 1.75, "ENTER": 3, "TAB": 1.5,
            "LCTRL": 1.5, "RCTRL": 2, "ALT": 1.5, "WIN": 1.5, "BACKSPACE": 2.0, "\\": 2.0
        }


        super().__init__("AZERTY", keys, {})

class Colemak(Keyboard):
    def __init__(self):
        keys = {
            # Number row remains unchanged
            (1, 1): "1", (1, 2): "2", (1, 3): "3", (1, 4): "4",
            (1, 5): "5", (1, 6): "6", (1, 7): "7", (1, 8): "8",
            (1, 9): "9", (1, 10): "0",

            # Colemak Top row
            (2, 1): "Q", (2, 2): "W", (2, 3): "F", (2, 4): "P",
            (2, 5): "G", (2, 6): "J", (2, 7): "L", (2, 8): "U",
            (2, 9): "Y", (2, 10): ";",
        }
        key_sizes = {
            "SPACE": 7, "LSHIFT": 2, "RSHIFT": 3, "CAPS": 1.75, "ENTER": 3, "TAB": 1.5,
            "LCTRL": 1.5, "RCTRL": 2, "ALT": 1.5, "WIN": 1.5, "BACKSPACE": 2.0, "\\": 2.0
        }
        super().__init__("Colemak", keys, {})


class KeyboardFactory:
    @staticmethod
    def get_keyboard(layout):
        """
        Returns a Keyboard object based on the layout name.
        :param layout: The name of the keyboard layout.
        """
        layouts = {
            "qwerty_full": QWERTY_Full(),
            "qwerty_reduced": QWERTY_Reduced(),
            "azerty": AZERTY(),
            "dvorak": Dvorak(),
            "colemak": Colemak()
        }
        return layouts.get(layout.lower(), Keyboard(layout, {}, {}))