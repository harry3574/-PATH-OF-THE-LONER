import sys
import os

# Define the path to the MenuScreen.py file
menu_screen_path = os.path.join('MenuScreen.py')

# Check if the file exists
if not os.path.isfile(menu_screen_path):
    print(f"Error: {menu_screen_path} does not exist.")
    sys.exit(1)

# Run the MenuScreen.py file
with open(menu_screen_path) as f:
    exec(f.read())
