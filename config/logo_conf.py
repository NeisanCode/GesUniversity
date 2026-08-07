import os
import sys

# Récupère le dossier racine du .exe (ou du script .py en dev)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemin portable et dynamique vers le logo
LOGO_PATH = os.path.join(BASE_DIR, "assets", "app_logo.png")
