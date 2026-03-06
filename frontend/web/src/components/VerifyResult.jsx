import React from 'react';

export default function VerifyResult({ result }) {
  if (!result) return null;

  return (
    <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
      <h3 className="text-lg font-semibold text-green-800">Verification Result</h3>
      <p className="text-green-700">{result}</p>
    </div>
  );
}