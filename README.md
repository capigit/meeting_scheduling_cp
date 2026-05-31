<div align="center">

# Meeting Scheduling CP — CSPLib 046

> Résolution par Programmation par Contraintes du problème de planification de réunions [CSPLib prob046](https://www.csplib.org/Problems/prob046/).

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-required-ED8B00?logo=openjdk&logoColor=white)
![Solver](https://img.shields.io/badge/Solver-ACE%20via%20PyCSP3-5C2D91)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## Table des matières

- [Aperçu](#aperçu)
- [Modèle CSP](#modèle-csp)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Données](#données)
- [Exécution](#exécution)
- [Résultats](#résultats)
- [Dashboard GitHub Pages](#dashboard-github-pages)
- [Configuration solveur](#configuration-solveur)
- [Structure du projet](#structure-du-projet)

---

## Aperçu

| Fonctionnalité | Détail |
|---|---|
| Modélisation | CSP avec [PyCSP3](https://pycsp3.org) |
| Solveur | ACE (via PyCSP3) |
| Données | Instances CSPLib 046 |
| Pipeline | Parsing → JSON → Résolution → Benchmark → Dashboard |

---

## Modèle CSP

**Variables** — un créneau de départ `starts[i]` par réunion, avec le domaine `{0, …, DomainSize - 1}`.

**Contraintes** — pour chaque agent, toutes les paires de réunions auxquelles il participe doivent être séparées d'au moins `distance[m1][m2]` créneaux :

```
|starts[m1] - starts[m2]| >= distance[m1][m2]
```

---

## Prérequis

- **Python** 3.8+
- **Java** JRE ou JDK — requis par le solveur ACE en arrière-plan

```bash
python3 --version
java -version
```

---

## Installation

```bash
git clone https://github.com/capigit/meeting_scheduling_cp.git
cd meeting_scheduling_cp

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Données

Les instances proviennent de CSPLib :

- **Problème** : https://www.csplib.org/Problems/prob046/
- **Instances** : https://www.csplib.org/Problems/prob046/data/instances.md.html

Placer le fichier téléchargé ici :

```
data/raw/toutes_les_instances.txt
```

### Format du fichier brut

Les instances sont délimitées par `**Instance #N**`. Chaque bloc contient :

```
**Instance #1**
NumberOfMeetings = 10
NumberOfAgents   = 5
DomainSize       = 8

Agents Meetings:
Agents 0: 0 3 7
Agents 1: 1 4 8
...

Between Meetings Distance:
Meeting 0: 0 3 2 1 ...
Meeting 1: 3 0 1 2 ...
...
```

### Format JSON intermédiaire

Chaque instance est convertie en JSON dans `data/processed/` :

| Champ | Type | Description |
|---|---|---|
| `NumberOfMeetings` | `int` | Nombre total de réunions |
| `NumberOfAgents` | `int` | Nombre d'agents |
| `DomainSize` | `int` | Nombre de créneaux disponibles |
| `AgentMeetings` | `list[list[int]]` | Réunions de chaque agent |
| `Distances` | `list[list[int]]` | Distance minimale entre chaque paire de réunions |

---

## Exécution

### Étape 1 — Préparer les données

```bash
venv/bin/python 1_prepare_data.py
```

Génère les fichiers JSON dans `data/processed/`.

### Étape 2 — Lancer le benchmark

```bash
venv/bin/python 2_run_benchmark.py
```

Affiche les résultats en console et les exporte dans `results/benchmark_output.md`.

### Étape 3 — Générer les données du dashboard

```bash
python3 3_export_web_data.py
```

Lit `results/benchmark_output.md` et les JSONs de `data/processed/`, puis produit `docs/data/benchmark.json` pour le dashboard web.

---

## Résultats

Le fichier `results/benchmark_output.md` contient deux sections :

1. **Tableau de benchmark** — statut (`SAT` / `UNSAT` / `UNKNOWN`) et temps de résolution par instance et par configuration
2. **Solutions détaillées** — pour chaque instance satisfiable, le créneau attribué à chaque réunion (configuration Standard)

> Chaque exécution régénère entièrement ce fichier.

---

## Dashboard GitHub Pages

Le dossier `docs/` contient une application statique (HTML/CSS/JS) déployable sur GitHub Pages.

**Fonctionnalités :**

- Vue d'ensemble — 4 cartes de statistiques globales
- Graphique — bar chart comparatif Standard (Min) vs Valeurs Max par instance, avec option pour masquer le démarrage JVM à froid
- Tableau — filtrable et triable par instance, statut, ou temps de résolution, avec lien direct vers la solution
- Solutions détaillées — accordéon par instance avec les créneaux assignés à chaque réunion

**Déploiement :**

Dans les *Settings* du dépôt → *Pages* → source : `main / docs`.

**Tester localement :**

```bash
cd docs
python3 -m http.server
# Ouvrir http://localhost:8000
```

> Les données sont chargées via `fetch` et nécessitent un serveur HTTP (incompatible avec `file://`).

---

## Configuration solveur

| Configuration | Option PyCSP3 | Description |
|---|---|---|
| Standard (Min) | *(aucune)* | Heuristique par défaut (valeurs minimales) |
| Valeurs Max | `valh=max` | Sélection des valeurs maximales en premier |

---

## Structure du projet

```
.
├── 1_prepare_data.py          # Étape 1 : parsing texte brut → JSON
├── 2_run_benchmark.py         # Étape 2 : résolution + rapport Markdown
├── 3_export_web_data.py       # Étape 3 : export JSON pour le dashboard
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── instance_parser.py     # Parse le format texte brut CSPLib
│   ├── data_loader.py         # Charge un JSON d'instance processée
│   ├── model.py               # Modèle CSP + résolution (PyCSP3)
│   ├── benchmark.py           # Runner du benchmark
│   └── reporter.py            # Affichage console + génération Markdown
├── data/
│   ├── raw/
│   │   └── toutes_les_instances.txt
│   └── processed/             # JSON générés par 1_prepare_data.py
├── results/
│   └── benchmark_output.md    # Rapport généré par 2_run_benchmark.py
└── docs/                      # Dashboard GitHub Pages
    ├── index.html
    ├── style.css
    ├── app.js
    └── data/
        └── benchmark.json     # Données générées par 3_export_web_data.py
```
