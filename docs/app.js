let allInstances = [];
let chartInstance = null;

fetch('data/benchmark.json')
  .then(r => r.json())
  .then(data => {
    allInstances = data.instances;
    document.getElementById('meta-generated').textContent = `Généré le ${data.generated}`;
    renderStats(data.instances);
    renderChart(data.instances);
    renderTable(data.instances);
    renderSolutions(data.instances);
  })
  .catch(() => {
    document.querySelector('main').innerHTML =
      '<p style="color:#c53030;padding:2rem">Impossible de charger les données. ' +
      'Lancez d\'abord <code>python3 3_export_web_data.py</code>, ' +
      'puis servez ce dossier avec <code>python3 -m http.server</code>.</p>';
  });

/* ── STATS ──────────────────────────────────────────────── */
function renderStats(instances) {
  const sat    = instances.filter(i => i.standard.status === 'SAT').length;
  const stdAvg = avg(instances.map(i => i.standard.time));
  const maxAvg = avg(instances.map(i => i.max.time));
  const stdAvgNoJvm = avg(instances.slice(1).map(i => i.standard.time));

  const cards = [
    {
      label: 'Instances traitées',
      value: instances.length,
      sub: 'CSPLib prob046',
    },
    {
      label: 'Satisfiables (SAT)',
      value: `${sat} / ${instances.length}`,
      sub: `${(sat / instances.length * 100).toFixed(0)} %`,
    },
    {
      label: 'Moy. Standard (Min)',
      value: `${stdAvg.toFixed(3)} s`,
      sub: `${stdAvgNoJvm.toFixed(3)} s hors démarrage JVM`,
    },
    {
      label: 'Moy. Valeurs Max',
      value: `${maxAvg.toFixed(3)} s`,
      sub: `Écart moy. ${Math.abs(stdAvg - maxAvg).toFixed(3)} s`,
    },
  ];

  document.getElementById('stats-grid').innerHTML = cards.map(c => `
    <div class="stat-card">
      <div class="stat-label">${c.label}</div>
      <div class="stat-value">${c.value}</div>
      <div class="stat-sub">${c.sub}</div>
    </div>
  `).join('');
}

