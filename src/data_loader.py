import json
import os


def load_instance(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
