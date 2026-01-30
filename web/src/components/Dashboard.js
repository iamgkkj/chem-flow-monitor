import { useEffect, useMemo, useState } from 'react';

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import ChartDataLabels from 'chartjs-plugin-datalabels';

import { downloadReport, fetchDataset, fetchHistory, setToken, uploadDataset } from '../api';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, ChartDataLabels);

const BLUE_PALETTE = [
  '#1d4ed8',
  '#2563eb',
  '#3b82f6',
  '#60a5fa',
  '#93c5fd',
  '#0ea5e9',
  '#0284c7',
  '#075985',
];

function formatNumber(n) {
  if (n === null || n === undefined || Number.isNaN(n)) return '—';
  return Number(n).toFixed(2);
}

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export default function Dashboard({ onLogout, theme, onToggleTheme }) {
  const [history, setHistory] = useState([]);
  const [selected, setSelected] = useState(null);
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('No file selected');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  async function refreshHistory() {
    const data = await fetchHistory();
    setHistory(data);
    if (!selected && data.length) {
      setSelected(data[0]);
    }
  }

  useEffect(() => {
    refreshHistory().catch((err) => {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to load history';
      setError(msg);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const typeDist = selected?.type_distribution || {};
  const distLabels = Object.keys(typeDist);
  const distValues = Object.values(typeDist);

  const chartTextColor = theme === 'light' ? '#0f172a' : '#e5e7eb';
  const gridColor = theme === 'light' ? 'rgba(15, 23, 42, 0.12)' : 'rgba(226, 232, 240, 0.15)';

  const pieData = useMemo(() => {
    return {
      labels: distLabels,
      datasets: [
        {
          label: 'Equipment Types',
          data: distValues,
          backgroundColor: distLabels.map((_, idx) => BLUE_PALETTE[idx % BLUE_PALETTE.length]),
          borderColor: theme === 'light' ? '#ffffff' : '#0b1220',
          borderWidth: 2,
        },
      ],
    };
  }, [distLabels, distValues, theme]);

  const barData = useMemo(() => {
    return {
      labels: distLabels,
      datasets: [
        {
          label: 'Count',
          data: distValues,
          backgroundColor: '#2563eb',
          borderRadius: 8,
        },
      ],
    };
  }, [distLabels, distValues]);

  const pieOptions = useMemo(() => {
    return {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: chartTextColor,
          },
        },
        datalabels: {
          color: theme === 'light' ? '#0b1220' : '#ffffff',
          backgroundColor: theme === 'light' ? 'rgba(255,255,255,0.75)' : 'rgba(2,6,23,0.55)',
          borderRadius: 6,
          padding: 6,
          font: { weight: '700' },
          formatter: (value, ctx) => {
            const dataArr = ctx.chart?.data?.datasets?.[0]?.data || [];
            const total = dataArr.reduce((a, b) => a + Number(b || 0), 0);
            if (!total) return '';
            const pct = (Number(value || 0) / total) * 100;
            return `${pct.toFixed(0)}%`;
          },
        },
        tooltip: {
          callbacks: {
            label: (item) => {
              const label = item.label || '';
              const value = item.raw;
              const dataArr = item.chart?.data?.datasets?.[0]?.data || [];
              const total = dataArr.reduce((a, b) => a + Number(b || 0), 0);
              const pct = total ? ((Number(value || 0) / total) * 100).toFixed(1) : '0.0';
              return `${label}: ${value} (${pct}%)`;
            },
          },
        },
      },
    };
  }, [chartTextColor, theme]);

  const barOptions = useMemo(() => {
    return {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true },
      },
      scales: {
        x: {
          ticks: { color: chartTextColor },
          grid: { color: gridColor },
        },
        y: {
          beginAtZero: true,
          ticks: { color: chartTextColor },
          grid: { color: gridColor },
        },
      },
    };
  }, [chartTextColor, gridColor]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;

    setError(null);
    setBusy(true);
    try {
      const created = await uploadDataset(file);
      setSelected(created);
      await refreshHistory();
      setFile(null);
      setFileName('No file selected');
      e.target.reset();
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || 'Upload failed';
      setError(msg);
    } finally {
      setBusy(false);
    }
  }

  async function handleSelect(id) {
    setError(null);
    setBusy(true);
    try {
      const data = await fetchDataset(id);
      setSelected(data);
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to load dataset';
      setError(msg);
    } finally {
      setBusy(false);
    }
  }

  async function handleDownload(id) {
    setError(null);
    setBusy(true);
    try {
      const blob = await downloadReport(id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `dataset_${id}_report.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to download report';
      setError(msg);
    } finally {
      setBusy(false);
    }
  }

  function handleLogout() {
    setToken(null);
    onLogout();
  }

  return (
    <div className="page">
      <header className="topbar">
        <div>
          <div className="brand">Chem Flow Monitor</div>
          <div className="muted">Equipment parameter visualizer</div>
        </div>
        <div className="topbarActions">
          <button className="button secondary" onClick={onToggleTheme}>
            {theme === 'dark' ? 'Light' : 'Dark'}
          </button>
          <button className="button secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="grid">
        <section className="panel">
          <h2 className="panelTitle">Upload CSV</h2>
          <form onSubmit={handleUpload} className="row">
            <input
              id="csvFile"
              className="fileInput"
              type="file"
              accept=".csv,text/csv"
              onChange={(e) => {
                const f = e.target.files?.[0] || null;
                setFile(f);
                setFileName(f ? f.name : 'No file selected');
              }}
            />
            <label className="button secondary" htmlFor="csvFile">
              Choose CSV
            </label>
            <div className="fileName" title={fileName}>
              {fileName}
            </div>
            <button className="button" type="submit" disabled={!file || busy}>
              {busy ? 'Working…' : 'Upload'}
            </button>
          </form>
          <div className="muted small">Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature</div>
          {error ? <div className="error" style={{ marginTop: 12 }}>{error}</div> : null}
        </section>

        <section className="panel">
          <h2 className="panelTitle">Latest Summary</h2>
          {selected ? (
            <div className="cards">
              <div className="stat">
                <div className="statLabel">Total Equipment</div>
                <div className="statValue">{selected.total_count}</div>
              </div>
              <div className="stat">
                <div className="statLabel">Avg Flowrate</div>
                <div className="statValue">{formatNumber(selected.avg_flowrate)}</div>
              </div>
              <div className="stat">
                <div className="statLabel">Avg Pressure</div>
                <div className="statValue">{formatNumber(selected.avg_pressure)}</div>
              </div>
              <div className="stat">
                <div className="statLabel">Avg Temperature</div>
                <div className="statValue">{formatNumber(selected.avg_temperature)}</div>
              </div>
            </div>
          ) : (
            <div className="muted">No dataset loaded yet.</div>
          )}
        </section>

        <section className="panel">
          <h2 className="panelTitle">Type Distribution</h2>
          {selected && distLabels.length ? (
            <div className="charts">
              <div className="chart">
                <Pie data={pieData} options={pieOptions} />
              </div>
              <div className="chart">
                <Bar
                  data={barData}
                  options={barOptions}
                />
              </div>
            </div>
          ) : (
            <div className="muted">Upload a dataset to see distribution.</div>
          )}
        </section>

        <section className="panel">
          <h2 className="panelTitle">History (last 5)</h2>
          <div className="table">
            <div className="tableHead">
              <div>ID</div>
              <div>Filename</div>
              <div>Uploaded</div>
              <div>Total</div>
              <div>Actions</div>
            </div>
            {history.map((d) => (
              <div className="tableRow" key={d.id}>
                <div>{d.id}</div>
                <div className="mono">{d.original_filename}</div>
                <div>{formatDate(d.created_at)}</div>
                <div>{d.total_count}</div>
                <div className="actions">
                  <button className="button small secondary" onClick={() => handleSelect(d.id)} disabled={busy}>
                    Load
                  </button>
                  <button className="button small" onClick={() => handleDownload(d.id)} disabled={busy}>
                    PDF
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="footerInner">
          <div className="footerNote">Developed by Gopal</div>
          <div className="footerLinks">
            <a
              className="iconLink"
              href="https://github.com/iamgkkj/"
              target="_blank"
              rel="noreferrer"
              title="GitHub"
            >
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">
                <path d="M12 .5C5.73.5.75 5.71.75 12.23c0 5.2 3.19 9.61 7.61 11.17.56.11.77-.25.77-.56 0-.27-.01-1.18-.02-2.14-3.1.7-3.75-1.37-3.75-1.37-.5-1.32-1.23-1.67-1.23-1.67-1-.7.08-.7.08-.7 1.11.08 1.7 1.2 1.7 1.2.99 1.76 2.6 1.25 3.23.96.1-.74.39-1.25.71-1.54-2.47-.29-5.07-1.28-5.07-5.72 0-1.26.43-2.28 1.14-3.08-.11-.29-.5-1.47.11-3.06 0 0 .94-.31 3.09 1.18.9-.26 1.86-.39 2.82-.39.96 0 1.93.13 2.82.39 2.15-1.49 3.09-1.18 3.09-1.18.61 1.59.22 2.77.11 3.06.71.8 1.14 1.82 1.14 3.08 0 4.45-2.61 5.42-5.1 5.71.4.36.76 1.06.76 2.14 0 1.54-.02 2.77-.02 3.14 0 .31.2.68.78.56 4.42-1.56 7.6-5.97 7.6-11.17C23.25 5.71 18.27.5 12 .5z" />
              </svg>
              <span className="srOnly">GitHub</span>
            </a>
            <a
              className="iconLink"
              href="https://www.linkedin.com/in/gopal-krishn-khoth-cse712003"
              target="_blank"
              rel="noreferrer"
              title="LinkedIn"
            >
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">
                <path d="M20.45 20.45h-3.55v-5.58c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.95v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.65-1.85 3.39-1.85 3.62 0 4.29 2.38 4.29 5.48v6.26zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.46C23.21 24 24 23.23 24 22.28V1.72C24 .77 23.21 0 22.23 0z" />
              </svg>
              <span className="srOnly">LinkedIn</span>
            </a>
            <a
              className="iconLink"
              href="https://mail.google.com/mail/u/2/#inbox?compose=GTvVlcRzCMfXjWgLcBtZskNXXJnNZrKsWbxlFdkxWtXjwgKqfXLHZgcPpbSsdXqQBzhFQvwTzFRpn"
              target="_blank"
              rel="noreferrer"
              title="Mail"
            >
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">
                <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z" />
              </svg>
              <span className="srOnly">Mail</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
