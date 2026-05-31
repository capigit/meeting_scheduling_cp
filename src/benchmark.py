import os
import re
import time

from pycsp3 import SAT, UNSAT

from src.data_loader import load_instance
from src.model import solve_meeting_problem

CONFIGURATIONS = [
    {"nom": "Standard (Min)", "opt": ""},
    {"nom": "Valeurs Max",    "opt": "valh=max"},
]


def run_benchmark(data_dir):
    """Résout toutes les instances du dossier avec chaque configuration.

    Retourne (rows, solutions) :
    - rows      : liste de dicts {instance, config, status, time} pour le tableau
    - solutions : liste de dicts {number, status, solution} pour la config Standard
    """
    instances = sorted(f for f in os.listdir(data_dir) if f.endswith('.json'))

    rows = []
    solutions = []

    for filename in instances:
        data = load_instance(os.path.join(data_dir, filename))

        for config in CONFIGURATIONS:
            t0 = time.perf_counter()
            result, solution = solve_meeting_problem(data, options=config["opt"])
            elapsed = time.perf_counter() - t0

            if result == SAT:
                status = "SAT"
            elif result == UNSAT:
                status = "UNSAT"
            else:
                status = "UNKNOWN"

            rows.append({
                "instance": filename,
                "config":   config["nom"],
                "status":   status,
                "time":     elapsed,
            })

            if config["nom"] == "Standard (Min)":
                match = re.search(r"(\d+)", filename)
                number = int(match.group(1)) if match else len(solutions) + 1
                solutions.append({
                    "number":   number,
                    "status":   status,
                    "solution": solution,
                })

    return rows, solutions
