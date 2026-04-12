import os
import json

def parse_meeting_file(filepath):
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")

    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    return data