import React, { useState } from "react";

async function computeSha256(file) {
  const arrayBuffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return "0x" + hex;
}

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [previewHash, setPreviewHash] = useState(null);
  const [status, setStatus] = useState(null);

  function onFileChange(e) {
    const f = e.target.files[0];
    setFile(f);
    setPreviewHash(null);
    setStatus(null);
    if (f) {
      computeSha256(f).then(h => setPreviewHash(h));
    }
  }

  async function onStore(e) {
    e.preventDefault();
    if (!file) return alert("Select a file");
    setStatus("Uploading...");
    const form = new FormData();
    form.append("file", file);
    const res = await fetch("http://127.0.0.1:8000/store", { method: "POST", body: form });
    const data = await res.json();
    setStatus(JSON.stringify(data, null, 2));
  }

  async function onVerify(e) {
    e.preventDefault();
    if (!file) return alert("Select a file");
    setStatus("Verifying...");
    const form = new FormData();
    form.append("file", file);
    const res = await fetch("http://127.0.0.1:8000/verify", { method: "POST", body: form });
    const data = await res.json();
    setStatus(JSON.stringify(data, null, 2));
  }

  return (
    <div className="max-w-xl mx-auto p-4">
      <h2 className="text-2xl font-semibold mb-4">Certificate Verifier</h2>
      <input type="file" accept="application/pdf" onChange={onFileChange} />
      {previewHash && <div className="mt-3">Client SHA-256: <code>{previewHash}</code></div>}
      <div className="mt-4 flex gap-2">
        <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={onStore}>Store on chain</button>
        <button className="px-4 py-2 bg-gray-600 text-white rounded" onClick={onVerify}>Verify</button>
      </div>
      {status && <pre className="mt-4 p-2 bg-gray-100 rounded">{status}</pre>}
    </div>
  );
}
