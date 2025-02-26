Hyprbinds - A GUI tool for configuring Hyprland keybinds

Hyprbinds is a tool that allows Hyprland users to easily add, remove and view existing keybinds. 
There is a visual representation of a keyboard the indicates which keys are bound. As well as simple dialogs
to create a bind by selecting modkeys and a number or letter. The remove dialog allows users to enter a key 
view all binds for that key, and select which one they would like to remove. Supports some basic hyprland 
commands - will add the rest soon, as well as the ability write a custom command the same way you would in 
your hyprland.conf. For example, select exec as your command then enter your command in the input box beside it

NOTE: you WILL have to create a separate source file in your ~/.config/hypr dirname this file hyprland-keybinds.conf or if you would like edit the source code to define a custom path.this is because the application reads the keybinds from a user defined config file as to not overwrite any content in your main hypr.conf 

The application functions by extracting your current hyprland-keybinds.conf file to a json file. All bind edits within the application are written to the json file until the user selects apply. At that point the updated binds list from the json file is formatted, and re-applied to your hyprland-keybinds.conf. The application also checks for duplicates to ensure that you do not add multiple binds with the same key strokes. (If you would like to exec multiple commands with a single keypress this must be maually configured in your keybinds file though multi command support is a future target.)

No official packages or release yet - Will be officially released first for Arch linux then potentially other distros

Any contributions to the project are welcome :) 

INSTALLATION: clone repo from git, cd into it and simply run main.py using python

Dependencies:
Python
PyQt6

SECOND NOTE: has not been tested outside my local environment and does not support all bind types just the main 
hyprland bind variable. Also does not support more than one extra modkeys, but that will be fixed 
in upcoming commits along with additional features such as support for all Hyprland bind types: bindel, bindl, bindm, and global binds.  

My end intention is the create a suite of GUI applications for configuring various common Hyprland settings such as monitor and workspace settings, default apps, window rules, colors, animations, enviroment variables, and more, I then plan on creating some sort of parent settings app called hyprconfig, though there already appears to be a project with that name so I might abandon this proect and contribute what I have to that instead. The goal is that hyprconfig will eventually act as if it were a settings app within a full fledged desktop environment.  

I love the flexibility of the CLI and hot reloading my hyprland config, but sometimes you just want a good ol point and click config.
