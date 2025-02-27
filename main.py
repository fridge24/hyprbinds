import sys
import os
from PyQt6.QtWidgets import QApplication
from hyprbinds_setup import HyprbindsSetup
from hyprbinds_app import HyprBindsApp

FIRST_RUN_FLAG = os.path.expanduser("~/.config/hyprbinds/.first-run/firstrun.flag")
FIRST_RUN_DIR = os.path.expanduser("~/.config/hyprbinds/.first-run")
def check_first_run():
    """Checks for first-run flag and runs setup if needed."""
    if not os.path.exists(FIRST_RUN_FLAG):
        if not os.path.exists(FIRST_RUN_DIR):
            os.mkdir(FIRST_RUN_DIR)
            print(f"Directory '{FIRST_RUN_DIR}' created successfully.")
        else:
            print(f"Directory '{FIRST_RUN_DIR}' already exists. Proceeding without error.")
        app = QApplication(sys.argv)  # Initialize a temporary Qt app for the dialog
        dialog = HyprbindsSetup()
        if dialog.exec():  # If user completes setup
            with open(FIRST_RUN_FLAG, "w") as f:
                f.write("Setup completed")  # Create flag file
        else:
            print("User cancelled setup, exiting program")
            sys.exit(0)
def main():
    """Main entry point for the application."""
    check_first_run()  # Ensure first-run setup is complete
    app = QApplication(sys.argv)
    window = HyprBindsApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
