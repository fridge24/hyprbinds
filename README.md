Hyprbinds - A GUI tool for configuring Hyprland keybinds, written in python with PyQt6

Hyprbinds is a tool that allows Hyprland users to easily add, remove and view existing keybinds. 

There is a visual representation of a keyboard the indicates which keys are bound. As well as a simple dialog
to create a bind by selecting modkeys and a number or letter along with your desired command. The remove dialog in the same popup allows users to view all binds for that key, and then select which one they would like to remove. The application currently supports some basic hyprland commands - will add the rest soon, as well as the ability write a custom command the same way you would in your hyprland.conf. For example, select exec as your command then enter your custom command in the input box.

NOTE: You WILL have to create a separate source file in your ~/.config/hypr or other directory (If you already have a separate config file for your keybinds you can skip this step and just select it in setup). Setting your binds filepath can be done via the setup window that runs when you first open the app. You can also open the setup at any time in the future to change the location at which your binds will be written and read from. The gui includes an option to read and erase and keybinds from your hyprland.conf file (expected to be stored at ~/.config/hypr/hyprland.conf). You must delete any existing keybinds in your main config file to avoid creating duplicates and conflictions with hyprbinds.    

The application functions by extracting all the lines that contain binds from your currently selected keybinds.conf file to a json file. All bind additions and removals within the application are written to the json file until the user selects apply. At that point, the updated json binds list with whatever modifications you made is formatted and re-applied to your hyprland-keybinds.conf. The users selected keybind layout and keybind filepath are also stored in respective json files. The application checks for duplicates to ensure that you do not add multiple binds with the same key strokes. Unfortunately this means that if you would like to exec multiple commands with a single keypress this is not supported currently.

No official packages or release yet - Will be officially released first for Arch linux then potentially other distros

Any contributions to the project are welcome :) 

INSTALLATION: clone repo from git, cd into it and simply run main.py using python

Dependencies:
Python
PyQt6

SECOND NOTE: has not been tested outside my local environment and does not support all bind types just the main hyprland bind variable. Also does not support more than one extra modkeys, but that will be fixed 
in upcoming commits along with additional features such as support for all Hyprland bind types: bindel, bindl, bindm, and global binds.  

My end intention is the create a suite of GUI applications for configuring various common Hyprland settings such as monitor and workspace settings, default apps, window rules, colors, animations, enviroment variables, and more, I then plan on creating some sort of parent settings app called hyprconfig, though there already appears to be a project with that name but there does not appear to be recent activity on the repo. The goal is that hyprconfig will eventually act as if it were a settings app within a full fledged desktop environment.  

I love the flexibility of the CLI and hot reloading my hyprland config, but sometimes you just want a good ol point and click config.
