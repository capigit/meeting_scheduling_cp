def print_header():
    header = f"{'Instance':<15} | {'Config':<18} | {'Statut':<8} | {'Temps (s)':<10}"
    print(header)
    print("-" * 60)


def print_row(row):
    print(f"{row['instance']:<15} | {row['config']:<18} | {row['status']:<8} | {row['time']:.4f}s")


def generate_report(filepath, rows, solutions):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Résultats du benchmark: Meeting Scheduling (CSPLib 046)\n\n")
        f.write("## Tableau benchmark\n\n")
        f.write("| Instance | Config | Statut | Temps (s) |\n")
        f.write("|---|---|---|---:|\n")
        for row in rows:
            f.write(f"| {row['instance']} | {row['config']} | {row['status']} | {row['time']:.4f}s |\n")

        f.write("\n## Solutions détaillées (configuration Standard (Min))\n\n")
        for sol in solutions:
            f.write(f"### Instance #{sol['number']}\n")
            if sol['status'] == "SAT" and sol['solution'] is not None:
                f.write("The instance is satisfiable and has the following solution:\n\n")
                for meeting_id, meeting_time in enumerate(sol['solution']):
                    printable_time = 0 if str(meeting_time) == "*" else meeting_time
                    f.write(f"- Meeting {meeting_id} scheduled at time {printable_time}\n")
            elif sol['status'] == "UNSAT":
                f.write("The instance is unsatisfiable.\n")
            else:
                f.write("The solver status is unknown for this instance.\n")
            f.write("\n")
