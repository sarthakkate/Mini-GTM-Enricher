import React, { useState, useEffect } from 'react';
import { uploadCSV, getBatchStatus } from './services/api';
import { Upload, Loader2, Table as TableIcon, CheckCircle, AlertCircle } from 'lucide-react';

function App() {
  const [file, setFile] = useState(null);
  const [batchId, setBatchId] = useState(null);
  const [status, setStatus] = useState('idle'); 
  const [results, setResults] = useState([]);

  useEffect(() => {
    let interval;
    if (batchId && (status === 'processing' || status === 'uploading')) {
      interval = setInterval(async () => {
        try {
          const data = await getBatchStatus(batchId);
          // Backend se 'results' array handle kar rahe hain
          if (data.results) setResults(data.results);
          if (data.status === 'completed') {
            setStatus('completed');
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [batchId, status]);

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    try {
      const res = await uploadCSV(file);
      setBatchId(res.id);
      setStatus('processing');
    } catch (err) {
      alert("Upload failed! Check Backend/Redis.");
      setStatus('idle');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8 font-sans">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-extrabold text-slate-900 mb-2">GTM Enricher</h1>
          <p className="text-slate-600">Upload CSV to get Explorium insights.</p>
        </header>

        <div className="bg-white border-2 border-dashed border-slate-300 rounded-2xl p-12 text-center shadow-sm mb-10">
          <input type="file" id="fileInput" accept=".csv" onChange={(e) => setFile(e.target.files[0])} className="hidden" />
          <label htmlFor="fileInput" className="cursor-pointer bg-slate-100 px-6 py-4 rounded-lg border mb-4 inline-block">
            {file ? file.name : "Select CSV"}
          </label>
          <br />
          <button onClick={handleUpload} disabled={!file || status === 'processing'} className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold">
            {status === 'idle' ? "Start Enrichment" : "Processing..."}
          </button>
        </div>

        {results.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border">
            <table className="w-full text-left">
              <thead className="bg-slate-50 text-xs font-bold uppercase text-slate-500">
                <tr>
                  <th className="p-4">Domain</th>
                  <th className="p-4">Industry</th>
                  <th className="p-4">Size</th>
                  <th className="p-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {results.map((row, i) => (
                  <tr key={i} className="hover:bg-slate-50">
                    <td className="p-4 font-medium">{row.domain}</td>
                    <td className="p-4">{row.industry || '—'}</td>
                    <td className="p-4">{row.company_size || '—'}</td>
                    <td className="p-4 text-center">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${row.enrichment_status === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                        {row.enrichment_status.toUpperCase()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;