/* ── CHART ──────────────────────────────────────────────── */
function renderChart(instances) {
  const hideFirst = document.getElementById('hide-first').checked;
  const data = hideFirst ? instances.slice(1) : instances;

  const labels   = data.map(i => `#${i.id}`);
  const stdTimes = data.map(i => i.standard.time);
  const maxTimes = data.map(i => i.max.time);

  if (chartInstance) {
    chartInstance.destroy();
  }

  const ctx = document.getElementById('timingChart').getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Standard (Min)',
          data: stdTimes,
          backgroundColor: 'rgba(43, 108, 176, 0.7)',
          borderColor: 'rgba(43, 108, 176, 1)',
          borderWidth: 1,
        },
        {
          label: 'Valeurs Max',
          data: maxTimes,
          backgroundColor: 'rgba(85, 60, 154, 0.45)',
          borderColor: 'rgba(85, 60, 154, 0.9)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 3,
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: 'Temps (s)', color: '#718096' },
          grid: { color: '#e2e8f0' },
          ticks: { color: '#718096' },
        },
        x: {
          title: { display: true, text: 'Instance', color: '#718096' },
          grid: { display: false },
          ticks: { color: '#718096' },
        },
      },
      plugins: {
        legend: { position: 'top', labels: { color: '#1a202c' } },
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.dataset.label} : ${ctx.raw.toFixed(4)} s`,
          },
        },
      },
    },
  });

  document.getElementById('hide-first').addEventListener('change', () => renderChart(allInstances));
}

/* ── TABLE ──────────────────────────────────────────────── */
function renderTable(instances) {
  document.getElementById('search').addEventListener('input', refreshTable);
  document.getElementById('status-filter').addEventListener('change', refreshTable);
  document.getElementById('sort-by').addEventListener('change', refreshTable);
  refreshTable();
}

function refreshTable() {
  const search = document.getElementById('search').value.toLowerCase();
  const statusFilter = document.getElementById('status-filter').value;
  const sortBy = document.getElementById('sort-by').value;

  let filtered = allInstances.filter(i => {
    const matchText = i.filename.toLowerCase().includes(search) ||
                      String(i.id).includes(search);
    const matchStatus = !statusFilter || i.standard.status === statusFilter;
    return matchText && matchStatus;
  });

  filtered = filtered.slice().sort((a, b) => {
    if (sortBy === 'time-std-asc') return a.standard.time - b.standard.time;
    if (sortBy === 'time-max-asc') return a.max.time - b.max.time;
    if (sortBy === 'diff-abs')
      return Math.abs(b.standard.time - b.max.time) - Math.abs(a.standard.time - a.max.time);
    return a.id - b.id;
  });

  const tbody = document.getElementById('table-body');
  const empty = document.getElementById('table-empty');

  if (filtered.length === 0) {
    tbody.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }

  empty.classList.add('hidden');

  tbody.innerHTML = filtered.map(i => {
    const diff = i.standard.time - i.max.time;
    const sign = diff >= 0 ? '+' : '';
    const diffClass = diff > 0.05 ? 'diff-pos' : diff < -0.05 ? 'diff-neg' : 'diff-zero';
    const statusClass = i.standard.status === 'SAT'   ? 'badge-sat' :
                        i.standard.status === 'UNSAT' ? 'badge-unsat' : 'badge-unknown';
    return `<tr>
      <td class="mono">${i.filename.replace('.json', '')}</td>
      <td>${i.n_meetings}</td>
      <td>${i.n_agents}</td>
      <td>${i.domain_size}</td>
      <td class="mono">${i.standard.time.toFixed(4)} s</td>
      <td class="mono">${i.max.time.toFixed(4)} s</td>
      <td class="mono ${diffClass}">${sign}${diff.toFixed(4)} s</td>
      <td><span class="badge ${statusClass}">${i.standard.status}</span></td>
      <td><button class="btn-link" onclick="jumpToSolution(${i.id})">Solution →</button></td>
    </tr>`;
  }).join('');
}

function jumpToSolution(id) {
  const acc = document.getElementById(`acc-${id}`);
  if (!acc) return;
  if (!acc.classList.contains('open')) acc.classList.add('open');
  acc.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── SOLUTIONS ──────────────────────────────────────────── */
function renderSolutions(instances) {
  document.getElementById('solutions-list').innerHTML = instances
    .filter(i => i.solution && i.solution.length > 0)
    .map(i => {
      const timeSummary = `Standard : ${i.standard.time.toFixed(3)} s · Max : ${i.max.time.toFixed(3)} s`;
      return `
        <div class="accordion" id="acc-${i.id}">
          <div class="accordion-header" onclick="toggleAccordion(${i.id})">
            <div>
              <span class="accordion-title">Instance #${i.id}</span>
              <span class="accordion-meta"> — ${i.n_meetings} réunions · ${i.n_agents} agents · domaine {0…${i.domain_size - 1}}</span>
            </div>
            <div class="accordion-right">
              <span class="accordion-meta">${timeSummary}</span>
              <svg class="accordion-icon" width="16" height="16" viewBox="0 0 24 24"
                   fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>
          <div class="accordion-body">
            <div class="solution-grid">
              ${i.solution.map((slot, m) => `
                <div class="meeting-item">
                  <span class="meeting-id">Réunion ${m}</span>
                  <span class="meeting-slot">→ ${slot}</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;
    }).join('');
}

function toggleAccordion(id) {
  document.getElementById(`acc-${id}`).classList.toggle('open');
}

function expandAll() {
  document.querySelectorAll('.accordion').forEach(a => a.classList.add('open'));
}

function collapseAll() {
  document.querySelectorAll('.accordion').forEach(a => a.classList.remove('open'));
}

/* ── UTILS ──────────────────────────────────────────────── */
function avg(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}
