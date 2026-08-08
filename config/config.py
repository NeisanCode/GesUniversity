import os
import sys

# Determining the root folder
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(DATA_DIR, exist_ok=True)

# Path files
DB_PATH = os.path.join(DATA_DIR, "school.db")
LOGO_PATH = os.path.join(ASSETS_DIR, "app_logo.png")
ICON_PATH = os.path.join(ASSETS_DIR, "app_icon_bip.ico")

# License path
LICENSE_PATH = os.path.join(BASE_DIR, "LICENSE.txt")