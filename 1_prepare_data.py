import json
import os
import re

from src.instance_parser import parse_text_instance


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

    print("\n             ÉTAPE 1 : PRÉPARATION DES DONNÉES")
    print("-" * 60)

    count = 0
    for inst in instances:
        if not inst.strip():
            continue
        count += 1
        donnees = parse_text_instance(inst)
        nom = os.path.join(dossier_sortie, f"instance_{count:02d}.json")
        with open(nom, 'w', encoding='utf-8') as f_json:
            json.dump(donnees, f_json, indent=4)

    print(f"[Succès] {count} instances générées dans {dossier_sortie}")


if __name__ == "__main__":
    main()
