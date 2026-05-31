import json
import os
import re
from datetime import date


def parse_benchmark_md(filepath):
    rows = {}
    solutions = {}
    current_inst = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            m = re.match(r'\| (instance_\d+\.json) \| (.+?) \| (\w+) \| ([\d.]+)s \|', line)
            if m:
                fname, config, status, time_str = m.group(1), m.group(2).strip(), m.group(3), float(m.group(4))
                if fname not in rows:
                    rows[fname] = {}
                key = 'standard' if 'Standard' in config else 'max'
                rows[fname][key] = {'status': status, 'time': time_str}
                continue

            m = re.match(r'### Instance #(\d+)', line)
            if m:
                current_inst = int(m.group(1))
                solutions[current_inst] = []
                continue

            if current_inst is not None:
                m = re.match(r'- Meeting \d+ scheduled at time (\d+)', line)
                if m:
                    solutions[current_inst].append(int(m.group(1)))

    return rows, solutions


def main():
    data_dir = 'data/processed/'
    md_file = 'results/benchmark_output.md'
    output_file = 'docs/data/benchmark.json'

    if not os.path.exists(md_file):
        print(f"ERREUR : '{md_file}' introuvable. Lancez d'abord 2_run_benchmark.py")
        return

    rows, solutions = parse_benchmark_md(md_file)

    instances = []
    for fname in sorted(rows.keys()):
        num = int(re.search(r'(\d+)', fname).group(1))
        path = os.path.join(data_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            inst = json.load(f)

        instances.append({
            'id': num,
            'filename': fname,
            'n_meetings': inst['NumberOfMeetings'],
            'n_agents': inst['NumberOfAgents'],
            'domain_size': inst['DomainSize'],
            'standard': rows[fname].get('standard', {}),
            'max': rows[fname].get('max', {}),
            'solution': solutions.get(num, []),
        })

    output = {
        'generated': str(date.today()),
        'instances': instances,
    }

    os.makedirs('docs/data', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'\n[Succès] {len(instances)} instances exportées vers {output_file}')


if __name__ == '__main__':
    main()
