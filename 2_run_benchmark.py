import os

from src.benchmark import run_benchmark
from src.reporter import generate_report, print_header, print_row


def main():
    data_dir = "data/processed/"
    results_dir = "results/"
    output_file = os.path.join(results_dir, "benchmark_output.md")

    print("\n         ÉTAPE 2 : BENCHMARK MEETING SCHEDULING")
    print("-" * 60)

    if not os.path.exists(data_dir):
        print(f"ERREUR : Le dossier '{data_dir}' n'existe pas. Lancez d'abord 1_prepare_data.py")
        return

    os.makedirs(results_dir, exist_ok=True)

    print_header()

    rows, solutions = run_benchmark(data_dir)

    for row in rows:
        print_row(row)

    generate_report(output_file, rows, solutions)

    print("-" * 60)
    print(f"Les résultats ont été sauvegardés dans : {output_file}")


if __name__ == "__main__":
    main()
