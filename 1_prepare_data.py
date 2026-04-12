import os
import re
import json

def parse_text_instance(instance_text):
    data = {"NumberOfMeetings": 0, "NumberOfAgents": 0, "DomainSize": 0, "AgentMeetings": [], "Distances": []}
    mode = None
    
    for line in instance_text.split('\n'):
        line = line.strip()
        if not line: continue
        
        if '=' in line and mode is None:
            key, value = line.split('=')
            data[key.strip()] = int(value.strip())
        elif line.startswith("Agents Meetings:"): mode = "agents"; continue
        elif line.startswith("Between Meetings Distance:"): mode = "distances"; continue
        elif line.startswith("Estimated"): break

        if mode == "agents" and line.startswith("Agents"):
            parts = line.split(':')
            if len(parts) == 2:
                data["AgentMeetings"].append([int(x) for x in parts[1].split()])
        elif mode == "distances" and ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                data["Distances"].append([int(x) for x in parts[1].split()])
    return data

def main():
    fichier_brut = "data/raw/toutes_les_instances.txt"
    dossier_sortie = "data/processed/"
    
    os.makedirs(dossier_sortie, exist_ok=True)
    
    if not os.path.exists(fichier_brut):
        print(f"ERREUR : Fichier '{fichier_brut}' introuvable.")
        return

    with open(fichier_brut, 'r', encoding='utf-8') as f:
        content = f.read()

    instances = re.split(r'\*\*Instance #\d+\*\*', content)
    
    count = 0
    print("\n             ÉTAPE 1 : PRÉPARATION DES DONNÉES")
    print("-" * 60)
    for inst in instances:
        if not inst.strip(): continue
        count += 1
        
        donnees_propres = parse_text_instance(inst)
        
        nom_fichier = os.path.join(dossier_sortie, f"instance_{count:02d}.json")
        with open(nom_fichier, 'w', encoding='utf-8') as f_json:
            json.dump(donnees_propres, f_json, indent=4)
            
    print(f"[Succès] {count} instances ont été générées au format JSON dans {dossier_sortie}")

if __name__ == "__main__":
    main()