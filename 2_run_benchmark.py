import os
import re
import time
from pycsp3 import SAT, UNSAT
from src.parser import parse_meeting_file
from src.meeting_model import solve_meeting_problem

def main():
    print("\n         ÉTAPE 2 : BENCHMARK MEETING SCHEDULING")
    print("-" * 60)
    
    dossier_data = "data/processed/"
    dossier_resultats = "results/"
    
    if not os.path.exists(dossier_data):
        print(f"ERREUR : Le dossier '{dossier_data}' n'existe pas. Lancez d'abord 1_prepare_data.py")
        return
        
    os.makedirs(dossier_resultats, exist_ok=True)
    fichier_resultat_md = os.path.join(dossier_resultats, "benchmark_output.md")
        
    instances = sorted([f for f in os.listdir(dossier_data) if f.endswith('.json')])
    
    configurations = [
        {"nom": "Standard (Min)", "opt": ""},
        {"nom": "Valeurs Max", "opt": "valh=max"}
    ]
    
    en_tete = f"{'Instance':<15} | {'Config':<18} | {'Statut':<8} | {'Temps (s)':<10}\n" + "-" * 60 + "\n"
    print(en_tete, end="")
    
    with open(fichier_resultat_md, "w", encoding="utf-8") as f_md:
        f_md.write("# Résultats du benchmark: Meeting Scheduling (CSPLib 046)\n\n")
        f_md.write("## Tableau benchmark\n\n")
        f_md.write("| Instance | Config | Statut | Temps (s) |\n")
        f_md.write("|---|---|---|---:|\n")

        solutions_standard = []
        
        for fichier in instances:
            chemin = os.path.join(dossier_data, fichier)
            donnees = parse_meeting_file(chemin)
            statut_standard = "UNKNOWN"
            solution_standard = None
            
            for config in configurations:
                debut = time.perf_counter()
                
                statut_resolution, solution = solve_meeting_problem(donnees, options=config["opt"])
                
                fin = time.perf_counter()
                duree = fin - debut
                
                if statut_resolution == SAT:
                    statut = "SAT"
                elif statut_resolution == UNSAT:
                    statut = "UNSAT"
                else:
                    statut = "UNKNOWN"
                
                ligne_resultat = f"{fichier:<15} | {config['nom']:<18} | {statut:<8} | {duree:.4f}s\n"
                
                print(ligne_resultat, end="")
                f_md.write(f"| {fichier} | {config['nom']} | {statut} | {duree:.4f}s |\n")

                if config["nom"] == "Standard (Min)":
                    statut_standard = statut
                    solution_standard = solution

            match = re.search(r"(\d+)", fichier)
            numero_instance = int(match.group(1)) if match else len(solutions_standard) + 1
            solutions_standard.append((numero_instance, statut_standard, solution_standard))

        f_md.write("\n## Solutions détaillées (configuration Standard (Min))\n\n")

        for numero_instance, statut, solution in solutions_standard:
            f_md.write(f"### Instance #{numero_instance}\n")

            if statut == "SAT" and solution is not None:
                f_md.write("The instance is satisfiable and has the following solution:\n\n")
                for meeting_id, meeting_time in enumerate(solution):
                    printable_time = 0 if str(meeting_time) == "*" else meeting_time
                    f_md.write(f"- Meeting {meeting_id} scheduled at time {printable_time}\n")
            elif statut == "UNSAT":
                f_md.write("The instance is unsatisfiable.\n")
            else:
                f_md.write("The solver status is unknown for this instance.\n")

            f_md.write("\n")
                
    print("-" * 60)
    print(f"Les résultats ont été sauvegardés dans : {fichier_resultat_md}")

if __name__ == "__main__":
    main()