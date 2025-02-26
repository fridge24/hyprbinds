Hyprbinds - A GUI tool for configuring Hyprland keybinds

Hyprbinds is a tool that allows Hyprland users to easily add, remove and view existing keybinds. 
There is a visual representation of a keyboard the indicates which keys are bound. As well as simple dialogs
to create a bind by selecting modkeys and a number or letter. The remove dialog allows users to enter a key 
view all binds for that key, and select which one they would like to remove. Supports some basic hyprland 
commands - will add the rest soon, as well as the ability write a custom command the same way you would in 
your hyprland.conf. For example, select exec as your command then enter your command in the input box beside it

No official packages or release yet - Will be officially released first for Arch linux then potentially other distros

INSTALLATION: clone repo from git, cd into it and simply run the command "python main.py"

Dependencies:
PyQt6

NOTE: you WILL have to create a separate source file in your ~/.config/hypr dir
name this file hyprland-keybinds.conf or if you would like edit the source code to define a custom path.
this is because the application reads the keybinds from a user defined config file as 
to not overwrite any content in your main hypr.conf 

SECOND NOTE: has not been tested outside my machine and does not support all bind types just the main 
hyprland bind variable. Also does not support more than one extra modkeys, but that will be fixed 
in upcoming commits along with additional features such as bindl and changing your mousekey binds. 
My intention is the create a suite of GUI applications for configuring various common Hyprland settings. 
I love the flexibility of the CLI and hot reloading, but sometimes you just want a good ol point and click config. 
