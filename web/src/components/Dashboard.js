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

import { downloadReport, fetchDataset, fetchHistory, setToken, uploadDataset } from '../api';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

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

export default function Dashboard({ onLogout }) {
  const [history, setHistory] = useState([]);
  const [selected, setSelected] = useState(null);
  const [file, setFile] = useState(null);
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

  const pieData = useMemo(() => {
    return {
      labels: distLabels,
      datasets: [
        {
          label: 'Equipment Types',
          data: distValues,
          backgroundColor: [
            '#2563eb',
            '#7c3aed',
            '#059669',
            '#f59e0b',
            '#ef4444',
            '#14b8a6',
            '#64748b',
            '#a855f7',
          ],
        },
      ],
    };
  }, [distLabels, distValues]);

  const barData = useMemo(() => {
    return {
      labels: distLabels,
      datasets: [
        {
          label: 'Count',
          data: distValues,
          backgroundColor: '#2563eb',
        },
      ],
    };
  }, [distLabels, distValues]);

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
        <button className="button secondary" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <main className="grid">
        <section className="panel">
          <h2 className="panelTitle">Upload CSV</h2>
          <form onSubmit={handleUpload} className="row">
            <input
              className="file"
              type="file"
              accept=".csv,text/csv"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
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
                <Pie data={pieData} />
              </div>
              <div className="chart">
                <Bar
                  data={barData}
                  options={{
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } },
                  }}
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
    </div>
  );
}
